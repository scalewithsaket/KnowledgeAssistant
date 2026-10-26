# Knowledge Assistant

Knowledge Assistant is a lightweight retrieval-augmented generation (RAG) project for answering questions from a PDF-based knowledge base. It extracts text from a document, splits it into logical sections, converts the text into embeddings, stores those embeddings in PostgreSQL with pgvector, retrieves the most relevant chunks for a question, and sends the result to Groq for grounded answer generation.

This project is designed for document-grounded Q&A over enterprise policy or knowledge documents such as HR handbooks, internal policy PDFs, and reference material.

## Features

- PDF text extraction with `pypdf`
- Section-aware chunking based on numbered headings
- Embeddings with `sentence-transformers`
- Vector similarity search using PostgreSQL + pgvector
- Retrieval pipeline for domain-specific context construction
- Prompt assembly and LLM answer generation with Groq
- Dockerized PostgreSQL setup for local development
- Example ingestion and Q&A scripts to run end-to-end

## Architecture

The application follows a standard RAG flow:

```text
PDF
  ↓
Text extraction
  ↓
Section-aware chunking
  ↓
Embedding generation
  ↓
PostgreSQL + pgvector
  ↓
Semantic retrieval
  ↓
Context construction
  ↓
Prompt construction
  ↓
Groq LLM
  ↓
Answer
```

## Tech Stack

- Python 3.10+
- `pypdf` for PDF parsing
- `sentence-transformers` for embeddings
- `psycopg` for PostgreSQL access
- `pgvector` extension for vector similarity search
- `groq` SDK for LLM calls
- Docker Compose for local PostgreSQL

## Repository Structure

```text
.
├── app/
│   ├── core/
│   ├── ingestion/
│   ├── llm/
│   ├── rag/
│   └── storage/
├── data/
│   └── acme-simple_employee_leave_policy.pdf
├── docker/
│   └── docker-compose.yml
├── scripts/
│   ├── ingest_embeddings.py
│   ├── test_chunker.py
│   ├── test_context_builder.py
│   ├── test_embedder.py
│   ├── test_groq_encoding.py
│   ├── test_pdf_loader.py
│   ├── test_prompt_builder.py
│   ├── test_rag.py
│   ├── test_similarity.py
│   └── test_vector_search.py
├── .env
├── requirements.txt
├── pyproject.toml
├── final_flow.md
├── README.md
└── ...
```

## Prerequisites

Before running the project, make sure you have:

- Python 3.10 or newer
- `pip` with access to the Python package index
- Docker Desktop or Docker Engine installed for PostgreSQL
- A Groq API key

## Setup

1. Clone the repository.
2. Create and activate a virtual environment:

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Configure environment variables. The project loads values from a `.env` file in the project root. Example:

```env
GROQ_API_KEY=your_groq_api_key
LLM_MODEL=openai/gpt-oss-120b
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ragdb
DB_USER=raguser
DB_PASSWORD=your_db_password
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
LLM_TEMPERATURE=0
LLM_MAX_COMPLETION_TOKENS=8192
LLM_TOP_P=1
LLM_REASONING_EFFORT=medium
LLM_STREAM=false
```

## PostgreSQL + pgvector Setup

Start the local database container:

```bash
docker compose -f docker/docker-compose.yml up -d
```

Then connect to PostgreSQL and create the extension and table used by the app:

```sql
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS document_chunks (
    id SERIAL PRIMARY KEY,
    document_id TEXT,
    document_name TEXT,
    page_number INTEGER,
    section TEXT,
    chunk_text TEXT,
    embedding vector(384),
    embedding_model TEXT
);
```

The project currently uses the `sentence-transformers/all-MiniLM-L6-v2` model, which produces 384-dimensional embeddings. If you switch models, make sure the vector dimension matches the embedding size.

## Ingesting the Knowledge Base

The sample PDF is located at `data/acme-simple_employee_leave_policy.pdf`.

Run the ingestion pipeline:

```bash
python scripts/ingest_embeddings.py
```

This script:

- extracts text from the PDF
- chunks the text by numbered sections
- loads the embedding model
- embeds each chunk
- writes each chunk and its embedding into `document_chunks`

## Running a Sample Query

The project includes a demo retrieval and answer generation pipeline:

```bash
python scripts/test_rag.py
```

This script performs the following:

1. embeds the user question
2. searches for semantically similar document chunks in PostgreSQL
3. builds a context block from the retrieved results
4. creates the final prompt for the LLM
5. asks Groq for a grounded answer

## Running the Web UI

Start the API from the repository root:

```bash
uvicorn app.api.main:app --reload
```

In another terminal, install the UI dependencies and start Vite:

```bash
cd app/ui
npm install
npm run dev
```

Copy `app/ui/.env.example` to `app/ui/.env`, then configure the API address:

```env
RAG_API_URL=http://127.0.0.1:8000
```

The React app runs at `http://127.0.0.1:5173` and calls the API directly on its separate port. The API allows requests from the local Vite origins `http://127.0.0.1:5173` and `http://localhost:5173`. The UI sends questions to `POST /query` and displays only the returned answer.

## Important Modules

### `app.ingestion.pdf_loader`
Extracts text from PDF pages while preserving page boundaries.

### `app.ingestion.chunker`
Splits extracted text into logical chunks based on section headings.

### `app.ingestion.embedder`
Creates normalized embeddings using Sentence Transformers.

### `app.storage.vector_store`
Stores embeddings and runs similarity search with pgvector.

### `app.rag.context_builder`
Formats the retrieved chunks into a prompt-compatible context string.

### `app.rag.prompt_builder`
Constructs the final system and user prompts sent to the LLM.

### `app.llm.groq_client`
Calls the Groq chat completion API.

## Environment and Configuration

Application settings are centralized in `app/core/config.py` and are loaded from `.env` via `python-dotenv`.

The main configuration keys are:

- `GROQ_API_KEY`
- `LLM_MODEL`
- `DB_HOST`
- `DB_PORT`
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`
- `EMBEDDING_MODEL`
- `LLM_TEMPERATURE`
- `LLM_MAX_COMPLETION_TOKENS`
- `LLM_TOP_P`
- `LLM_REASONING_EFFORT`
- `LLM_STREAM`

## Example Workflow

1. Start PostgreSQL with Docker.
2. Create the `document_chunks` table and pgvector extension.
3. Populate the knowledge base by running `scripts/ingest_embeddings.py`.
4. Ask a question by editing the query inside `scripts/test_rag.py` or replacing the script with a custom entry point.
5. Run the script to get a grounded answer backed by the retrieved document context.

## Testing

The repository contains a set of focused scripts under `scripts/` for validating individual components such as chunking, embedding, similarity, and prompt building. You can run any script directly, for example:

```bash
python scripts/test_chunker.py
python scripts/test_embedder.py
python scripts/test_similarity.py
python scripts/test_prompt_builder.py
```

## Notes

- The current project is a clean, minimal RAG prototype intended for learning and experimentation.
- It is optimized for a single PDF document and a local PostgreSQL setup.
- For production use, it would be beneficial to add:
  - secure secret management
  - automated database migrations
  - multi-document ingestion
  - asynchronous pipeline jobs
  - evaluation and logging
  - an API layer or web UI

## License

This project is provided as-is for educational and experimental use.
  - secure secret management
  - automated database migrations
  - multi-document ingestion
  - asynchronous pipeline jobs
  - evaluation and logging
  - API layer or web UI

## License

This project is provided as-is for educational and experimental use.
