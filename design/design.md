### System Architecture Diagram

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                            OFFLINE INGESTION FLOW                           │
│                     (scripts/ingest_embeddings.py)                          │
│                                                                             │
│  ┌─────────────────────────┐        ┌──────────────────────────────────┐    │
│  │ data/                   │        │ app.ingestion.pdf_loader         │    │
│  │ acme-simple_employee... ├───────►│ Extract text per page (pypdf)    │    │
│  └─────────────────────────┘        └────────────────┬─────────────────┘    │
│                                                      │                      │
│                                                      ▼                      │
│  ┌─────────────────────────┐        ┌──────────────────────────────────┐    │
│  │ app.storage.vector_store│        │ app.ingestion.chunker            │    │
│  │ Write to PostgreSQL +   │◄───────┤ Split into section-aware chunks  │    │
│  │ pgvector (384-dim)      │        └────────────────┬─────────────────┘    │
│  └─────────────────────────┘                         │                      │
│                                                      ▼                      │
│                                     ┌──────────────────────────────────┐    │
│                                     │ app.ingestion.embedder           │    │
│                                     │ sentence-transformers/all-MiniLM │    │
│                                     └──────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘

===============================================================================

┌─────────────────────────────────────────────────────────────────────────────┐
│                           ONLINE RETRIEVAL & Q&A FLOW                       │
│                        (app/ui + FastAPI Backend + Groq)                    │
│                                                                             │
│  ┌─────────────────────────┐               ┌─────────────────────────────┐  │
│  │ React Web UI            │  POST /query  │ FastAPI Web Server          │  │
│  │ (app/ui - Vite)         ├──────────────►│ (app/api/main.py)           │  │
│  │ Client sends query      │◄──────────────┤ Returns JSON answer         │  │
│  └─────────────────────────┘  Answer JSON  └──────────────┬──────────────┘  │
│                                                           │                 │
│                                                           ▼                 │
│                                            ┌─────────────────────────────┐  │
│                                            │ app.ingestion.embedder      │  │
│                                            │ Embed user question         │  │
│                                            └──────────────┬──────────────┘  │
│                                                           │                 │
│                                                           ▼                 │
│  ┌─────────────────────────┐               ┌─────────────────────────────┐  │
│  │ PostgreSQL + pgvector   │ Vector Search │ app.storage.vector_store    │  │
│  │ (docker/docker-compose) ├──────────────►│ Similarity search (<=>)     │  │
│  │ document_chunks table   │  Top-K Chunks │ Fetch matching context      │  │
│  └─────────────────────────┘               └──────────────┬──────────────┘  │
│                                                           │                 │
│                                                           ▼                 │
│                                            ┌─────────────────────────────┐  │
│                                            │ app.rag.context_builder     │  │
│                                            │ Format context string       │  │
│                                            └──────────────┬──────────────┘  │
│                                                           │                 │
│                                                           ▼                 │
│                                            ┌─────────────────────────────┐  │
│                                            │ app.rag.prompt_builder      │  │
│                                            │ System + Context + Question │  │
│                                            └──────────────┬──────────────┘  │
│                                                           │                 │
│                                                           ▼                 │
│  ┌─────────────────────────┐               ┌─────────────────────────────┐  │
│  │ Groq Cloud API          │  API Call     │ app.llm.groq_client         │  │
│  │ Groq SDK LLM Inference  │◄──────────────┤ Dispatch prompt to Groq API │  │
│  │ Generates answer        ├──────────────►│ Returns response            │  │
│  └─────────────────────────┘  Grounded Ans └─────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘

```

---

### Key Design Notes

#### 1. Ingestion Pipeline (Offline Execution)

* **Document Extraction (`app.ingestion.pdf_loader`)**: Utilizes `pypdf` to parse incoming PDF documents while preserving page-boundary boundaries.


* **Section-Aware Chunking (`app.ingestion.chunker`)**: Splits raw extracted text into chunk blocks based on numbered headings.


* **Dense Vector Generation (`app.ingestion.embedder`)**: Uses `sentence-transformers/all-MiniLM-L6-v2` to generate 384-dimensional dense vector embeddings.


* **Vector Persistence (`app.storage.vector_store`)**: Stores document metadata, section chunks, and 384-dim embeddings inside PostgreSQL with the `pgvector` extension enabled.



#### 2. Query Pipeline (Online Interactive Execution)

* **Frontend Layer (`app/ui`)**: React + Vite single-page web app running on port `5173`. Sends query payloads via `POST /query`.


* **Backend API (`app/api/main.py`)**: FastAPI server handling CORS configuration and service routing.


* **Semantic Vector Search**: Incoming queries are embedded using the same `sentence-transformers` model and searched against PostgreSQL using `pgvector` vector distance operators (`<=>` cosine/L2 distance).


* **Context Construction (`app.rag.context_builder`)**: Formats retrieved Top-$K$ text chunks into standard text blocks ready for prompt assembly.


* **Prompt Assembly (`app.rag.prompt_builder`)**: Constructs a strict system prompt containing domain instructions, relevant document context, and the user's question.


* **Inference Execution (`app.llm.groq_client`)**: Dispatches the assembled prompt to Groq API endpoints using the official `groq` SDK for fast LLM response generation.



#### 3. Configuration & Infrastructure

* **Environment Configuration (`app/core/config.py`)**: Centralized management loading variables (Groq keys, model choices, DB connections) via `.env`.


* **Containerization (`docker/docker-compose.yml`)**: Packages PostgreSQL with `pgvector` pre-configured for local developer deployment.