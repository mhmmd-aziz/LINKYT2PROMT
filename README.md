# ⚡ imzy affilate
> **Google Flow Edition: Alat Ekstraksi Transkrip YouTube ke Prompt Video AI Konsisten (10 Detik Penuh per Scene)**

Aplikasi web modern berbasis **React TSX + FastAPI** yang dirancang persis dengan visual alur **Google Flow / Google AI Studio**. Membantu kreator konten & affiliate marketer mengubah link YouTube menjadi alur storyboard prompt teks-ke-video (untuk Google Veo, Kling AI, Runway Gen-3, Luma Dream Machine) dengan konsistensi objek dan tokoh 100%.

---

## 🌟 Fitur Utama

1. **Modal Copas Link YouTube**
   - Cukup masukkan URL video YouTube, YouTube Shorts, atau ID video.
   - Mengambil judul video, thumbnail, pembuat konten, dan total durasi secara akurat.

2. **Ekstraksi Transkrip Percakapan Lengkap**
   - Mengambil seluruh teks percakapan dan audio subtitle dengan stempel waktu detik milidetik.
   - Pencarian percakapan interaktif & fitur salin seluruh transkrip.
   - Dual-engine: Menggunakan YouTube Transcript API cepat, dengan fallback ke **Faster-Whisper** lokal bertenaga GPU.

3. **Per Scene 10 Detik Penuh**
   - Video dibagi menjadi segmen tepat **10 detik per scene**.
   - Menghitung jumlah scene secara otomatis menyesuaikan durasi total video YouTube (misal video 60 detik = 6 scene, 120 detik = 12 scene).
   - Seluruh percakapan yang diucapkan dalam rentang 10 detik dirangkum penuh tanpa terpotong.

4. **Konsistensi Objek & Karakter Antar Scene (Google Flow Matrix)**
   - Menjaga objek affiliasi / produk yang di-review tetap konsisten dari Scene 1 sampai Scene terakhir.
   - Mengunci deskripsi wajah, pakaian, dan persona subjek kreator agar tidak berubah (no morphing).
   - Latar belakang studio dan pencahayaan sinematik dipertahankan seragam.
   - Rotasi sudut kamera sinematik dinamis (Wide Establishing ➔ Medium Dialogue ➔ Macro Product Close-up ➔ Over-the-shoulder ➔ CTA Ending).

5. **Bahasa Otomatis Menyesuaikan Video Asli**
   - Mendeteksi bahasa percakapan video (Bahasa Indonesia atau English).
   - Menghasilkan aksi visual, dialog, dan struktur prompt video dalam bahasa yang sesuai.

6. **Deteksi Hardware Otomatis (GPU CUDA & CPU)**
   - Otomatis mendeteksi kartu grafis sistem Anda (contoh: **NVIDIA GeForce RTX 3050 Laptop GPU 4GB VRAM**).
   - Menampilkan status VRAM, versi CUDA, dan kesehatan komputasi langsung di UI.
   - Jika GPU tidak tersedia atau dinonaktifkan, aplikasi otomatis fallback ke mode multi-core CPU.

7. **Alur Prompt Langsung ke Generator Video (Prompt-to-Video Flow)**
   - 1-Klik Salin Prompt untuk setiap scene.
   - Tombol Export Batch: Salin Seluruh Alur Prompt, Download JSON, Download CSV / Spreadsheet, dan Subtitle (.SRT).

---

## 🚀 Cara Menjalankan

### Cara Cepat (Rekomendasi):
Cukup jalankan file `start.bat` dengan klik dua kali, atau lewat terminal:
```bash
python run.py
```
Aplikasi akan otomatis mendeteksi GPU Anda dan membuka browser di `http://127.0.0.1:8000`.

### Mode Pengembangan (Developer):
Jika ingin melakukan pengeditan frontend React TSX:
1. Jalankan backend:
   ```bash
   python -m uvicorn server.main:app --host 127.0.0.1 --port 8000 --reload
   ```
2. Jalankan frontend Vite:
   ```bash
   npm run dev
   ```
   Buka `http://localhost:3000`.

---

## 🛠️ Struktur Project

```
LINKYT2PROMPT/
├── dist/                   # Hasil build frontend siap saji
├── server/                 # Backend FastAPI
│   ├── hardware.py         # Deteksi GPU NVIDIA CUDA & CPU
│   ├── transcriber.py      # Ekstraksi YouTube Transcript & Whisper
│   ├── prompt_engine.py    # Logika Scene 10s & Konsistensi Objek
│   └── main.py             # FastAPI REST Endpoints & File Server
├── src/                    # Frontend React TSX
│   ├── components/
│   │   ├── Header.tsx          # Navigasi & Badge Hardware
│   │   ├── HardwareBadge.tsx   # Modal & Status GPU / CPU
│   │   ├── UrlInputNode.tsx    # Node 01: Input YouTube Link
│   │   ├── ConsistencyNode.tsx # Node 02: Kunci Konsistensi 10s
│   │   ├── TranscriptNode.tsx  # Node 03: Transkrip Percakapan YT
│   │   ├── SceneFlowNode.tsx   # Node 04: Alur Prompt-to-Video
│   │   └── ExportModal.tsx     # Modal Ekspor Format Lengkap
│   ├── App.tsx             # Canvas Alur Google Flow
│   ├── types.ts            # Definisi TypeScript
│   └── index.css           # Styling Google Flow & Tailwind
├── run.py                  # Script Peluncur Otomatis Satu Perintah
├── start.bat               # Windows Launcher
└── package.json            # Dependensi React & Vite
```

