# 🧮 Aplikasi Tracking Level Matematika (Streamlit + Google Sheets)

Aplikasi web untuk tracking level siswa dengan sistem **bayar per sub-level**
menggunakan kode akses unik. Dibangun dengan Streamlit, database Google Sheets,
siap deploy ke Streamlit Cloud.

## 📁 Struktur File

```
├── app.py                          # Aplikasi utama (UI Guru & Siswa)
├── config.py                       # Data 31 level x 6 sub-level + harga
├── questions.py                    # 186 generator soal acak (5 soal/sub-level)
├── sheets_manager.py                # Integrasi Google Sheets (database)
├── requirements.txt                 # Dependencies Python
├── .streamlit/
│   └── secrets.toml.example         # Contoh file kredensial (JANGAN dipakai langsung)
└── README.md                        # Dokumen ini
```

## ✨ Fitur

- **31 Level x 6 Sub-Level = 186 sub-level**, masing-masing punya 5 soal yang
  **dibuat secara acak** (random) setiap kali dikerjakan — jadi siswa yang
  mengulang akan mendapat soal berbeda, bukan soal yang sama persis.
- **Harga otomatis** berdasarkan tingkat kesulitan (Mudah Rp5.000 / Sedang
  Rp10.000 / Sulit Rp15.000).
- **Kode akses unik** format `SL{level}{sub}-{6 digit acak}`, berlaku 7 hari,
  hanya bisa dipakai 1 kali.
- **Panel Guru**: generate kode akses, lihat daftar kode, data siswa, dan riwayat.
- **Panel Siswa**: daftar/login dengan nama, masukkan kode akses, kerjakan 5 soal,
  otomatis naik level jika skor ≥ 80%.
- Semua data tersimpan di **Google Sheets** (4 sheet: `siswa`, `riwayat`,
  `kode_akses`, `pretest`).

## 🚀 Langkah Setup

### 1. Siapkan Google Sheet

1. Buat 1 file Google Spreadsheet baru (nama bebas, misal "DB Tracking Matematika").
2. Salin **ID spreadsheet**-nya dari URL:
   `https://docs.google.com/spreadsheets/d/`**`ID_SPREADSHEET_ADA_DI_SINI`**`/edit`
3. Sheet (tab) di dalamnya **tidak perlu dibuat manual** — aplikasi akan otomatis
   membuat 4 sheet (`siswa`, `riwayat`, `kode_akses`, `pretest`) beserta headernya
   saat pertama kali dijalankan.

### 2. Buat Service Account Google Cloud (agar aplikasi bisa akses Sheet)

1. Buka [Google Cloud Console](https://console.cloud.google.com/).
2. Buat project baru (atau pakai yang sudah ada).
3. Aktifkan 2 API berikut di menu "APIs & Services > Library":
   - **Google Sheets API**
   - **Google Drive API**
4. Buka menu "APIs & Services > Credentials" → "Create Credentials" →
   "Service Account". Beri nama bebas, lalu klik "Done".
5. Klik service account yang baru dibuat → tab "Keys" → "Add Key" →
   "Create new key" → pilih **JSON** → download filenya.
6. Buka file JSON tersebut, kamu akan butuh isinya untuk langkah berikutnya.
7. **Penting:** buka kembali Google Spreadsheet yang dibuat di langkah 1, klik
   "Share", lalu **tambahkan email service account** (ada di field `client_email`
   pada file JSON, formatnya seperti
   `nama@nama-project.iam.gserviceaccount.com`) dengan akses **Editor**.

### 3. Isi File Secrets

Salin file `.streamlit/secrets.toml.example` menjadi `.streamlit/secrets.toml`,
lalu isi:

- `spreadsheet_id` → ID spreadsheet dari langkah 1.
- `guru_password` → password bebas untuk masuk ke Panel Guru.
- Bagian `[gcp_service_account]` → salin semua field dari file JSON yang
  didownload di langkah 2 (type, project_id, private_key, client_email, dst).
  Perhatikan `private_key` harus tetap memakai tanda kutip dan `\n` di
  dalamnya (jangan diubah formatnya).

⚠️ **Jangan pernah commit file `secrets.toml` (yang sudah diisi) ke GitHub**
karena berisi kredensial rahasia. File `.example` aman untuk di-commit karena
isinya cuma contoh kosong.

### 4. Jalankan Secara Lokal (opsional, untuk uji coba)

```bash
pip install -r requirements.txt
streamlit run app.py
```

### 5. Deploy ke Streamlit Cloud

1. Push seluruh folder project ini (kecuali `secrets.toml` asli) ke repository
   GitHub.
2. Buka [share.streamlit.io](https://share.streamlit.io/), klik "New app",
   hubungkan ke repo GitHub kamu, pilih file utama `app.py`.
3. Sebelum deploy (atau setelahnya via menu app → "Settings" → "Secrets"),
   tempelkan seluruh isi file `secrets.toml` yang sudah kamu isi di langkah 3.
4. Klik "Deploy". Selesai — aplikasi bisa diakses via URL publik.

## 🧭 Cara Pakai

### Sebagai Guru
1. Buka aplikasi, pilih mode **Guru** di sidebar, masukkan password.
2. Tab **Generate Kode Akses**: pilih level & sub-level yang dibeli siswa,
   harga otomatis muncul, klik "Generate Kode Akses", lalu berikan kode
   tersebut ke siswa setelah pembayaran diterima.
3. Tab **Daftar Kode / Data Siswa / Riwayat**: memantau semua aktivitas.

### Sebagai Siswa
1. Pilih mode **Siswa**, masukkan nama (daftar dulu jika baru pertama kali).
2. Masukkan kode akses yang diberikan guru, lalu kerjakan 5 soal.
3. Jika skor ≥ 80% → otomatis naik ke sub-level berikutnya (butuh kode baru
   untuk lanjut). Jika < 80% → perlu kode baru untuk mengulang sub-level yang
   sama.

## 📝 Catatan tentang Bank Soal

Soal dibuat lewat **generator terprogram** (bukan daftar statis 930 soal),
sehingga:
- Soal selalu bervariasi (angka acak setiap percobaan) — mencegah siswa
  menghafal jawaban temannya.
- Lebih mudah dipelihara/ditambah dibanding menyimpan 930 baris soal manual.
- Semua 186 generator sudah diuji otomatis dan menghasilkan soal + kunci
  jawaban yang valid.

Jika ke depannya kamu ingin bank soal yang benar-benar statis (fixed, tidak
acak) untuk keperluan tertentu, generator di `questions.py` bisa dengan mudah
dikonversi menjadi daftar soal tetap.

## 🔧 Menyesuaikan Harga / Level

Semua harga & struktur level ada di `config.py` (dictionary `LEVELS` dan
`HARGA`). Ubah nilainya untuk menyesuaikan dengan kebutuhanmu.
