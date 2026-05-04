# Backend BP2TL Chatbot

## Setup Cepat

1. Buat virtual environment:
```bash
python -m venv venv
```

2. Aktifkan virtual environment:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Setup environment variables:
```bash
cp .env.example .env
# Edit .env dengan credentials Supabase Anda
```

5. Load data:
```bash
python load_data.py
```

6. Jalankan server:
```bash
python main.py
```

Server akan berjalan di `http://localhost:8000`

## Environment Variables

Buat file `.env` dengan isi:

```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
OLLAMA_BASE_URL=http://localhost:11434
```

## Arsitektur RAG

1. **User Query** → Input dari user
2. **Embedding** → E5-base encode query
3. **Vector Search** → FAISS retrieve top 10
4. **Reranking** → Cross-encoder pilih top 3
5. **LLM Generation** → Ollama LLaMA 3 generate jawaban
6. **Response** → Return ke user

## Model yang Digunakan

- **Embedding**: intfloat/e5-base (768 dim)
- **Reranker**: cross-encoder/ms-marco-MiniLM-L-6-v2
- **LLM**: llama3 via Ollama

Semua model berjalan LOKAL (offline).
