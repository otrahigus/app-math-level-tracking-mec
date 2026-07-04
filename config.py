# -*- coding: utf-8 -*-
"""
Konfigurasi Level, Sub-Level, Kesulitan, dan Harga
Sistem Tracking Level Siswa - Matematika
"""

HARGA = {
    "Mudah": 5000,
    "Sedang": 10000,
    "Sulit": 15000,
}

# Struktur: level -> { "materi": str, "kesulitan": str, "sub": {sub_no: nama_sub} }
LEVELS = {
    0: {"materi": "Berhitung 1-50, +/- Dasar", "kesulitan": "Mudah", "sub": {
        1: "Berhitung 1 (1-20)",
        2: "Penjumlahan dasar 1 (bawah 20)",
        3: "Pengurangan dasar 1 (bawah 20)",
        4: "Berhitung 2 (20-50)",
        5: "Penjumlahan dasar 2 (bawah 50)",
        6: "Pengurangan dasar 2 (bawah 50)",
    }},
    1: {"materi": "Berhitung 1-100, +/- Menyimpan/Meminjam", "kesulitan": "Mudah", "sub": {
        1: "Berhitung 3 (1-100)",
        2: "Penjumlahan dasar 3 (tanpa menyimpan, bawah 100)",
        3: "Penjumlahan dengan menyimpan (bawah 100)",
        4: "Pengurangan dasar 3 (tanpa meminjam, bawah 100)",
        5: "Pengurangan dengan meminjam (bawah 100)",
        6: "Soal cerita campuran (1 langkah)",
    }},
    2: {"materi": "Perkalian & Pembagian 1-10", "kesulitan": "Mudah", "sub": {
        1: "Perkalian dasar 1 (1-5)",
        2: "Pembagian dasar 1 (1-5)",
        3: "Perkalian dasar 2 (6-10)",
        4: "Pembagian dasar 2 (6-10)",
        5: "Soal cerita perkalian & pembagian (1 langkah)",
        6: "Operasi hitung campuran (+/-) 2 suku",
    }},
    3: {"materi": "Bersusun Ratusan, Nilai Tempat, Membandingkan", "kesulitan": "Mudah", "sub": {
        1: "Penjumlahan bersusun panjang (ratusan, dengan menyimpan)",
        2: "Pengurangan bersusun panjang (ratusan, dengan meminjam)",
        3: "Nilai tempat (ratusan, ribuan)",
        4: "Membandingkan & mengurutkan bilangan sampai 1.000",
        5: "Perkalian bersusun (2 digit x 1 digit)",
        6: "Soal cerita 2 langkah (+/-/x/: campuran)",
    }},
    4: {"materi": "Pecahan Dasar, +/- Penyebut Sama", "kesulitan": "Mudah", "sub": {
        1: "Pengenalan pecahan sederhana (1/2, 1/3, 1/4)",
        2: "Membandingkan pecahan dengan gambar & angka",
        3: "Penjumlahan pecahan berpenyebut sama",
        4: "Pengurangan pecahan berpenyebut sama",
        5: "Pengenalan desimal (persepuluh, perseratus)",
        6: "Soal cerita pecahan & desimal (1 langkah)",
    }},
    5: {"materi": "Perkalian 2 Digit x 2 Digit, Pembagian 2 Digit : 1 Digit", "kesulitan": "Mudah", "sub": {
        1: "Perkalian bersusun (2 digit x 2 digit)",
        2: "Pembagian bersusun (2 digit : 1 digit, tanpa sisa)",
        3: "Mengubah pecahan ke desimal (1/2, 1/4, 3/4, 1/5)",
        4: "Operasi hitung campuran dengan kurung (prioritas operasi)",
        5: "Soal cerita multi-langkah (3-4 langkah)",
        6: "Pengenalan persentase sederhana (10%, 25%, 50%)",
    }},
    6: {"materi": "Menyederhanakan Pecahan, +/- Penyebut Beda", "kesulitan": "Sedang", "sub": {
        1: "Menyederhanakan pecahan dengan FPB",
        2: "Penjumlahan pecahan berpenyebut berbeda (penyebut kelipatan)",
        3: "Pengurangan pecahan berpenyebut berbeda (penyebut kelipatan)",
        4: "Perkalian pecahan dengan bilangan bulat",
        5: "Pembagian pecahan dengan bilangan bulat",
        6: "Mengubah desimal ke pecahan (1 & 2 angka di belakang koma)",
    }},
    7: {"materi": "Bilangan Bulat Positif/Negatif", "kesulitan": "Sedang", "sub": {
        1: "Penjumlahan bilangan bulat positif & negatif",
        2: "Pengurangan bilangan bulat positif & negatif",
        3: "Perkalian & pembagian bilangan bulat",
        4: "Operasi hitung campuran bilangan bulat (tanpa kurung)",
        5: "Operasi hitung campuran bilangan bulat (dengan kurung)",
        6: "Soal cerita bilangan bulat (suhu, utang, ketinggian)",
    }},
    8: {"materi": "Satuan & Pengukuran", "kesulitan": "Sedang", "sub": {
        1: "Satuan panjang (km, m, cm, mm) konversi & operasi",
        2: "Satuan berat (kg, g, mg) konversi & operasi",
        3: "Satuan waktu (jam, menit, detik) konversi & operasi",
        4: "Satuan volume & debit (liter, ml)",
        5: "Keliling & luas persegi & persegi panjang",
        6: "Soal cerita pengukuran (panjang, berat, waktu) 2 langkah",
    }},
    9: {"materi": "Pola Bilangan, Variabel, Persamaan Sederhana", "kesulitan": "Sedang", "sub": {
        1: "Pola bilangan sederhana (+, -, x, :)",
        2: "Pengenalan variabel (x, y) dalam kalimat matematika",
        3: "Menyelesaikan persamaan sederhana (x + a = b, x - a = b)",
        4: "Menyelesaikan persamaan sederhana (a x x = b, x : a = b)",
        5: "Membaca & menyajikan data dalam tabel & diagram batang",
        6: "Menentukan mean (rata-rata) dari data tunggal",
    }},
    10: {"materi": "Nilai Tempat sampai 10.000", "kesulitan": "Sedang", "sub": {
        1: "Nilai tempat sampai 10.000 (puluhan ribu)",
        2: "Membandingkan & mengurutkan bilangan sampai 10.000",
        3: "Penjumlahan & pengurangan sampai 10.000 (bersusun)",
        4: "Perkalian bersusun (3 digit x 1 digit)",
        5: "Pembagian bersusun (3 digit : 1 digit, tanpa sisa)",
        6: "Soal cerita operasi campuran (2-3 langkah, sampai 10.000)",
    }},
    11: {"materi": "+/- Pecahan Penyebut Beda, Tidak Kelipatan", "kesulitan": "Sedang", "sub": {
        1: "Penjumlahan pecahan berpenyebut berbeda (tidak kelipatan)",
        2: "Pengurangan pecahan berpenyebut berbeda (tidak kelipatan)",
        3: "Perkalian pecahan (pembilang x pembilang, penyebut x penyebut)",
        4: "Pembagian pecahan (dibalik & kali)",
        5: "Mengubah pecahan campuran ke pecahan biasa & sebaliknya",
        6: "Soal cerita operasi hitung pecahan (2 langkah)",
    }},
    12: {"materi": "Perbandingan, Skala, Untung/Rugi, Diskon", "kesulitan": "Sedang", "sub": {
        1: "Perbandingan sederhana (2 objek)",
        2: "Perbandingan senilai (proporsi)",
        3: "Perbandingan berbalik nilai",
        4: "Skala pada peta & denah",
        5: "Harga jual, harga beli, untung & rugi",
        6: "Diskon (potongan harga) & pajak sederhana",
    }},
    13: {"materi": "Bangun Datar Lanjutan, Luas & Volume Kubus/Balok/Prisma", "kesulitan": "Sedang", "sub": {
        1: "Mengidentifikasi bangun datar (segitiga, trapesium, jajar genjang, layang-layang)",
        2: "Keliling segitiga, trapesium, jajar genjang",
        3: "Luas segitiga, trapesium, jajar genjang, layang-layang",
        4: "Mengidentifikasi bangun ruang (kubus, balok, prisma, limas, tabung)",
        5: "Volume kubus & balok",
        6: "Volume prisma segitiga",
    }},
    14: {"materi": "Jaring-jaring, Luas Permukaan & Volume Tabung", "kesulitan": "Sulit", "sub": {
        1: "Jaring-jaring kubus & balok",
        2: "Luas permukaan kubus & balok",
        3: "Luas permukaan prisma & tabung",
        4: "Volume tabung",
        5: "Sistem koordinat (kuadran I, titik koordinat)",
        6: "Soal cerita geometri (keliling, luas, volume)",
    }},
    15: {"materi": "Statistika, Mean/Median/Modus, Peluang", "kesulitan": "Sulit", "sub": {
        1: "Mengumpulkan & mengorganisasi data (tabel frekuensi)",
        2: "Menyajikan data dalam diagram garis & diagram lingkaran",
        3: "Mean, median, modus dari data tunggal",
        4: "Mean, median, modus dari data kelompok sederhana",
        5: "Pengenalan peluang (skala 0-1, kemungkinan)",
        6: "Soal cerita pemecahan masalah kompleks (4-5 langkah)",
    }},
    16: {"materi": "Bentuk Aljabar, PLSV", "kesulitan": "Sulit", "sub": {
        1: "Mengenal bentuk aljabar (suku, variabel, koefisien, konstanta)",
        2: "Operasi +/- bentuk aljabar (suku sejenis)",
        3: "Operasi x/: bentuk aljabar (monomial x monomial)",
        4: "Menyelesaikan PLSV sederhana (ax + b = c)",
        5: "Menyelesaikan PLSV dengan variabel di kedua ruas (ax+b=cx+d)",
        6: "Soal cerita PLSV (1 langkah)",
    }},
    17: {"materi": "Perbandingan & Trigonometri Dasar", "kesulitan": "Sulit", "sub": {
        1: "Perbandingan senilai lanjutan (3 variabel)",
        2: "Perbandingan berbalik nilai lanjutan (3 variabel)",
        3: "Skala pada peta & denah lanjutan (jarak sebenarnya)",
        4: "Perbandingan trigonometri dasar (sin, cos, tan)",
        5: "Soal cerita perbandingan (2-3 langkah)",
        6: "Soal cerita skala & perbandingan (kehidupan sehari-hari)",
    }},
    18: {"materi": "Himpunan & Diagram Venn", "kesulitan": "Sulit", "sub": {
        1: "Pengenalan himpunan (notasi, anggota, kardinalitas)",
        2: "Menyatakan himpunan (deskripsi, enumerasi, notasi pembentuk himpunan)",
        3: "Himpunan bagian & himpunan kuasa",
        4: "Irisan & gabungan himpunan",
        5: "Selisih & komplemen himpunan",
        6: "Soal cerita himpunan (diagram Venn, 2 himpunan)",
    }},
    19: {"materi": "Bilangan Berpangkat & Bentuk Akar", "kesulitan": "Sulit", "sub": {
        1: "Bilangan berpangkat bulat positif (a^n)",
        2: "Bilangan berpangkat bulat negatif & nol (a^-n, a^0)",
        3: "Sifat-sifat operasi bilangan berpangkat",
        4: "Bentuk akar sederhana (menyederhanakan akar)",
        5: "Operasi bentuk akar (+, -, x, :)",
        6: "Merasionalkan penyebut pecahan bentuk akar",
    }},
    20: {"materi": "PLSV, PtLSV, PLDV Dasar", "kesulitan": "Sulit", "sub": {
        1: "PLSV lanjutan (dengan pecahan & desimal)",
        2: "Pertidaksamaan linear satu variabel (>,<,>=,<=)",
        3: "Menyelesaikan PtLSV dengan operasi aljabar",
        4: "Menyelesaikan PtLSV dengan garis bilangan",
        5: "Persamaan linear dua variabel (PLDV) bentuk dasar",
        6: "Soal cerita PLSV & PtLSV (2 langkah)",
    }},
    21: {"materi": "SPLDV", "kesulitan": "Sulit", "sub": {
        1: "SPLDV metode substitusi",
        2: "SPLDV metode eliminasi",
        3: "SPLDV metode campuran",
        4: "SPLDV metode grafik",
        5: "Soal cerita SPLDV (2 variabel, 2 persamaan)",
        6: "Pengenalan SPLTV (tiga variabel)",
    }},
    22: {"materi": "Relasi & Fungsi", "kesulitan": "Sulit", "sub": {
        1: "Pengenalan relasi & fungsi (domain, kodomain, range)",
        2: "Menyatakan fungsi (diagram panah, kartesius, pasangan berurutan)",
        3: "Fungsi linear (f(x) = ax + b)",
        4: "Menentukan nilai fungsi (f(x) untuk x tertentu)",
        5: "Menentukan rumus fungsi dari grafik/tabel",
        6: "Soal cerita fungsi linear",
    }},
    23: {"materi": "Garis & Sudut", "kesulitan": "Sulit", "sub": {
        1: "Mengenal garis (lurus, sejajar, tegak lurus, berpotongan)",
        2: "Mengenal sudut (lancip, siku-siku, tumpul, lurus, refleks)",
        3: "Hubungan antar sudut (berpelurus, berpenyiku, bertolak belakang)",
        4: "Sudut pada dua garis sejajar dipotong garis lain",
        5: "Menghitung besar sudut pada bangun datar",
        6: "Soal cerita garis & sudut",
    }},
    24: {"materi": "Segitiga & Teorema Pythagoras", "kesulitan": "Sulit", "sub": {
        1: "Jenis-jenis segitiga",
        2: "Keliling & luas segitiga lanjutan",
        3: "Teorema Pythagoras (sisi miring, sisi siku-siku)",
        4: "Menentukan jenis segitiga dengan kebalikan Pythagoras",
        5: "Menyelesaikan masalah dengan teorema Pythagoras",
        6: "Soal cerita teorema Pythagoras",
    }},
    25: {"materi": "Segiempat & Segi-n", "kesulitan": "Sulit", "sub": {
        1: "Segiempat (persegi, persegi panjang, jajar genjang, belah ketupat, layang-layang, trapesium)",
        2: "Sifat-sifat segiempat (sisi, sudut, diagonal)",
        3: "Keliling & luas segiempat lanjutan",
        4: "Segi-n beraturan (segilima, segienam, segidelapan)",
        5: "Menghitung besar sudut dalam segi-n ((n-2)x180)",
        6: "Soal cerita bangun datar lanjutan (2-3 langkah)",
    }},
    26: {"materi": "Bangun Ruang Sisi Datar & Luas Permukaan", "kesulitan": "Sulit", "sub": {
        1: "Mengenal bangun ruang sisi datar",
        2: "Jaring-jaring bangun ruang",
        3: "Luas permukaan kubus & balok",
        4: "Luas permukaan prisma (tegak segitiga & segi-n)",
        5: "Luas permukaan limas (segi-n)",
        6: "Soal cerita luas permukaan bangun ruang",
    }},
    27: {"materi": "Volume Bangun Ruang", "kesulitan": "Sulit", "sub": {
        1: "Volume kubus & balok lanjutan (dengan variabel)",
        2: "Volume prisma (tegak segitiga & segi-n)",
        3: "Volume limas (segi-n)",
        4: "Volume tabung",
        5: "Volume kerucut",
        6: "Soal cerita volume bangun ruang (2-3 langkah)",
    }},
    28: {"materi": "Lingkaran", "kesulitan": "Sulit", "sub": {
        1: "Mengenal lingkaran (pusat, jari-jari, diameter, busur, dll)",
        2: "Keliling lingkaran (pi x d atau 2 x pi x r)",
        3: "Luas lingkaran (pi x r^2)",
        4: "Panjang busur & luas juring",
        5: "Hubungan sudut pusat & sudut keliling",
        6: "Soal cerita lingkaran (keliling, luas, busur, juring)",
    }},
    29: {"materi": "Statistika & Peluang", "kesulitan": "Sulit", "sub": {
        1: "Mengumpulkan data (populasi, sampel, sensus)",
        2: "Menyajikan data dalam tabel distribusi frekuensi",
        3: "Menyajikan data dalam diagram batang, garis, lingkaran",
        4: "Mean, median, modus dari data tunggal & kelompok",
        5: "Peluang (ruang sampel, kejadian, frekuensi harapan)",
        6: "Soal cerita statistika & peluang (2-3 langkah)",
    }},
    30: {"materi": "Trigonometri & Transformasi", "kesulitan": "Sulit", "sub": {
        1: "Perbandingan trigonometri (sin, cos, tan, sec, cosec, cot)",
        2: "Nilai trigonometri sudut istimewa (0,30,45,60,90)",
        3: "Menyelesaikan masalah dengan trigonometri (tinggi & jarak)",
        4: "Transformasi geometri (translasi, refleksi, rotasi, dilatasi)",
        5: "Komposisi transformasi (2 transformasi berurutan)",
        6: "Soal cerita trigonometri & transformasi (2-3 langkah)",
    }},
}


def get_harga(level: int) -> int:
    return HARGA[LEVELS[level]["kesulitan"]]


def get_sub_nama(level: int, sub: int) -> str:
    return LEVELS[level]["sub"][sub]


def get_materi(level: int) -> str:
    return LEVELS[level]["materi"]


def get_kesulitan(level: int) -> str:
    return LEVELS[level]["kesulitan"]


def next_sub(level: int, sub: int):
    """Return (next_level, next_sub) tuple, or None if it's the very last sub-level."""
    if sub < 6:
        return (level, sub + 1)
    if level < 30:
        return (level + 1, 1)
    return None


def all_level_options():
    """List of (level, sub) tuples in order, for UI dropdowns."""
    out = []
    for lvl in sorted(LEVELS.keys()):
        for sub in sorted(LEVELS[lvl]["sub"].keys()):
            out.append((lvl, sub))
    return out
