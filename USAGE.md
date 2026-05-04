# Panduan Penggunaan Chatbot BP2TL Jakarta

## Cara Menggunakan Chatbot

### 1. Interface Chat


### 2. Mengirim Pesan

1. Ketik pertanyaan Anda di kotak input
2. Tekan Enter atau klik tombol kirim
3. Tunggu bot memproses (akan muncul animasi typing)
4. Jawaban akan muncul dalam bubble putih di kiri

### 3. Jenis Pertanyaan yang Bisa Dijawab

Chatbot dapat menjawab pertanyaan seputar:

**Informasi Umum:**
- Apa itu BP2TL Jakarta?
- Visi dan misi BP2TL
- Lokasi kantor
- Jam operasional
- Kontak

**Informasi Diklat:**
- Diklat Pelaut
- Diklat Fungsional

### 4. Tips Bertanya

**DO (Lakukan):**
- Tanyakan satu hal dalam satu pesan
- Gunakan bahasa yang jelas dan spesifik
- Contoh: "Bagaimana cara mendaftar diklat?"

**DON'T (Hindari):**
- Pertanyaan yang terlalu umum: "Tolong bantu saya"
- Pertanyaan di luar domain BP2TL
- Multiple pertanyaan dalam satu pesan

### 6. Jika Informasi Tidak Tersedia

Jika bot tidak menemukan informasi, akan menampilkan:
```
"Mohon maaf kak 😊, untuk informasi tersebut belum tersedia.
Silakan cek: https://linktr.ee/bpptljkt"
```

Anda bisa:
- Coba tanyakan dengan kata-kata berbeda
- Akses link yang diberikan untuk info lebih lanjut
- Hubungi BP2TL langsung

### 7. Session Management

- Setiap user mendapat session ID otomatis
- Chat history disimpan per session
- Session tetap aktif selama browser terbuka
- Refresh page akan membuat session baru

### 8. Fitur-Fitur

**Auto Scroll:**
- Chat otomatis scroll ke pesan terbaru
- Tidak perlu scroll manual

**Typing Indicator:**
- Animasi titik-titik saat bot sedang memikirkan jawaban
- Menunjukkan bot sedang memproses

**Timestamp:**
- Setiap pesan punya timestamp
- Format: HH:MM (24 jam)

**Responsive:**
- Bisa digunakan di desktop dan mobile
- Layout otomatis menyesuaikan ukuran layar

## Menambah atau Mengubah Data

### Menambah FAQ

1. Buka file `data/faq.csv`
2. Tambahkan baris baru dengan format:
   ```csv
   "Pertanyaan baru?","Jawaban untuk pertanyaan baru"
   ```
3. Save file
4. Jalankan di terminal backend:
   ```bash
   python load_data.py
   ```
5. Restart backend server

### Menambah Knowledge Base

1. Buat file `.txt` baru di folder `data/knowledge/`
2. Isi dengan informasi yang ingin ditambahkan
3. Save file
4. Jalankan di terminal backend:
   ```bash
   python load_data.py
   ```
5. Restart backend server

### Format Knowledge Base

File `.txt` sebaiknya berisi:
- Paragraf informasi yang koheren
- Tidak terlalu panjang (max 500 kata per file)
- Satu topik per file
- Gunakan bahasa Indonesia yang baik

## Melihat Chat History

Chat history tersimpan di database Supabase:

1. Login ke dashboard Supabase
2. Pilih project Anda
3. Buka Table Editor
4. Pilih table `chat_history`
5. Lihat semua percakapan

## Performance

**Response Time:**
- Normal: 2-3 detik
- Slow: 5-10 detik (jika sistem sibuk)

**Jika Lambat:**
- Pastikan Ollama running dengan baik
- Cek resource komputer (RAM, CPU)
- Restart Ollama jika perlu
- Pertimbangkan upgrade hardware

## Batasan Sistem

**Tidak bisa menjawab:**
- Pertanyaan di luar domain BP2TL/perizinan
- Informasi yang tidak ada di database
- Pertanyaan real-time (cuaca, berita)
- Perhitungan kompleks
- Informasi pribadi/rahasia

**Hanya bisa menjawab:**
- Informasi yang ada di FAQ
- Informasi yang ada di knowledge base
- Pertanyaan seputar BP2TL Jakarta

## Support
Jika mengalami masalah teknis:
- Refresh halaman browser
- Clear cache browser
- Restart backend server
- Check terminal untuk error log
