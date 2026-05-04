# Quick Start Guide - BP2TL Chatbot

Panduan cepat untuk menjalankan chatbot.

## Prasyarat

1. Python 3.9+ installed
2. Node.js 18+ installed
3. Ollama installed dari https://ollama.ai

## Langkah 1: Setup Ollama

```bash
# Download model llama3
ollama pull llama3

# Jalankan Ollama (terminal 1 - biarkan tetap berjalan)
ollama run llama3
```

## Langkah 2: Setup Backend

Buka terminal baru:

```bash
cd backend

# Buat virtual environment
python -m venv venv

# Aktifkan virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies (akan memakan waktu, download ~1-2GB model)
pip install -r requirements.txt
```

## Langkah 3: Load Data

```bash
# Masih di folder backend dengan venv aktif
python load_data.py
```

Tunggu hingga selesai. Proses ini akan:
- Load FAQ dan knowledge base
- Generate embeddings dengan E5
- Simpan ke Supabase
- Build FAISS index

## Langkah 4: Jalankan Backend

```bash
# Masih di folder backend dengan venv aktif
python main.py
```

Backend akan berjalan di `http://localhost:8000`

**JANGAN tutup terminal ini!**

## Langkah 5: Jalankan Frontend

Buka terminal BARU:

```bash
# Dari root project
npm install
npm run dev
```

Frontend akan berjalan di `http://localhost:5173`

## Buka Browser

Akses: **http://localhost:5173**

Mulai chat dengan bot!

---

## Checklist

Pastikan semua berjalan:

- [ ] Terminal 1: Ollama running (`ollama run llama3`)
- [ ] Terminal 2: Backend running (`python main.py`)
- [ ] Terminal 3: Frontend running (`npm run dev`)
- [ ] Browser: http://localhost:5173 terbuka

## Test Query

## Troubleshooting Cepat

**Backend error saat load_data.py:**
- Pastikan file `backend/.env` ada dan berisi Supabase credentials
- Cek koneksi internet (untuk download model pertama kali)

**Ollama connection error:**
- Pastikan Ollama running: `ollama run llama3`
- Test: buka http://localhost:11434 di browser

**Frontend tidak bisa connect:**
- Pastikan backend running di http://localhost:8000
- Test: buka http://localhost:8000 di browser

---

Untuk panduan lengkap, lihat: `SETUP_GUIDE.md`
