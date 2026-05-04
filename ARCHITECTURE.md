# Arsitektur Sistem Chatbot BP2TL Jakarta

## Overview

Chatbot Helpdesk BP2TL Jakarta adalah aplikasi AI berbasis RAG (Retrieval-Augmented Generation)

## Arsitektur  

```
┌─────────────────────────────────────────────────────────────┐
│                        USER INTERFACE                        │
│              (React + Vite + TypeScript)                     │
│                                  │
└─────────────────────┬───────────────────────────────────────┘
                      │ HTTP (POST /chat)
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                      FASTAPI BACKEND                        │
│                                                             │
│  ┌────────────────────────────────────────────────────┐     │
│  │           RAG PIPELINE (Advanced)                  │     │
│  │                                                    │     │
│  │  1. User Query                                     │     │
│  │       ↓                                            │     │
│  │  2. E5 Embedding (intfloat/e5-base)                │     │
│  │       ↓                                            │     │
│  │  3. FAISS Vector Search (Top 10)                   │     │
│  │       ↓                                            │     │
│  │  4. Cross-Encoder Reranking (Top 3)                │     │
│  │       ↓                                            │     │
│  │  5. Context Injection                              │     │
│  │       ↓                                            │     │
│  │  6. Ollama LLaMA 3 Generation                      │     │
│  │       ↓                                            │     │
│  │  7. Natural Response                               │     │
│  └────────────────────────────────────────────────────┘     │
│                                                             │
└───────────┬──────────────────────────────┬──────────────────┘
            │                              │
            ▼                              ▼
┌─────────────────────┐      ┌──────────────────────────┐
│   OLLAMA SERVER     │      │   SUPABASE DATABASE      │
│   (localhost:11434) │      │   (PostgreSQL + pgvector)│
│                     │      │                          │
│   Model: llama3     │      │  - FAQ table             │
│   Running locally   │      │  - Knowledge table       │
└─────────────────────┘      │  - Chat history table    │
                             │  - Vector embeddings     │
                             └──────────────────────────┘
```

## Komponen Utama

### 1. Frontend (React)

**Teknologi:**
- React 18 + TypeScript
- Vite (build tool)
- Tailwind CSS (styling)
- Lucide React (icons)

**Komponen:**
- `ChatBubble`: Bubble pesan user & bot
- `ChatInput`: Input field dengan auto-resize
- `TypingIndicator`: Animasi typing bot
- `App`: Main component dengan state management

**Fitur:**
- Auto-scroll ke pesan terbaru
- Session management
- Loading states
- Error handling
- Responsive design

### 2. Backend (FastAPI)

**Struktur:**
```
backend/
├── main.py              # FastAPI app & endpoints
├── config.py            # Konfigurasi global
├── models.py            # Pydantic models
├── embedding_service.py # E5 embedding
├── vector_store.py      # FAISS management
├── reranker_service.py  # Cross-encoder reranking
├── ollama_service.py    # Ollama integration
├── database.py          # Supabase client
└── load_data.py         # Data initialization
```

**API Endpoints:**
- `GET /` - Info API
- `GET /health` - Health check dengan metrics
- `POST /chat` - Main chat endpoint

### 3. RAG Pipeline (Detail)

#### Step 1: Embedding
```python
# Format E5
Query: "query: {user_input}"
Document: "passage: {content}"

# Model: intfloat/e5-base
# Output: 768-dimensional vector
# Normalized dengan L2 normalization
```

#### Step 2: Vector Search
```python
# FAISS IndexFlatIP (Inner Product)
# Similarity: Cosine similarity
# Retrieve: Top 10 kandidat
# Fast: O(n) untuk flat index
```

#### Step 3: Reranking
```python
# Model: cross-encoder/ms-marco-MiniLM-L-6-v2
# Input: (query, document) pairs
# Output: Relevance scores
# Select: Top 3 most relevant
```

#### Step 4: LLM Generation
```python
# Model: LLaMA 3 via Ollama
# Temperature: 0.7
# Top-p: 0.9
# Context: Top 3 reranked documents
# System prompt: Anti-halusinasi
```

## Data Flow

### Chat Request Flow
```
1. User mengetik pesan → Frontend
2. Frontend kirim POST /chat → Backend
3. Backend generate embedding → E5 Model
4. Backend search FAISS → Top 10 results
5. Backend rerank → Cross-Encoder → Top 3
6. Backend format prompt + context → Ollama
7. Ollama generate response → LLaMA 3
8. Backend return response → Frontend
9. Frontend display di chat bubble
10. Save to Supabase (async)
```

### Data Loading Flow
```
1. Load FAQ dari CSV → Pandas
2. Load Knowledge dari TXT → File I/O
3. Generate embeddings → E5 Model
4. Save to Supabase → PostgreSQL
5. Build FAISS index → Vector Store
6. Save FAISS index → Disk (pickle)
```

## Database Schema (Supabase)

### Table: faq
```sql
id           uuid PRIMARY KEY
question     text NOT NULL
answer       text NOT NULL
embedding    vector(768)
created_at   timestamptz
```

### Table: knowledge
```sql
id           uuid PRIMARY KEY
content      text NOT NULL
source_file  text NOT NULL
embedding    vector(768)
created_at   timestamptz
```

