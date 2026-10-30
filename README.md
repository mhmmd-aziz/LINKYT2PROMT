# 🚗 imzy tools yt (v2.2)
> **Google Flow Edition: Kids YouTube Remake Engine (Full 10-Second Continuous Spoken English Script + Seamless 60-Scene Story Flow)**

**imzy tools yt** adalah aplikasi web modern berbasis **React TSX + FastAPI** yang dirancang khusus untuk membuat ulang (*remake*) konten **video YouTube anak-anak (lagi main mobil-mobilan, monster truck, Hot Wheels, balapan ceria, suara vroom-vroom/sound effects kartun)** ke format **60 scene prompt**.

Setiap scene kini menghasilkan **percakapan / voiceover penuh 10 detik tanpa jeda kosong dalam bahasa Inggris (English)** yang saling menyambung dari Scene 1 sampai Scene 60, lengkap dengan kunci konsistensi objek mobil & karakter 100% paten.

---

## 🌟 Fitur Baru: Full 10s Continuous English Speech & Story Flow

1. **Percakapan Full 10 Detik Penuh Tanpa Ruang Kosong (No Dead Air)**
   - Setiap scene menghasilkan naskah voiceover bahasa Inggris berenergi tinggi sebanyak **22 hingga 28 kata** yang pas mengisi tepat durasi 10 detik penuh tanpa hening atau ruang kosong.
   - Siap dipakai untuk voiceover, Text-to-Speech (seperti ElevenLabs), atau dibacakan langsung.

2. **Alur Cerita Bersambung Antar Setiap Scene (Seamless Narrative Continuity)**
   - Scene 1 mengawali balapan dan menderukan mesin di garis start.
   - Scene 2 meluncurkan mobil menuruni tanjakan.
   - Scene 3 bermanuver di tikungan tajam.
   - Scene berikutnya menghadapi rintangan balok kayu, tanjakan lompat 360°, terowongan pelangi, hingga selebrasi kemenangan di garis finish.
   - Setiap scene saling menyambung secara logis dan natural (*builds upon the previous scene*).

3. **Bahasa Inggris Standar Global (English Voiceover)**
   - Sesuai standar video anak-anak viral dunia, narasi percakapan dihasilkan dalam bahasa Inggris yang ramah anak, ekspresif, dan ceria.

4. **Kunci Objek & Karakter 100% Konsisten (No Morphing)**
   - Mobil mainan (model bodi, warna cat merah-kuning menyala, motif ban bergerigi, velg) dan tokoh anak dikunci identik di setiap scene prompt.
   - Format prompt dibuat sinematik mengalir alami (*fluid 3D Pixar/Disney style*), tanpa pemisah kurung siku kaku.

5. **Viral YouTube Kit (Judul FYP, Deskripsi SEO & Prompt Thumbnail AI Gemini)**
   - **5 Judul Hype FYP Bahasa Inggris**: Dirancang dengan teknik CTR tinggi standar video anak YouTube (stunt ramp focus, loop challenge, speed obstacle).
   - **Prompt Gambar Thumbnail AI (16:9 Widescreen)**: Diformulasikan khusus untuk Google Gemini / Imagen 3 / Midjourney dengan efek 3D pop-out mobil melompat ke arah kamera, ekspresi wajah anak kagum, warna neon kontras tinggi, dan pencahayaan studio Pixar 8K.
   - **Deskripsi SEO Lengkap**: Mencakup sinopsis cerita seru, 8 milestone chapter timestamps (00:00, 01:40, 03:20, ...), ajakan subscribe, dan hashtag viral.
   - **Tags YouTube SEO**: 17 kata kunci pencarian teratas untuk langsung disalin ke kolom tags YouTube Studio.

6. **Dukungan Model AI Lengkap**:
   - **DeepSeek-V4.1-Flash** ([deepseek-ai/DeepSeek-V4.1-Flash-1017](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash-1017)) via Hugging Face Router.
   - **DeepSeek Official API** (`deepseek-chat`).
   - **Google Gemini 1.5 Flash Vision AI**.
   - **Smart Kids Director Engine (Dynamic Local Mode)**: Tetap bisa menghasilkan 60 scene English monologue lengkap secara offline/gratis tanpa API key.

7. **Fitur Ekspor Lengkap**:
   - 1-Klik Salin Prompt Video (untuk Kling AI / Google Veo / Runway Gen-3).
   - 1-Klik Salin YouTube Kit Lengkap (Judul, Deskripsi, Thumbnail Prompt).
   - 1-Klik Salin Naskah Voiceover English (untuk ElevenLabs / dubbing).
   - Download YouTube Kit (.TXT), Naskah Suara (.TXT), Subtitle (.SRT), JSON, dan CSV Spreadsheet.

---

## 🚀 Cara Menjalankan

Cukup klik dua kali file [`start.bat`](file:///d:/script/LINKYT2PROMPT/start.bat) atau lewat terminal:
```bash
python run.py
```
Buka browser di:
👉 **`http://127.0.0.1:8000`**
