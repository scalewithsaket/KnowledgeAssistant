PDF
 ↓
Text extraction
 ↓
Section-aware chunking
 ↓
Embedding
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


                  ┌──────────────────────┐
                  │   Knowledge Base     │
                  │ PostgreSQL + pgvector│
                  └──────────┬───────────┘
                             │
                             │ retrieve
                             ▼
Question ──► Embedding ──► Retriever
                             │
                             ▼
                     Context Builder
                             │
                             ▼
                     Prompt Builder
                             │
                             ▼
                       Groq Client
                             │
                             ▼
                          Answer