### Table: chat_history
```sql
id            uuid PRIMARY KEY
session_id    text NOT NULL
user_message  text NOT NULL
bot_response  text NOT NULL
created_at    timestamptz
```

## Model Specifications

### Embedding Model: E5-base
- **Model**: intfloat/e5-base
- **Dimensions**: 768
- **Type**: Sentence Transformer
- **Size**: ~438MB
- **Speed**: ~50ms per query
- **Keunggulan**:
  - State-of-the-art untuk retrieval
  - Instruction-aware (query vs passage)
  - Multilingual support (termasuk Indonesia)

### Reranker: Cross-Encoder
- **Model**: cross-encoder/ms-marco-MiniLM-L-6-v2
- **Type**: Cross-Encoder
- **Size**: ~90MB
- **Speed**: ~30ms untuk 10 pairs
- **Keunggulan**:
  - Lebih akurat dari bi-encoder
  - MS MARCO trained (high quality)
  - Fast inference

### LLM: LLaMA 3
- **Model**: Meta LLaMA 3 (8B parameters)
- **Via**: Ollama
- **Size**: ~4.7GB
- **Context**: 8192 tokens
- **Keunggulan**:
  - Open source
  - Natural Indonesian
  - Instruction following
  - Fast on consumer hardware

## Vector Store (FAISS)

**Configuration:**
```python
Index Type: IndexFlatIP
Metric: Inner Product (cosine similarity)
Dimension: 768
Normalization: L2 normalized vectors
```

**Keunggulan FAISS:**
- Sangat cepat untuk search
- Memory efficient
- Support untuk billion-scale
- CPU optimized (SIMD)

**Trade-offs:**
- Flat index: O(n) search time
- Suitable untuk <1M vectors
- Bisa upgrade ke IVF untuk scale

## Security & Anti-Halusinasi

### 1. Context Injection
Semua respons WAJIB berdasarkan context yang di-retrieve:
```python
prompt = f"""
Jawab HANYA berdasarkan informasi berikut.
Jangan menambahkan informasi di luar konteks.

Konteks: {contexts}

Pertanyaan: {query}
"""
```

### 2. Fallback Response
Jika tidak ada context yang relevan:
```python
"Mohon maaf kak, untuk informasi tersebut belum tersedia.
Silakan cek: https://linktr.ee/bpptljkt"
```

### 3. Row Level Security (RLS)
Semua tabel di Supabase menggunakan RLS dengan policy:
- Public read untuk FAQ & knowledge
- Public insert untuk chat history (demo)

## Performance Metrics

### Latency Breakdown (Average)
```
Embedding:           ~50ms
FAISS Search:        ~10ms
Reranking:           ~30ms
Ollama Generation:   ~2000ms (depends on response length)
Total:               ~2100ms
```

### Resource Usage
```
RAM:
  - E5 model:         ~500MB
  - Reranker:         ~200MB
  - LLaMA 3:          ~5GB
  - FAISS index:      ~10MB (for 1K docs)
  - Total:            ~6GB

Storage:
  - Models:           ~5.2GB
  - FAISS index:      ~10MB
  - Database:         Variable
```

## Scalability

### Current Capacity
- Documents: Up to 100K (dengan flat FAISS)
- Users: Unlimited (stateless API)
- Concurrent: Limited by Ollama (1 request at a time)

### Scaling Options
1. **FAISS Index**: Upgrade ke IVF/HNSW untuk 1M+ docs
2. **LLM**: Gunakan multiple Ollama instances
3. **Caching**: Redis untuk frequent queries
4. **Load Balancing**: Multiple backend instances

## Deployment Options

### Development (Current)
- Frontend: Vite dev server (localhost:5173)
- Backend: Uvicorn (localhost:8000)
- Ollama: Local (localhost:11434)
- Database: Supabase Cloud

### Production (Recommended)
- Frontend: Nginx/Apache static hosting
- Backend: Gunicorn + Uvicorn workers
- Ollama: Dedicated server (GPU recommended)
- Database: Supabase Cloud atau self-hosted PostgreSQL

## Keunggulan Arsitektur

1. **100% Lokal**: Tidak ada biaya API recurring
2. **Privacy**: Data tidak keluar dari infrastruktur Anda
3. **No Vendor Lock-in**: Semua komponen open source
4. **Scalable**: Bisa di-scale sesuai kebutuhan
5. **Accurate**: RAG dengan reranker = high quality
6. **Fast**: Optimized pipeline dengan FAISS
7. **Maintainable**: Clean architecture, modular

## Limitasi & Trade-offs

1. **Hardware**: Butuh RAM 8GB+ dan CPU decent
2. **Setup**: Initial setup lebih kompleks
3. **Maintenance**: Update model manual
4. **Concurrent**: Ollama handle 1 request at a time
5. **Multilingual**: LLaMA 3 best di English, decent di Indonesian

## Future Improvements

1. **Caching Layer**: Redis untuk frequent queries
2. **Async LLM**: Queue system untuk concurrent
3. **Better Embeddings**: Upgrade ke E5-large atau BGE-large
4. **Hybrid Search**: Combine vector + keyword search
5. **Monitoring**: Logging, metrics, alerting
6. **A/B Testing**: Compare different prompts/models
7. **Fine-tuning**: Train model dengan domain data
