# Panduan Setup BP2TL Chatbot Helpdesk

Panduan lengkap untuk menjalankan Chatbot Helpdesk BP2TL Jakarta.

## Prasyarat Sistem

1. **Python 3.11 atau lebih tinggi**
   - Download: https://www.python.org/downloads/


## Langkah Setup

### 1. Install dan Setup Groq

```bash
# Download dan install groq dari https://ollama.ai

# Setelah install, download model llama3
ollama pull llama3

# Test Ollama (buka terminal baru)
ollama run llama3
```

**PENTING**: Biarkan Ollama tetap berjalan di terminal ini!

### 2. Setup database phpmyadmin

1. Login ke http://172.16.1.19/myadminphp
2. Buat database baru
3. Buat tabel-tabel yang dibutuhkan
4. Simpan

### 3. Setup Backend

Buka terminal baru:

```bash
# Masuk ke folder backend
cd backend

# Buat virtual environment
python -m venv venv

# Aktifkan virtual environment
# Untuk Windows:
venv\Scripts\activate
# Untuk Linux/Mac:
source venv/bin/activate

# Install dependencies (akan memakan waktu beberapa menit)
pip install -r requirements.txt
```

**Catatan**: Pastikan koneksi internet stabil.

### 4. Konfigurasi Environment Variables

```bash
# Edit file .env dengan text editor favorit Anda
# Isi dengan credentials :

SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
OLLAMA_BASE_URL=http://localhost:11434
```

### 5. Load Data ke Database

```bash
# Pastikan virtual environment masih aktif (lihat (venv) di terminal)
# Jika belum aktif, aktifkan lagi:
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate

# Jalankan script load data
python load_data.py
```

Output yang diharapkan:
```
Loading embedding model: intfloat/e5-base
Embedding model loaded successfully
Loading reranker model: cross-encoder/ms-marco-MiniLM-L-6-v2
Reranker model loaded successfully
============================================================
Initializing BP2TL Chatbot Data
============================================================
Loading FAQ from ../data/faq.csv...
Found 20 FAQ entries
Loaded FAQ 1/20
Loaded FAQ 2/20
...
FAQ data loaded successfully
Loading knowledge from ../data/knowledge...
Found 3 knowledge files
Loaded knowledge 1/3: tentang_bp2tl.txt
Loaded knowledge 2/3: sistem_oss.txt
Loaded knowledge 3/3: jam_operasional.txt
Knowledge data loaded successfully

FAISS index saved successfully
============================================================
Data initialization completed!
============================================================
```

**CATATAN PENTING**:
- Proses pertama kali akan download model embedding dan reranker (~1GB)
- Tunggu hingga selesai, JANGAN dibatalkan
- Jika error, pastikan Supabase credentials benar

### 6. Jalankan Backend Server

```bash
# Masih di folder backend dengan venv aktif
python main.py
```

Output:
```
Loading FAISS index...
FAISS index loaded successfully with 23 documents
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**JANGAN tutup terminal ini!** Backend harus tetap berjalan.


### 8. Buka Browser

Buka browser dan akses: **http://localhost:5173**

Anda akan melihat chatbot dengan pesan selamat datang!

## Checklist Sebelum Mulai

- [ ] Ollama sudah terinstall dan running (`ollama run llama3`)
- [ ] Backend sudah running di http://localhost:8000
- [ ] Frontend sudah running di http://localhost:5173
- [ ] Browser terbuka di http://localhost:5173

## Testing

Coba tanyakan ke chatbot:
- "Apa itu BP2TL Jakarta?"
- 
-
## Troubleshooting

### Error: "Module not found"
```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
npm install
```

### Error: "Ollama connection refused"
```bash
# Pastikan Ollama running
ollama run llama3
```

### Error: "FAISS index not found"
```bash
# Load data lagi
cd backend
python load_data.py
```

### Error: "Supabase error"
- Cek file `.env` di folder backend
- Pastikan SUPABASE_URL dan SUPABASE_KEY benar
- Test koneksi ke Supabase dashboard

### Frontend tidak bisa connect ke backend
- Pastikan backend running di http://localhost:8000
- Buka http://localhost:8000 di browser, harus ada response JSON
- Cek console browser untuk error

## Menambah Data

### Menambah FAQ

1. Edit file `data/faq.csv`
2. Tambahkan baris baru dengan format:
   ```csv
   "Pertanyaan baru","Jawaban baru"
   ```
3. Jalankan ulang: `python load_data.py`

### Menambah Knowledge Base

1. Buat file `.txt` baru di folder `data/knowledge/`
2. Isi dengan informasi yang ingin ditambahkan
3. Jalankan ulang: `python load_data.py`

## Spesifikasi Teknis

### Model AI yang Digunakan:
- **Embedding**: intfloat/e5-base (768 dimensions)
- **Reranker**: cross-encoder/ms-marco-MiniLM-L-6-v2
- **LLM**: LLaMA 3 via Ollama

### Pipeline RAG:
1. User query → E5 embedding
2. FAISS vector search (top 10)
3. Cross-encoder reranking (top 3)
4. LLaMA 3 generation dengan context
5. Natural language response

### Kebutuhan Sistem:
- **RAM**: Minimal 8GB (Recommended 16GB)
- **Storage**: ~5GB untuk semua model
- **CPU**: Multi-core recommended
- **Internet**: Hanya untuk setup awal (download model)

## Support

Jika mengalami masalah:
1. Cek bagian Troubleshooting di atas
2. Pastikan semua prasyarat terpenuhi
3. Cek log error di terminal backend
4. Cek console browser untuk error frontend

