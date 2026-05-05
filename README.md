# Chatbot Helpdesk BP2TL Jakarta

Chatbot AI Helpdesk untuk BP2TL Jakarta dengan sistem RAG (Retrieval-Augmented Generation) menggunakan model groq.

## Teknologi yang Digunakan

### Backend
- **FastAPI** - Web framework
- **Embedding**: intfloat/e5-base (LOCAL)
- **Vector Search**: FAISS
- **Reranker**: cross-encoder/ms-marco-MiniLM-L-6-v2
- **LLM**: groq
- **Database**: Supabase (PostgreSQL)

### Frontend
- **React** + **Vite** + **TypeScript**
- **Tailwind CSS**
- **Lucide React** (icons)

## Fitur

- RAG advanced dengan E5 embedding + reranker
- Respons natural menggunakan groq 
- UI chat seperti WhatsApp
- Responsive (desktop & mobile)
- Simpan riwayat chat
- Auto-scroll
- Typing indicator

## Prasyarat

1. **Python 3.9+**
2. **Node.js 18+**
3. **Ollama** - [Install Ollama](https://ollama.ai)
4. **Supabase Account** - Database sudah dikonfigurasi

## Instalasi

### 1. Install Ollama dan Download Model

```bash
# Install Ollama dari https://ollama.ai

# Download model llama3
ollama pull llama3

# Jalankan Ollama (biarkan berjalan)
ollama run llama3
```

### 2. Setup Backend

```bash
cd backend

# Buat virtual environment
python -m venv venv

# Aktifkan virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy .env.example ke .env
cp .env.example .env

# Edit .env dan isi dengan credentials Supabase Anda
# SUPABASE_URL=your_supabase_url
# SUPABASE_KEY=your_supabase_anon_key
```

### 3. Load Data

```bash
# Masih di folder backend dengan venv aktif
python load_data.py
```

Script ini akan:
- Load FAQ dari `data/faq.csv`
- Load knowledge dari `data/knowledge/*.txt`
- Generate embeddings
- Simpan ke database Supabase
- Buat FAISS index

### 4. Jalankan Backend

```bash
# Masih di folder backend dengan venv aktif
python main.py
```

Backend akan berjalan di `http://localhost:8000`

### 5. Setup Frontend

Buka terminal baru:

```bash
# Install dependencies
npm install

# Jalankan dev server
npm run dev
```

Frontend akan berjalan di `http://localhost:5173`

## Cara Menggunakan

1. Pastikan Ollama sudah berjalan (`ollama run llama3`)
2. Jalankan backend (`python main.py`)
3. Jalankan frontend (`npm run dev`)
4. Buka browser ke `http://localhost:5173`
5. Mulai chat dengan bot!

## Struktur Project

```
.
├── backend/
│   ├── main.py                 # FastAPI server
│   ├── config.py               # Konfigurasi
│   ├── models.py               # Pydantic models
│   ├── embedding_service.py    # E5 embedding service
│   ├── vector_store.py         # FAISS vector store
│   ├── reranker_service.py     # Cross-encoder reranker
│   ├── ollama_service.py       # Ollama LLM integration
│   ├── database.py             # Supabase database
│   ├── load_data.py            # Data loading script
│   └── requirements.txt
├── data/
│   ├── faq.csv                 # FAQ data
│   └── knowledge/              # Knowledge base (.txt files)
├── src/
│   ├── components/             # React components
│   ├── types.ts                # TypeScript types
│   └── App.tsx                 # Main app
└── README.md

```

## Menambah Data

### FAQ
Edit file `data/faq.csv` dengan format:
```csv
question,answer
"Pertanyaan 1","Jawaban 1"
"Pertanyaan 2","Jawaban 2"
```

### Knowledge Base
Tambahkan file `.txt` di folder `data/knowledge/`

Setelah menambah data, jalankan:
```bash
cd backend
python load_data.py
```

## API Endpoints

- `GET /` - Info API
- `GET /health` - Health check
- `POST /chat` - Chat endpoint

Request:
```json
{
  "message": "Apa itu BP2TL?",
  "session_id": "optional-session-id"
}
```

Response:
```json
{
  "response": "BP2TL Jakarta adalah...",
  "session_id": "session-id"
}
```

## Troubleshooting

### Backend tidak bisa start
- Pastikan virtual environment sudah aktif
- Pastikan semua dependencies terinstall
- Cek file `.env` sudah diisi dengan benar

### Ollama error
- Pastikan Ollama sudah running: `ollama run llama3`
- Cek Ollama berjalan di `http://localhost:11434`

### Model download lambat
- Model E5 dan reranker akan otomatis didownload saat pertama kali dijalankan
- Tunggu hingga selesai (sekitar 1-2 GB)

## Catatan Penting

- Aplikasi ini 100% lokal, tidak ada koneksi ke API eksternal (kecuali Supabase untuk database)
- Model AI berjalan di komputer Anda
- Membutuhkan RAM minimal 8GB (16GB recommended)
- Pertama kali akan download model (1-2GB)

## Lisensi

MIT
