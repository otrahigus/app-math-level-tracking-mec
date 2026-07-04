# -*- coding: utf-8 -*-
"""
Bank Soal - Generator soal acak untuk setiap sub-level (0.1 s/d 30.6)
Setiap sub-level punya fungsi generator yang mengembalikan 5 soal + kunci jawaban.
Soal dibuat secara acak (random) setiap kali dipanggil, sehingga siswa yang
mengulang sub-level yang sama akan mendapat variasi soal yang berbeda.
"""
import random
import math
from fractions import Fraction

# ---------------------------------------------------------------------------
# HELPER UMUM
# ---------------------------------------------------------------------------

NAMA = ["Andi", "Budi", "Citra", "Dewi", "Eka", "Fajar", "Gita", "Hana",
        "Ivan", "Joko", "Kiki", "Lina", "Made", "Nia", "Oki", "Putri",
        "Rani", "Sari", "Toni", "Umi", "Vino", "Wati", "Yoga", "Zahra"]

BARANG = ["apel", "jeruk", "buku", "pensil", "kelereng", "permen",
          "roti", "telur", "bola", "mangga"]


def nama():
    return random.choice(NAMA)


def barang():
    return random.choice(BARANG)


def ri(a, b):
    return random.randint(a, b)


def q(soal, jawaban):
    return {"soal": soal, "jawaban": str(jawaban)}


def frac_str(fr: Fraction):
    if fr.denominator == 1:
        return str(fr.numerator)
    return f"{fr.numerator}/{fr.denominator}"


def simplify(n, d):
    g = math.gcd(n, d)
    return n // g, d // g


def rand_fraction(max_num=9, max_den=12, proper=True):
    d = ri(2, max_den)
    n = ri(1, d - 1) if proper else ri(1, max_num)
    return n, d


def check_answer(user_ans: str, correct_ans: str) -> bool:
    """Normalisasi & bandingkan jawaban siswa dengan kunci jawaban."""
    if user_ans is None:
        return False
    u = str(user_ans).strip().lower().replace(" ", "").replace(",", ".")
    c = str(correct_ans).strip().lower().replace(" ", "").replace(",", ".")
    if u == c:
        return True
    # coba bandingkan sebagai angka
    try:
        return abs(float(u) - float(c)) < 1e-6
    except ValueError:
        pass
    # coba bandingkan sebagai pecahan (mis. "3/4")
    try:
        fu = Fraction(u)
        fc = Fraction(c)
        return fu == fc
    except (ValueError, ZeroDivisionError):
        pass
    return False


def make_set(fn, n=5):
    """Panggil fn() sebanyak n kali untuk membuat n soal berbeda."""
    out = []
    tries = 0
    seen = set()
    while len(out) < n and tries < n * 20:
        tries += 1
        item = fn()
        key = item["soal"]
        if key in seen:
            continue
        seen.add(key)
        out.append(item)
    return out

# ---------------------------------------------------------------------------
# LEVEL 0 - Berhitung 1-50, +/- Dasar (Mudah)
# ---------------------------------------------------------------------------

def g_0_1():
    a = ri(1, 20)
    return q(f"Tuliskan bilangan setelah {a}.", a + 1)

def g_0_2():
    a, b = ri(1, 10), ri(1, 9)
    return q(f"{a} + {b} = ...", a + b)

def g_0_3():
    a = ri(5, 20)
    b = ri(1, a - 1)
    return q(f"{a} - {b} = ...", a - b)

def g_0_4():
    a = ri(20, 49)
    return q(f"Tuliskan bilangan sebelum {a + 1}.", a)

def g_0_5():
    a, b = ri(10, 30), ri(1, 19)
    return q(f"{a} + {b} = ...", a + b)

def g_0_6():
    a = ri(20, 50)
    b = ri(1, a - 1)
    return q(f"{a} - {b} = ...", a - b)

# ---------------------------------------------------------------------------
# LEVEL 1 - Berhitung 1-100, +/- Menyimpan/Meminjam (Mudah)
# ---------------------------------------------------------------------------

def g_1_1():
    a = ri(1, 99)
    return q(f"Bilangan setelah {a} adalah ...", a + 1)

def g_1_2():
    a = ri(10, 40)
    b = ri(1, max(1, 9 - (a % 10)))
    return q(f"{a} + {b} = ... (tanpa menyimpan)", a + b)

def g_1_3():
    a = ri(15, 89)
    b = ri(max(1, 10 - (a % 10)), 30)
    return q(f"{a} + {b} = ... (dengan menyimpan)", a + b)

def g_1_4():
    a = ri(30, 99)
    b = ri(1, a % 10 if a % 10 > 0 else 1)
    return q(f"{a} - {b} = ... (tanpa meminjam)", a - b)

def g_1_5():
    a = ri(30, 90)
    b = ri((a % 10) + 1, a - 1)
    return q(f"{a} - {b} = ... (dengan meminjam)", a - b)

def g_1_6():
    n1, n2 = nama(), nama()
    a, b = ri(20, 60), ri(5, 30)
    op = random.choice(["+", "-"])
    if op == "+":
        return q(f"{n1} punya {a} {barang()}. {n2} memberi {b} lagi. "
                  f"Berapa jumlah {barang()} {n1} sekarang?", a + b)
    b = min(b, a - 1)
    return q(f"{n1} punya {a} {barang()}. {n1} memberi {b} kepada {n2}. "
              f"Berapa sisa {barang()} {n1}?", a - b)

# ---------------------------------------------------------------------------
# LEVEL 2 - Perkalian & Pembagian 1-10 (Mudah)
# ---------------------------------------------------------------------------

def g_2_1():
    a, b = ri(1, 5), ri(1, 5)
    return q(f"{a} x {b} = ...", a * b)

def g_2_2():
    b = ri(1, 5)
    hasil = ri(1, 10)
    a = b * hasil
    return q(f"{a} : {b} = ...", hasil)

def g_2_3():
    a, b = ri(6, 10), ri(6, 10)
    return q(f"{a} x {b} = ...", a * b)

def g_2_4():
    b = ri(6, 10)
    hasil = ri(1, 10)
    a = b * hasil
    return q(f"{a} : {b} = ...", hasil)

def g_2_5():
    n1 = nama()
    op = random.choice(["kali", "bagi"])
    if op == "kali":
        a, b = ri(2, 9), ri(2, 9)
        return q(f"{n1} membeli {a} kotak {barang()}. Setiap kotak berisi {b} buah. "
                  f"Berapa total {barang()} yang dibeli {n1}?", a * b)
    b = ri(2, 9)
    hasil = ri(2, 9)
    a = b * hasil
    return q(f"{n1} punya {a} {barang()} yang akan dibagi rata ke {b} teman. "
              f"Berapa {barang()} yang diterima setiap teman?", hasil)

def g_2_6():
    a, b, c = ri(5, 20), ri(1, 10), ri(1, 10)
    op1, op2 = random.choice(["+", "-"]), random.choice(["+", "-"])
    expr = f"{a} {op1} {b} {op2} {c}"
    hasil = eval(expr)
    return q(f"{expr} = ...", hasil)

# ---------------------------------------------------------------------------
# LEVEL 3 - Bersusun Ratusan, Nilai Tempat, Membandingkan (Mudah)
# ---------------------------------------------------------------------------

def g_3_1():
    a, b = ri(150, 800), ri(100, 199)
    return q(f"{a} + {b} = ... (kerjakan bersusun)", a + b)

def g_3_2():
    a = ri(300, 999)
    b = ri(100, a - 1)
    return q(f"{a} - {b} = ... (kerjakan bersusun)", a - b)

def g_3_3():
    a = ri(1000, 9999)
    s = str(a)
    digit = int(s[-3])
    nilai = digit * 100
    return q(f"Nilai tempat angka {digit} pada bilangan {a} (posisi ratusan) adalah ...", nilai)

def g_3_4():
    a, b = ri(100, 999), ri(100, 999)
    while a == b:
        b = ri(100, 999)
    tanda = ">" if a > b else "<"
    return q(f"Isilah dengan >, <, atau =: {a} ... {b}", tanda)

def g_3_5():
    a, b = ri(10, 49), ri(2, 9)
    return q(f"{a} x {b} = ... (kerjakan bersusun)", a * b)

def g_3_6():
    n1 = nama()
    a, b, c = ri(50, 200), ri(2, 5), ri(5, 20)
    total = a * b - c
    return q(f"{n1} membeli {b} dus {barang()}, setiap dus berisi {a} buah. "
              f"Setelah itu {c} {barang()} rusak dan dibuang. "
              f"Berapa sisa {barang()} milik {n1}?", total)

# ---------------------------------------------------------------------------
# LEVEL 4 - Pecahan Dasar, +/- Penyebut Sama (Mudah)
# ---------------------------------------------------------------------------

def g_4_1():
    d = random.choice([2, 3, 4])
    n = ri(1, d - 1)
    return q(f"Sebuah kue dipotong menjadi {d} bagian sama besar, {n} bagian dimakan. "
              f"Berapa bagian pecahan kue yang dimakan? (bentuk pecahan)", f"{n}/{d}")

def g_4_2():
    d = random.choice([3, 4, 5])
    n1v = ri(1, d - 1)
    n2v = ri(1, d - 1)
    while n1v == n2v:
        n2v = ri(1, d - 1)
    tanda = ">" if n1v > n2v else "<"
    return q(f"Bandingkan pecahan berikut: {n1v}/{d} ... {n2v}/{d}", tanda)

def g_4_3():
    d = ri(4, 10)
    n1v = ri(1, d - 2)
    n2v = ri(1, d - n1v - 1) if d - n1v - 1 >= 1 else 1
    return q(f"{n1v}/{d} + {n2v}/{d} = ...", frac_str(Fraction(n1v + n2v, d)))

def g_4_4():
    d = ri(4, 10)
    n1v = ri(2, d - 1)
    n2v = ri(1, n1v - 1)
    return q(f"{n1v}/{d} - {n2v}/{d} = ...", frac_str(Fraction(n1v - n2v, d)))

def g_4_5():
    n = ri(1, 9)
    return q(f"Ubah pecahan {n}/10 ke bentuk desimal.", f"0.{n}")

def g_4_6():
    n1 = nama()
    d = random.choice([4, 5])
    nfrac = ri(1, d - 1)
    total = ri(20, 40)
    while (total * nfrac) % d != 0:
        total = ri(20, 40)
    bagian = total * nfrac // d
    return q(f"{n1} punya {total} {barang()}. Sebanyak {nfrac}/{d} bagian diberikan ke temannya. "
              f"Berapa {barang()} yang diberikan?", bagian)

# ---------------------------------------------------------------------------
# LEVEL 5 - Perkalian 2x2 Digit, Pembagian 2:1 Digit (Mudah)
# ---------------------------------------------------------------------------

def g_5_1():
    a, b = ri(11, 50), ri(11, 30)
    return q(f"{a} x {b} = ... (kerjakan bersusun)", a * b)

def g_5_2():
    b = ri(2, 9)
    hasil = ri(11, 30)
    a = b * hasil
    return q(f"{a} : {b} = ... (tanpa sisa)", hasil)

def g_5_3():
    pilihan = {"1/2": "0.5", "1/4": "0.25", "3/4": "0.75", "1/5": "0.2"}
    p = random.choice(list(pilihan.keys()))
    return q(f"Ubah pecahan {p} ke bentuk desimal.", pilihan[p])

def g_5_4():
    a, b, c = ri(2, 15), ri(2, 10), ri(2, 6)
    expr = f"({a} + {b}) x {c}"
    return q(f"{expr} = ...", (a + b) * c)

def g_5_5():
    n1 = nama()
    a, b, c, d = ri(5, 15), ri(2, 6), ri(3, 10), ri(2, 8)
    total = a * b + c * d
    return q(f"{n1} membeli {b} bungkus permen isi {a}, lalu membeli lagi {d} bungkus coklat isi {c}. "
              f"Berapa total semua barang yang dibeli {n1}?", total)

def g_5_6():
    persen = random.choice([10, 25, 50])
    total = random.choice([20, 40, 60, 80, 100, 200])
    hasil = total * persen // 100
    return q(f"{persen}% dari {total} adalah ...", hasil)

# ---------------------------------------------------------------------------
# LEVEL 6 - Menyederhanakan Pecahan, +/- Penyebut Beda (kelipatan) (Sedang)
# ---------------------------------------------------------------------------

def g_6_1():
    g = ri(2, 6)
    n1v, d1 = ri(1, 5), ri(2, 6)
    while n1v >= d1:
        n1v = ri(1, d1 - 1)
    n, d = n1v * g, d1 * g
    sn, sd = simplify(n, d)
    return q(f"Sederhanakan pecahan {n}/{d} dengan FPB.", f"{sn}/{sd}")

def g_6_2():
    d1 = ri(2, 4)
    d2 = d1 * ri(2, 3)
    n1v, n2v = ri(1, d1 - 1), ri(1, d2 - 1)
    hasil = Fraction(n1v, d1) + Fraction(n2v, d2)
    return q(f"{n1v}/{d1} + {n2v}/{d2} = ... (penyebut kelipatan)", frac_str(hasil))

def g_6_3():
    d1 = ri(2, 4)
    d2 = d1 * ri(2, 3)
    n1v, n2v = ri(1, d1 - 1), ri(1, d2 - 1)
    a, b = Fraction(n1v, d1), Fraction(n2v, d2)
    if a < b:
        a, b = b, a
    hasil = a - b
    return q(f"{a.numerator}/{a.denominator} - {b.numerator}/{b.denominator} = ... (penyebut kelipatan)", frac_str(hasil))

def g_6_4():
    d = ri(3, 8)
    n1v = ri(1, d - 1)
    bil = ri(2, 6)
    hasil = Fraction(n1v, d) * bil
    return q(f"{n1v}/{d} x {bil} = ...", frac_str(hasil))

def g_6_5():
    d = ri(2, 6)
    n1v = ri(1, d - 1)
    bil = ri(2, 5)
    hasil = Fraction(n1v, d) / bil
    return q(f"{n1v}/{d} : {bil} = ...", frac_str(hasil))

def g_6_6():
    angka = random.choice([1, 2])
    if angka == 1:
        d_ = ri(1, 9)
        n1v, d1v = simplify(d_, 10)
        return q(f"Ubah desimal 0.{d_} ke bentuk pecahan paling sederhana.", f"{n1v}/{d1v}")
    dd = ri(1, 99)
    n1v, d1v = simplify(dd, 100)
    dstr = f"0.{dd:02d}"
    return q(f"Ubah desimal {dstr} ke bentuk pecahan paling sederhana.", f"{n1v}/{d1v}")

# ---------------------------------------------------------------------------
# LEVEL 7 - Bilangan Bulat Positif/Negatif (Sedang)
# ---------------------------------------------------------------------------

def g_7_1():
    a, b = ri(-20, 20), ri(-20, 20)
    return q(f"{a} + ({b}) = ...", a + b)

def g_7_2():
    a, b = ri(-20, 20), ri(-20, 20)
    return q(f"{a} - ({b}) = ...", a - b)

def g_7_3():
    a, b = random.choice([-1, 1]) * ri(2, 12), random.choice([-1, 1]) * ri(2, 12)
    op = random.choice(["x", ":"])
    if op == "x":
        return q(f"{a} x {b} = ...", a * b)
    hasil = ri(2, 10) * random.choice([-1, 1])
    a = b * hasil
    return q(f"{a} : {b} = ...", hasil)

def g_7_4():
    a, b, c = ri(-15, 15), ri(-15, 15), ri(-10, 10)
    op1, op2 = random.choice(["+", "-"]), random.choice(["+", "-"])
    expr = f"{a} {op1} {b} {op2} {c}"
    return q(f"{expr} = ...", eval(expr))

def g_7_5():
    a, b, c = ri(-10, 10), ri(-10, 10), ri(2, 5)
    expr = f"({a} + {b}) x {c}"
    return q(f"{expr} = ...", (a + b) * c)

def g_7_6():
    n1 = nama()
    konteks = random.choice(["suhu", "utang", "ketinggian"])
    a, b = ri(-10, 10), ri(1, 15)
    if konteks == "suhu":
        return q(f"Suhu di suatu kota pagi hari {a} derajat C. Siang hari naik {b} derajat. "
                  f"Berapa suhu siang hari?", a + b)
    if konteks == "utang":
        return q(f"{n1} memiliki utang Rp{abs(a)*1000} (ditulis -{abs(a)}). "
                  f"{n1} membayar {b} (dalam ribuan). Berapa sisa utang {n1} (dalam ribuan, boleh negatif)?", -abs(a) + b)
    return q(f"Sebuah kapal selam berada {abs(a)} meter di bawah permukaan laut (ditulis -{abs(a)}). "
              f"Kapal naik {b} meter. Berapa posisi kapal sekarang (meter, boleh negatif)?", -abs(a) + b)

# ---------------------------------------------------------------------------
# LEVEL 8 - Satuan & Pengukuran (Sedang)
# ---------------------------------------------------------------------------

def g_8_1():
    a = ri(1, 20)
    return q(f"{a} km = ... m", a * 1000)

def g_8_2():
    a = ri(1, 20)
    return q(f"{a} kg = ... g", a * 1000)

def g_8_3():
    a = ri(1, 10)
    return q(f"{a} jam = ... menit", a * 60)

def g_8_4():
    a = ri(1, 20)
    return q(f"{a} liter = ... ml", a * 1000)

def g_8_5():
    p, l = ri(4, 20), ri(3, 15)
    tipe = random.choice(["keliling", "luas"])
    if tipe == "keliling":
        return q(f"Sebuah persegi panjang berukuran panjang {p} cm dan lebar {l} cm. "
                  f"Berapa kelilingnya (cm)?", 2 * (p + l))
    return q(f"Sebuah persegi panjang berukuran panjang {p} cm dan lebar {l} cm. "
              f"Berapa luasnya (cm persegi)?", p * l)

def g_8_6():
    n1 = nama()
    a, b = ri(2, 5), ri(200, 900)
    total_menit = a * 60 + b // 10
    return q(f"{n1} berjalan kaki selama {a} jam, lalu istirahat, kemudian berjalan lagi selama "
              f"{b // 10} menit. Berapa total waktu {n1} berjalan (dalam menit)?", total_menit)

# ---------------------------------------------------------------------------
# LEVEL 9 - Pola Bilangan, Variabel, Persamaan Sederhana (Sedang)
# ---------------------------------------------------------------------------

def g_9_1():
    start = ri(1, 10)
    step = ri(2, 6)
    op = random.choice(["+", "x"])
    if op == "+":
        seq = [start + step * i for i in range(4)]
        jawaban = start + step * 4
    else:
        step = ri(2, 3)
        seq = [start * (step ** i) for i in range(4)]
        jawaban = start * (step ** 4)
    seq_str = ", ".join(str(x) for x in seq)
    return q(f"Tentukan bilangan selanjutnya dari pola: {seq_str}, ...", jawaban)

def g_9_2():
    a, b = ri(2, 9), ri(1, 9)
    x = ri(1, 9)
    return q(f"Jika x = {x}, berapa nilai dari {a}x + {b}?", a * x + b)

def g_9_3():
    x = ri(1, 20)
    a = ri(1, 15)
    op = random.choice(["+", "-"])
    if op == "+":
        b = x + a
        return q(f"Tentukan nilai x: x + {a} = {b}", x)
    b = x - a
    return q(f"Tentukan nilai x: x - {a} = {b}", x)

def g_9_4():
    x = ri(2, 12)
    a = ri(2, 8)
    op = random.choice(["x", ":"])
    if op == "x":
        b = a * x
        return q(f"Tentukan nilai x: {a} x x = {b}", x)
    b = x
    hasil = a * x
    return q(f"Tentukan nilai x: x : {a} = {b}", hasil)

def g_9_5():
    data = [ri(2, 20) for _ in range(4)]
    idx = ri(0, 3)
    return q(f"Diagram batang menunjukkan data: A={data[0]}, B={data[1]}, C={data[2]}, D={data[3]}. "
              f"Berapa nilai data ke-{idx+1} (urutan A,B,C,D)?", data[idx])

def g_9_6():
    data = [ri(2, 10) for _ in range(5)]
    mean_val = sum(data) / len(data)
    data_str = ", ".join(str(x) for x in data)
    ans = round(mean_val, 2)
    if ans == int(ans):
        ans = int(ans)
    return q(f"Tentukan mean (rata-rata) dari data: {data_str}", ans)

# ---------------------------------------------------------------------------
# LEVEL 10 - Nilai Tempat sampai 10.000 (Sedang)
# ---------------------------------------------------------------------------

def g_10_1():
    a = ri(1000, 9999)
    s = str(a)
    digit = int(s[-4])
    return q(f"Nilai tempat angka {digit} pada bilangan {a} (posisi ribuan) adalah ...", digit * 1000)

def g_10_2():
    a, b = ri(1000, 9999), ri(1000, 9999)
    while a == b:
        b = ri(1000, 9999)
    tanda = ">" if a > b else "<"
    return q(f"Isilah dengan >, <, atau =: {a} ... {b}", tanda)

def g_10_3():
    a, b = ri(1000, 8000), ri(500, 1999)
    op = random.choice(["+", "-"])
    if op == "+":
        return q(f"{a} + {b} = ... (kerjakan bersusun)", a + b)
    a2 = max(a, b + 1)
    return q(f"{a2} - {b} = ... (kerjakan bersusun)", a2 - b)

def g_10_4():
    a, b = ri(100, 300), ri(2, 9)
    return q(f"{a} x {b} = ... (kerjakan bersusun)", a * b)

def g_10_5():
    b = ri(2, 9)
    hasil = ri(100, 300)
    a = b * hasil
    return q(f"{a} : {b} = ... (tanpa sisa)", hasil)

def g_10_6():
    n1 = nama()
    a, b, c = ri(1000, 3000), ri(2, 5), ri(200, 900)
    total = a * b - c
    return q(f"Sebuah toko memiliki {b} dus barang, setiap dus berisi {a} unit. "
              f"Sebanyak {c} unit rusak. Berapa sisa unit barang yang baik?", total)

# ---------------------------------------------------------------------------
# LEVEL 11 - +/- Pecahan Penyebut Beda, Tidak Kelipatan (Sedang)
# ---------------------------------------------------------------------------

def g_11_1():
    d1, d2 = ri(3, 7), ri(3, 7)
    while d2 % d1 == 0 or d1 % d2 == 0 or d1 == d2:
        d2 = ri(3, 7)
    n1v, n2v = ri(1, d1 - 1), ri(1, d2 - 1)
    hasil = Fraction(n1v, d1) + Fraction(n2v, d2)
    return q(f"{n1v}/{d1} + {n2v}/{d2} = ...", frac_str(hasil))

def g_11_2():
    d1, d2 = ri(3, 7), ri(3, 7)
    while d2 % d1 == 0 or d1 % d2 == 0 or d1 == d2:
        d2 = ri(3, 7)
    n1v, n2v = ri(1, d1 - 1), ri(1, d2 - 1)
    a, b = Fraction(n1v, d1), Fraction(n2v, d2)
    if a < b:
        a, b = b, a
    return q(f"{a.numerator}/{a.denominator} - {b.numerator}/{b.denominator} = ...", frac_str(a - b))

def g_11_3():
    n1v, d1 = ri(1, 8), ri(2, 9)
    n2v, d2 = ri(1, 8), ri(2, 9)
    hasil = Fraction(n1v, d1) * Fraction(n2v, d2)
    return q(f"{n1v}/{d1} x {n2v}/{d2} = ...", frac_str(hasil))

def g_11_4():
    n1v, d1 = ri(1, 8), ri(2, 9)
    n2v, d2 = ri(1, 8), ri(2, 9)
    hasil = Fraction(n1v, d1) / Fraction(n2v, d2)
    return q(f"{n1v}/{d1} : {n2v}/{d2} = ...", frac_str(hasil))

def g_11_5():
    tipe = random.choice(["ke_biasa", "ke_campuran"])
    if tipe == "ke_biasa":
        whole = ri(1, 5)
        d = ri(2, 8)
        n1v = ri(1, d - 1)
        return q(f"Ubah pecahan campuran {whole} {n1v}/{d} menjadi pecahan biasa.",
                  f"{whole*d+n1v}/{d}")
    d = ri(2, 8)
    n1v = ri(d + 1, d * 4)
    whole, sisa = divmod(n1v, d)
    return q(f"Ubah pecahan biasa {n1v}/{d} menjadi pecahan campuran.",
              f"{whole} {sisa}/{d}" if sisa else str(whole))

def g_11_6():
    n1 = nama()
    d1, d2 = 4, 8
    n1v, n2v = ri(1, 3), ri(1, 7)
    a, b = Fraction(n1v, d1), Fraction(n2v, d2)
    hasil = a + b
    return q(f"{n1} makan {n1v}/{d1} bagian kue dan adiknya makan {n2v}/{d2} bagian kue yang sama. "
              f"Berapa bagian kue yang sudah dimakan? (pecahan sederhana)", frac_str(hasil))

# ---------------------------------------------------------------------------
# LEVEL 12 - Perbandingan, Skala, Untung/Rugi, Diskon (Sedang)
# ---------------------------------------------------------------------------

def g_12_1():
    a, b = ri(2, 10), ri(2, 10)
    g_ = math.gcd(a, b)
    return q(f"Sederhanakan perbandingan {a}:{b}", f"{a//g_}:{b//g_}")

def g_12_2():
    rasio_a, rasio_b = ri(2, 6), ri(2, 6)
    while rasio_a == rasio_b:
        rasio_b = ri(2, 6)
    faktor = ri(2, 8)
    a1, b1 = rasio_a, rasio_b
    a2 = a1 * faktor
    b2 = b1 * faktor
    return q(f"Jika perbandingan a:b = {a1}:{b1}, dan a = {a2}, berapa nilai b?", b2)

def g_12_3():
    pekerja1, hari1 = ri(2, 6), ri(6, 20)
    pekerja2 = ri(2, 10)
    while pekerja2 == pekerja1:
        pekerja2 = ri(2, 10)
    hari2 = pekerja1 * hari1 // pekerja2
    while (pekerja1 * hari1) % pekerja2 != 0:
        pekerja2 = ri(2, 10)
        hari2 = pekerja1 * hari1 // pekerja2 if pekerja2 else 1
        if (pekerja1*hari1) % pekerja2 == 0:
            break
    hari2 = (pekerja1 * hari1) // pekerja2
    return q(f"Sebuah proyek selesai dalam {hari1} hari oleh {pekerja1} pekerja. "
              f"Jika dikerjakan oleh {pekerja2} pekerja, berapa hari yang dibutuhkan?", hari2)

def g_12_4():
    skala = random.choice([100, 200, 500, 1000])
    jarak_peta = ri(2, 20)
    jarak_asli_cm = jarak_peta * skala
    jarak_asli_m = jarak_asli_cm / 100
    return q(f"Skala peta 1:{skala}. Jarak pada peta {jarak_peta} cm. "
              f"Berapa jarak sebenarnya (dalam meter)?", int(jarak_asli_m) if jarak_asli_m == int(jarak_asli_m) else jarak_asli_m)

def g_12_5():
    beli = ri(10, 50) * 1000
    untung = ri(2, 15) * 1000
    jual = beli + untung
    return q(f"Seorang pedagang membeli barang seharga Rp{beli} dan menjualnya seharga Rp{jual}. "
              f"Berapa untung yang didapat (Rp)?", jual - beli)

def g_12_6():
    harga = ri(20, 200) * 1000
    diskon = random.choice([10, 15, 20, 25])
    potongan = harga * diskon // 100
    return q(f"Harga sebuah baju Rp{harga} mendapat diskon {diskon}%. "
              f"Berapa harga yang harus dibayar setelah diskon (Rp)?", harga - potongan)

# ---------------------------------------------------------------------------
# LEVEL 13 - Bangun Datar Lanjutan, Luas & Volume Kubus/Balok/Prisma (Sedang)
# ---------------------------------------------------------------------------

def g_13_1():
    bangun = random.choice(["segitiga", "trapesium", "jajar genjang", "layang-layang"])
    ciri = {
        "segitiga": "memiliki 3 sisi dan 3 sudut",
        "trapesium": "memiliki sepasang sisi sejajar yang tidak sama panjang",
        "jajar genjang": "memiliki dua pasang sisi sejajar sama panjang",
        "layang-layang": "memiliki dua pasang sisi berdekatan sama panjang",
    }
    return q(f"Bangun datar yang {ciri[bangun]} disebut ...", bangun)

def g_13_2():
    a, b, c = ri(4, 15), ri(4, 15), ri(4, 15)
    return q(f"Sebuah segitiga memiliki sisi {a} cm, {b} cm, dan {c} cm. Berapa kelilingnya (cm)?", a + b + c)

def g_13_3():
    alas, tinggi = ri(4, 20), ri(3, 15)
    bangun = random.choice(["segitiga", "jajar genjang"])
    if bangun == "segitiga":
        return q(f"Segitiga memiliki alas {alas} cm dan tinggi {tinggi} cm. Berapa luasnya (cm persegi)?",
                  alas * tinggi / 2)
    return q(f"Jajar genjang memiliki alas {alas} cm dan tinggi {tinggi} cm. Berapa luasnya (cm persegi)?",
              alas * tinggi)

def g_13_4():
    bangun = random.choice(["kubus", "balok", "prisma", "limas", "tabung"])
    ciri = {
        "kubus": "memiliki 6 sisi berbentuk persegi yang sama besar",
        "balok": "memiliki 6 sisi berbentuk persegi panjang",
        "prisma": "memiliki dua alas kongruen sejajar dan sisi tegak berbentuk persegi panjang",
        "limas": "memiliki 1 alas dan sisi tegak berbentuk segitiga yang bertemu di satu titik puncak",
        "tabung": "memiliki alas dan tutup berbentuk lingkaran dengan selimut melengkung",
    }
    return q(f"Bangun ruang yang {ciri[bangun]} disebut ...", bangun)

def g_13_5():
    s = ri(3, 12)
    bangun = random.choice(["kubus", "balok"])
    if bangun == "kubus":
        return q(f"Sebuah kubus memiliki panjang rusuk {s} cm. Berapa volumenya (cm kubik)?", s ** 3)
    p, l, t = ri(3, 15), ri(3, 12), ri(3, 10)
    return q(f"Sebuah balok berukuran p={p} cm, l={l} cm, t={t} cm. Berapa volumenya (cm kubik)?", p * l * t)

def g_13_6():
    alas, tinggi_segitiga, tinggi_prisma = ri(4, 12), ri(3, 10), ri(4, 15)
    luas_alas = alas * tinggi_segitiga / 2
    return q(f"Prisma segitiga memiliki alas segitiga dengan alas {alas} cm, tinggi segitiga {tinggi_segitiga} cm, "
              f"dan tinggi prisma {tinggi_prisma} cm. Berapa volumenya (cm kubik)?", luas_alas * tinggi_prisma)

# ---------------------------------------------------------------------------
# LEVEL 14 - Jaring-jaring, Luas Permukaan & Volume Tabung (Sulit)
# ---------------------------------------------------------------------------

def g_14_1():
    bangun = random.choice(["kubus", "balok"])
    n_sisi = 6
    return q(f"Berapa jumlah sisi persegi/persegi panjang pada jaring-jaring {bangun}?", n_sisi)

def g_14_2():
    s = ri(3, 12)
    bangun = random.choice(["kubus", "balok"])
    if bangun == "kubus":
        return q(f"Kubus memiliki rusuk {s} cm. Berapa luas permukaannya (cm persegi)?", 6 * s * s)
    p, l, t = ri(3, 12), ri(3, 10), ri(3, 8)
    lp = 2 * (p*l + p*t + l*t)
    return q(f"Balok berukuran p={p} cm, l={l} cm, t={t} cm. Berapa luas permukaannya (cm persegi)?", lp)

def g_14_3():
    r, t = ri(3, 10), ri(5, 20)
    hasil = round(2 * 3.14 * r * (r + t), 2)
    return q(f"Tabung berjari-jari {r} cm dan tinggi {t} cm (gunakan pi=3.14). "
              f"Berapa luas permukaannya (cm persegi)?", hasil)

def g_14_4():
    r, t = ri(3, 10), ri(5, 20)
    hasil = round(3.14 * r * r * t, 2)
    return q(f"Tabung berjari-jari {r} cm dan tinggi {t} cm (gunakan pi=3.14). "
              f"Berapa volumenya (cm kubik)?", hasil)

def g_14_5():
    x, y = ri(-10, 10), ri(-10, 10)
    kuadran = "I" if x > 0 and y > 0 else ("II" if x < 0 and y > 0 else ("III" if x < 0 and y < 0 else "IV"))
    return q(f"Titik koordinat ({x}, {y}) berada pada kuadran ...", kuadran)

def g_14_6():
    s = ri(4, 15)
    return q(f"Sebuah kolam berbentuk kubus dengan rusuk {s} m akan diisi air penuh. "
              f"Berapa liter air yang dibutuhkan? (1 m kubik = 1000 liter)", s**3 * 1000)

# ---------------------------------------------------------------------------
# LEVEL 15 - Statistika, Mean/Median/Modus, Peluang (Sulit)
# ---------------------------------------------------------------------------

def g_15_1():
    data = [random.choice(["A", "A", "B", "C", "B", "A"]) for _ in range(10)]
    target = random.choice(["A", "B", "C"])
    return q(f"Data nilai ujian siswa: {', '.join(data)}. Berapa frekuensi kemunculan {target}?", data.count(target))

def g_15_2():
    total = ri(50, 200)
    persen = random.choice([25, 50, 20])
    return q(f"Sebuah diagram lingkaran menunjukkan total data {total} siswa, kategori 'suka matematika' "
              f"sebesar {persen}%. Berapa jumlah siswa yang suka matematika?", total * persen // 100)

def g_15_3():
    data = sorted([ri(1, 20) for _ in range(5)])
    return q(f"Data: {', '.join(map(str,data))}. Tentukan median dari data tersebut.", data[2])

def g_15_4():
    data = [ri(1, 10) for _ in range(6)]
    mean_val = sum(data) / len(data)
    ans = round(mean_val, 2)
    return q(f"Data kelompok: {', '.join(map(str,data))}. Tentukan mean (rata-rata) data tersebut.", ans)

def g_15_5():
    total = random.choice([2, 4, 6, 8, 10])
    favorit = ri(1, total)
    frac = Fraction(favorit, total)
    return q(f"Sebuah dadu memiliki {total} sisi bernomor 1-{total}. "
              f"Berapa peluang muncul angka kurang dari atau sama dengan {favorit} (bentuk pecahan sederhana)?",
              frac_str(frac))

def g_15_6():
    n1 = nama()
    harga_a, jumlah_a = ri(2,8)*1000, ri(2,5)
    harga_b, jumlah_b = ri(2,8)*1000, ri(2,5)
    uang = (harga_a*jumlah_a + harga_b*jumlah_b) + ri(5,20)*1000
    kembalian = uang - (harga_a*jumlah_a + harga_b*jumlah_b)
    return q(f"{n1} membeli {jumlah_a} buku seharga Rp{harga_a} per buku dan {jumlah_b} pensil seharga Rp{harga_b} "
              f"per pensil. {n1} membayar dengan uang Rp{uang}. Berapa uang kembalian yang diterima {n1}?", kembalian)

# ---------------------------------------------------------------------------
# LEVEL 16 - Bentuk Aljabar, PLSV (Sulit)
# ---------------------------------------------------------------------------

def g_16_1():
    a, b = ri(2, 9), ri(1, 9)
    return q(f"Pada bentuk aljabar {a}x + {b}, tentukan koefisien dari x.", a)

def g_16_2():
    a, b, c = ri(2, 9), ri(2, 9), ri(1, 9)
    return q(f"Sederhanakan: {a}x + {b}x + {c} = ...", f"{a+b}x + {c}")

def g_16_3():
    a, b = ri(2, 6), ri(2, 6)
    return q(f"Sederhanakan: {a}x . {b}x = ...", f"{a*b}x^2")

def g_16_4():
    x = ri(1, 15)
    a = ri(2, 8)
    b = ri(1, 10)
    c = a * x + b
    return q(f"Tentukan nilai x dari: {a}x + {b} = {c}", x)

def g_16_5():
    x = ri(1, 10)
    a, c = ri(3, 8), ri(1, 5)
    b = ri(1, 15)
    d = c * x + (a * x + b - c * x)
    d = a * x + b - c * x
    return q(f"Tentukan nilai x dari: {a}x + {b} = {c}x + {d}", x)

def g_16_6():
    n1 = nama()
    x = ri(2, 15)
    a, b = ri(2, 6), ri(1, 10)
    total = a * x + b
    return q(f"Umur {n1} adalah x tahun. Jika {a} kali umur {n1} ditambah {b} adalah {total}, "
              f"berapa umur {n1}?", x)

# ---------------------------------------------------------------------------
# LEVEL 17 - Perbandingan & Trigonometri Dasar (Sulit)
# ---------------------------------------------------------------------------

def g_17_1():
    a, b, c = ri(2, 5), ri(2, 5), ri(2, 5)
    faktor = ri(2, 6)
    return q(f"Perbandingan a:b:c = {a}:{b}:{c}. Jika a = {a*faktor}, berapa nilai b dan c? "
              f"(format jawaban: b,c)", f"{b*faktor},{c*faktor}")

def g_17_2():
    p1, h1 = ri(3, 8), ri(10, 30)
    total = p1 * h1
    kandidat = [d for d in range(2, 11) if d != p1 and total % d == 0]
    p2 = random.choice(kandidat) if kandidat else p1 + 1
    while total % p2 != 0:
        p2 += 1
    h2 = total // p2
    return q(f"{p1} mesin menyelesaikan pekerjaan dalam {h1} hari. Berapa hari dibutuhkan oleh {p2} mesin?", h2)

def g_17_3():
    skala = random.choice([250, 500, 1000, 2500])
    jarak_peta = ri(3, 25)
    jarak_asli_km = (jarak_peta * skala) / 100000
    return q(f"Skala peta 1:{skala}. Jarak pada peta {jarak_peta} cm. "
              f"Berapa jarak sebenarnya (dalam km)?", jarak_asli_km)

def g_17_4():
    sudut = random.choice([30, 45, 60])
    nilai = {30: {"sin": "1/2", "cos": "1/2 akar3", "tan": "1/3 akar3"},
             45: {"sin": "1/2 akar2", "cos": "1/2 akar2", "tan": "1"},
             60: {"sin": "1/2 akar3", "cos": "1/2", "tan": "akar3"}}
    fungsi = random.choice(["sin", "cos", "tan"])
    return q(f"Tentukan nilai {fungsi} {sudut} derajat.", nilai[sudut][fungsi])

def g_17_5():
    n1 = nama()
    resep_a, resep_b = ri(2, 5), ri(2, 5)
    faktor = ri(2, 6)
    return q(f"Resep kue membutuhkan perbandingan tepung:gula = {resep_a}:{resep_b}. "
              f"Jika {n1} menggunakan {resep_a*faktor} kg tepung, berapa kg gula yang dibutuhkan?", resep_b*faktor)

def g_17_6():
    peta_cm = ri(4, 15)
    skala = random.choice([100, 200, 500])
    asli_m = peta_cm * skala / 100
    return q(f"Jarak dua kota pada denah adalah {peta_cm} cm dengan skala 1:{skala}. "
              f"Berapa jarak sebenarnya (dalam meter)?", asli_m)

# ---------------------------------------------------------------------------
# LEVEL 18 - Himpunan & Diagram Venn (Sulit)
# ---------------------------------------------------------------------------

def g_18_1():
    n = ri(3, 8)
    anggota = random.sample(range(1, 20), n)
    return q(f"Himpunan A = {{{', '.join(map(str, anggota))}}}. Berapa kardinalitas (n(A)) himpunan A?", n)

def g_18_2():
    anggota = sorted(random.sample(range(1, 10), 4))
    return q(f"Nyatakan himpunan bilangan asli kurang dari 10 yang merupakan anggota {{{', '.join(map(str,anggota))}}} "
              f"dalam notasi enumerasi (daftar anggota, format: {{a,b,c,d}})",
              "{" + ",".join(map(str, anggota)) + "}")

def g_18_3():
    n = ri(2, 5)
    return q(f"Jika himpunan A memiliki {n} anggota, berapa banyak himpunan bagian (kuasa) dari A?", 2 ** n)

def g_18_4():
    a = set(random.sample(range(1, 15), 5))
    b = set(random.sample(range(1, 15), 5))
    op = random.choice(["irisan", "gabungan"])
    a_list = sorted(a)
    b_list = sorted(b)
    if op == "irisan":
        hasil = sorted(a & b)
    else:
        hasil = sorted(a | b)
    hasil_str = "{" + ",".join(map(str, hasil)) + "}"
    return q(f"A = {{{','.join(map(str,a_list))}}}, B = {{{','.join(map(str,b_list))}}}. "
              f"Tentukan {op} A dan B (format: {{a,b,c}}).", hasil_str)

def g_18_5():
    a = set(random.sample(range(1, 15), 6))
    b = set(random.sample(range(1, 15), 5))
    hasil = sorted(a - b)
    a_list = sorted(a)
    b_list = sorted(b)
    hasil_str = "{" + ",".join(map(str, hasil)) + "}"
    return q(f"A = {{{','.join(map(str,a_list))}}}, B = {{{','.join(map(str,b_list))}}}. "
              f"Tentukan A - B (selisih, format: {{a,b,c}}).", hasil_str)

def g_18_6():
    total = ri(30, 50)
    suka_a = ri(15, 25)
    suka_b = ri(15, 25)
    keduanya = ri(5, min(suka_a, suka_b) - 1)
    tidak_suka = total - (suka_a + suka_b - keduanya)
    return q(f"Dari {total} siswa, {suka_a} suka matematika, {suka_b} suka IPA, dan {keduanya} suka keduanya. "
              f"Berapa siswa yang tidak suka keduanya?", tidak_suka)

# ---------------------------------------------------------------------------
# LEVEL 19 - Bilangan Berpangkat & Bentuk Akar (Sulit)
# ---------------------------------------------------------------------------

def g_19_1():
    a, n = ri(2, 9), ri(2, 4)
    return q(f"{a}^{n} = ...", a ** n)

def g_19_2():
    a = ri(2, 9)
    tipe = random.choice(["negatif", "nol"])
    if tipe == "nol":
        return q(f"{a}^0 = ...", 1)
    n = ri(1, 3)
    return q(f"{a}^-{n} = ... (bentuk pecahan)", f"1/{a**n}")

def g_19_3():
    a, m, n = ri(2, 6), ri(1, 4), ri(1, 4)
    return q(f"Sederhanakan: {a}^{m} x {a}^{n} = ... (bentuk {a}^pangkat)", f"{a}^{m+n}")

def g_19_4():
    base = random.choice([2, 3, 5])
    n = ri(2, 4)
    val = base * base * n
    return q(f"Sederhanakan akar {val} (bentuk a akar b, tulis sebagai 'a akar b')", f"{base} akar {n}")

def g_19_5():
    n = random.choice([2, 3, 5])
    a, b = ri(1, 5), ri(1, 5)
    return q(f"{a} akar {n} + {b} akar {n} = ... (bentuk 'c akar {n}')", f"{a+b} akar {n}")

def g_19_6():
    n = random.choice([2, 3, 5])
    a = ri(1, 6)
    return q(f"Rasionalkan penyebut: {a} / akar {n} = ... (bentuk 'a akar {n} / {n}')",
              f"{a} akar {n} / {n}")

# ---------------------------------------------------------------------------
# LEVEL 20 - PLSV, PtLSV, PLDV Dasar (Sulit)
# ---------------------------------------------------------------------------

def g_20_1():
    x = ri(2, 10)
    a = ri(2, 6)
    b = ri(1, 5)
    c = a * x + b
    return q(f"Tentukan nilai x: {a}x + {b} = {c} (x bulat)", x)

def g_20_2():
    x_batas = ri(2, 10)
    a = ri(2, 6)
    tanda = random.choice([">", "<", ">=", "<="])
    b = a * x_batas
    return q(f"Selesaikan pertidaksamaan: {a}x {tanda} {b}. Tentukan batas nilai x (format: x {tanda} {x_batas})",
              f"x {tanda} {x_batas}")

def g_20_3():
    x = ri(2, 12)
    a, b, c = ri(2, 5), ri(1, 10), ri(1, 5)
    total = a * x - b
    tanda = random.choice([">", "<"])
    return q(f"Selesaikan: {a}x - {b} {tanda} {total-c if tanda=='>' else total+c}. "
              f"Tentukan bentuk paling sederhana (format: x {tanda} nilai)",
              f"x {tanda} {x - c//a if tanda=='>' else x + c//a}")

def g_20_4():
    batas = ri(-5, 10)
    tanda = random.choice([">", "<", ">=", "<="])
    return q(f"Gambarkan garis bilangan untuk x {tanda} {batas}. Berapa batas nilai x pada pertidaksamaan tersebut?", batas)

def g_20_5():
    a, b, c = ri(1, 5), ri(1, 5), ri(5, 30)
    x = ri(1, 8)
    y = (c - a * x) / b if b != 0 else 0
    return q(f"Diketahui PLDV: {a}x + {b}y = {c}. Jika x = {x}, berapa nilai y?", round(y, 2))

def g_20_6():
    n1 = nama()
    x = ri(3, 15)
    a, b = ri(2, 6), ri(1, 10)
    total = a * x + b
    return q(f"{n1} membeli beberapa buku (x buku) seharga Rp{a}.000 per buku, ditambah ongkos kirim Rp{b}.000. "
              f"Jika total yang dibayar Rp{total}.000, berapa buku yang dibeli {n1}?", x)

# ---------------------------------------------------------------------------
# LEVEL 21 - SPLDV (Sulit)
# ---------------------------------------------------------------------------

def _gen_spldv():
    x, y = ri(1, 10), ri(1, 10)
    a1, b1 = ri(1, 5), ri(1, 5)
    a2, b2 = ri(1, 5), ri(1, 5)
    while a1 * b2 - a2 * b1 == 0:
        a2, b2 = ri(1, 5), ri(1, 5)
    c1 = a1 * x + b1 * y
    c2 = a2 * x + b2 * y
    return a1, b1, c1, a2, b2, c2, x, y

def g_21_1():
    a1, b1, c1, a2, b2, c2, x, y = _gen_spldv()
    return q(f"Selesaikan SPLDV berikut dengan substitusi: {a1}x + {b1}y = {c1} dan {a2}x + {b2}y = {c2}. "
              f"Tentukan nilai x dan y (format: x,y)", f"{x},{y}")

def g_21_2():
    a1, b1, c1, a2, b2, c2, x, y = _gen_spldv()
    return q(f"Selesaikan SPLDV berikut dengan eliminasi: {a1}x + {b1}y = {c1} dan {a2}x + {b2}y = {c2}. "
              f"Tentukan nilai x dan y (format: x,y)", f"{x},{y}")

def g_21_3():
    a1, b1, c1, a2, b2, c2, x, y = _gen_spldv()
    return q(f"Selesaikan SPLDV berikut (metode campuran): {a1}x + {b1}y = {c1} dan {a2}x + {b2}y = {c2}. "
              f"Tentukan nilai x dan y (format: x,y)", f"{x},{y}")

def g_21_4():
    a1, b1, c1, a2, b2, c2, x, y = _gen_spldv()
    return q(f"Selesaikan SPLDV berikut dengan metode grafik: {a1}x + {b1}y = {c1} dan {a2}x + {b2}y = {c2}. "
              f"Tentukan titik potong (x,y)", f"{x},{y}")

def g_21_5():
    n1 = nama()
    harga_a, harga_b = ri(2, 8) * 1000, ri(2, 8) * 1000
    jml_a, jml_b = ri(1, 5), ri(1, 5)
    total = harga_a * jml_a + harga_b * jml_b
    return q(f"{n1} membeli {jml_a} pensil dan {jml_b} buku dengan total Rp{total}. "
              f"Jika harga 1 pensil Rp{harga_a} dan 1 buku Rp{harga_b}, berapa total tersebut membuktikan "
              f"harga sesuai (jawab 'benar' jika sesuai)?", "benar")

def g_21_6():
    x, y, z = ri(1, 6), ri(1, 6), ri(1, 6)
    return q(f"Sistem persamaan linear tiga variabel (SPLTV) memiliki penyelesaian x={x}, y={y}, z={z}. "
              f"Berapa nilai dari x+y+z?", x + y + z)

# ---------------------------------------------------------------------------
# LEVEL 22 - Relasi & Fungsi (Sulit)
# ---------------------------------------------------------------------------

def g_22_1():
    domain = sorted(random.sample(range(1, 10), 3))
    kodomain = sorted(random.sample(range(10, 20), 3))
    return q(f"Diketahui domain {{{','.join(map(str,domain))}}} dan kodomain {{{','.join(map(str,kodomain))}}}. "
              f"Berapa banyak anggota domain?", len(domain))

def g_22_2():
    pairs = [(x, x + ri(1, 5)) for x in random.sample(range(1, 8), 3)]
    pairs_str = ", ".join(f"({a},{b})" for a, b in pairs)
    return q(f"Fungsi dinyatakan sebagai pasangan berurutan: {pairs_str}. "
              f"Berapa nilai fungsi untuk x = {pairs[0][0]}?", pairs[0][1])

def g_22_3():
    a, b = ri(2, 6), ri(1, 10)
    return q(f"Fungsi f(x) = {a}x + {b}. Tentukan bentuk f(x) jika x diganti dengan 2x (format: {a*2}x + {b})",
              f"{a*2}x + {b}")

def g_22_4():
    a, b, x = ri(2, 8), ri(1, 10), ri(1, 10)
    return q(f"Fungsi f(x) = {a}x + {b}. Tentukan nilai f({x}).", a * x + b)

def g_22_5():
    a, b = ri(2, 6), ri(1, 8)
    x1, x2 = 1, 2
    y1, y2 = a * x1 + b, a * x2 + b
    return q(f"Dari tabel: x=1 -> y={y1}, x=2 -> y={y2}. Tentukan rumus fungsi f(x) = ax+b (format: ax+b)",
              f"{a}x+{b}")

def g_22_6():
    n1 = nama()
    a, b, x = ri(2, 6), ri(5, 20), ri(2, 10)
    return q(f"Biaya sewa mobil dinyatakan f(x) = {a}x + {b} (ribu rupiah), dengan x adalah jumlah hari sewa. "
              f"Berapa biaya sewa {n1} jika menyewa selama {x} hari (ribu rupiah)?", a * x + b)

# ---------------------------------------------------------------------------
# LEVEL 23 - Garis & Sudut (Sulit)
# ---------------------------------------------------------------------------

def g_23_1():
    tipe = random.choice(["sejajar", "tegak lurus", "berpotongan"])
    ciri = {"sejajar": "tidak akan pernah bertemu meskipun diperpanjang",
            "tegak lurus": "berpotongan membentuk sudut 90 derajat",
            "berpotongan": "bertemu di satu titik"}
    return q(f"Dua garis yang {ciri[tipe]} disebut garis ...", tipe)

def g_23_2():
    besar = random.choice([30, 45, 89, 90, 120, 180, 200])
    if besar < 90:
        jenis = "lancip"
    elif besar == 90:
        jenis = "siku-siku"
    elif besar < 180:
        jenis = "tumpul"
    elif besar == 180:
        jenis = "lurus"
    else:
        jenis = "refleks"
    return q(f"Sudut sebesar {besar} derajat termasuk jenis sudut ...", jenis)

def g_23_3():
    a = ri(20, 160)
    tipe = random.choice(["pelurus", "penyiku"])
    if tipe == "pelurus":
        return q(f"Dua sudut saling berpelurus. Jika salah satu sudut {a} derajat, berapa sudut lainnya?", 180 - a)
    a = ri(10, 80)
    return q(f"Dua sudut saling berpenyiku. Jika salah satu sudut {a} derajat, berapa sudut lainnya?", 90 - a)

def g_23_4():
    a = ri(30, 150)
    tipe = random.choice(["sehadap", "dalam berseberangan", "luar berseberangan"])
    # sehadap dan berseberangan sama besar
    return q(f"Dua garis sejajar dipotong garis lain. Salah satu sudut {a} derajat. "
              f"Berapa besar sudut yang {tipe} dengannya (sudut sama besar)?", a)

def g_23_5():
    a, b = ri(30, 100), ri(30, 100)
    c = 180 - a - b
    return q(f"Segitiga memiliki dua sudut {a} derajat dan {b} derajat. Berapa besar sudut ketiga?", c)

def g_23_6():
    n1 = nama()
    a = ri(40, 140)
    return q(f"{n1} mengukur sudut kemiringan atap rumah sebesar {a} derajat. "
              f"Berapa besar sudut pelurusnya?", 180 - a)

# ---------------------------------------------------------------------------
# LEVEL 24 - Segitiga & Teorema Pythagoras (Sulit)
# ---------------------------------------------------------------------------

def g_24_1():
    tipe = random.choice(["siku-siku", "sama kaki", "sama sisi", "sembarang"])
    ciri = {"siku-siku": "salah satu sudutnya 90 derajat",
            "sama kaki": "dua sisinya sama panjang",
            "sama sisi": "ketiga sisinya sama panjang",
            "sembarang": "ketiga sisinya berbeda panjang"}
    return q(f"Segitiga yang {ciri[tipe]} disebut segitiga ...", tipe)

def g_24_2():
    a, t = ri(6, 20), ri(4, 15)
    return q(f"Segitiga dengan alas {a} cm dan tinggi {t} cm. Berapa luasnya (cm persegi)?", a * t / 2)

def g_24_3():
    triples = [(3,4,5), (6,8,10), (5,12,13), (9,12,15), (8,15,17), (7,24,25)]
    a, b, c = random.choice(triples)
    k = ri(1, 3)
    a, b, c = a*k, b*k, c*k
    tanya = random.choice(["sisi_miring", "sisi_tegak"])
    if tanya == "sisi_miring":
        return q(f"Segitiga siku-siku memiliki sisi tegak {a} cm dan {b} cm. Berapa panjang sisi miringnya (cm)?", c)
    return q(f"Segitiga siku-siku memiliki sisi miring {c} cm dan salah satu sisi tegak {a} cm. "
              f"Berapa panjang sisi tegak lainnya (cm)?", b)

def g_24_4():
    triples = [(3,4,5), (6,8,10), (5,12,13), (9,12,15)]
    is_valid = random.choice([True, False])
    if is_valid:
        a, b, c = random.choice(triples)
    else:
        a, b, c = ri(3, 10), ri(3, 10), ri(15, 25)
        is_valid = (a*a + b*b == c*c)
    jawaban = "siku-siku" if (a*a + b*b == c*c) else "bukan siku-siku"
    return q(f"Sebuah segitiga memiliki sisi {a} cm, {b} cm, dan {c} cm. "
              f"Apakah segitiga tersebut siku-siku? (jawab: 'siku-siku' atau 'bukan siku-siku')", jawaban)

def g_24_5():
    triples = [(3,4,5), (6,8,10), (5,12,13), (9,12,15), (8,15,17)]
    a, b, c = random.choice(triples)
    k = ri(1, 4)
    a, b, c = a*k, b*k, c*k
    n1 = nama()
    return q(f"{n1} menyandarkan tangga sepanjang {c} m ke tembok. Jarak kaki tangga ke tembok {a} m. "
              f"Berapa tinggi tangga menyentuh tembok (m)?", b)

def g_24_6():
    triples = [(3,4,5), (6,8,10), (5,12,13)]
    a, b, c = random.choice(triples)
    k = ri(1, 5)
    a, b, c = a*k, b*k, c*k
    return q(f"Sebuah lapangan berbentuk siku-siku dengan sisi {a} m dan {b} m. "
              f"Berapa panjang diagonal lapangan tersebut (m)?", c)

# ---------------------------------------------------------------------------
# LEVEL 25 - Segiempat & Segi-n (Sulit)
# ---------------------------------------------------------------------------

def g_25_1():
    ciri_map = {
        "persegi": "semua sisi sama panjang dan semua sudut 90 derajat",
        "persegi panjang": "sisi berhadapan sama panjang dan semua sudut 90 derajat",
        "belah ketupat": "semua sisi sama panjang dengan sudut berhadapan sama besar (bukan 90)",
        "layang-layang": "dua pasang sisi berdekatan sama panjang",
        "trapesium": "memiliki sepasang sisi sejajar",
    }
    bangun = random.choice(list(ciri_map.keys()))
    return q(f"Segiempat dengan ciri: {ciri_map[bangun]}, disebut ...", bangun)

def g_25_2():
    bangun = random.choice(["persegi", "belah ketupat"])
    return q(f"Pada bangun {bangun}, berapa banyak sisi yang sama panjang (dari total 4 sisi)?", 4)

def g_25_3():
    s = ri(5, 20)
    bangun = random.choice(["persegi"])
    if bangun == "persegi":
        tipe = random.choice(["keliling", "luas"])
        if tipe == "keliling":
            return q(f"Persegi dengan sisi {s} cm. Berapa kelilingnya (cm)?", 4 * s)
        return q(f"Persegi dengan sisi {s} cm. Berapa luasnya (cm persegi)?", s * s)
    return q("", "")

def g_25_4():
    n = random.choice([5, 6, 8])
    nama_map = {5: "segilima", 6: "segienam", 8: "segidelapan"}
    return q(f"Bangun {nama_map[n]} beraturan memiliki berapa sisi?", n)

def g_25_5():
    n = random.choice([5, 6, 8, 10])
    total_sudut = (n - 2) * 180
    return q(f"Tentukan jumlah besar sudut dalam segi-{n} beraturan (derajat), rumus (n-2) x 180.", total_sudut)

def g_25_6():
    n1 = nama()
    p, l = ri(10, 30), ri(5, 20)
    return q(f"{n1} memiliki lahan persegi panjang berukuran {p} m x {l} m. Lahan tersebut akan dipagari "
              f"keliling lahan. Berapa meter pagar yang dibutuhkan?", 2 * (p + l))

# ---------------------------------------------------------------------------
# LEVEL 26 - Bangun Ruang Sisi Datar & Luas Permukaan (Sulit)
# ---------------------------------------------------------------------------

def g_26_1():
    bangun = random.choice(["kubus", "balok", "prisma", "limas"])
    n_sisi = {"kubus": 6, "balok": 6, "prisma": 5, "limas": 5}
    return q(f"Bangun ruang {bangun} segitiga/segiempat memiliki berapa banyak sisi minimal (untuk bentuk paling sederhana)?", n_sisi[bangun])

def g_26_2():
    bangun = random.choice(["kubus", "balok"])
    return q(f"Jaring-jaring {bangun} tersusun dari bangun datar apa? (persegi/persegi panjang)",
              "persegi" if bangun == "kubus" else "persegi panjang")

def g_26_3():
    s = ri(4, 15)
    return q(f"Kubus dengan rusuk {s} cm. Berapa luas permukaannya (cm persegi)?", 6 * s * s)

def g_26_4():
    alas, tinggi_seg, keliling_alas, tinggi_prisma = ri(4,10), ri(3,8), ri(12,30), ri(5,15)
    luas_alas = alas * tinggi_seg / 2
    lp = 2 * luas_alas + keliling_alas * tinggi_prisma
    return q(f"Prisma segitiga: luas alas segitiga = {luas_alas} cm persegi, keliling alas {keliling_alas} cm, "
              f"tinggi prisma {tinggi_prisma} cm. Berapa luas permukaannya (cm persegi)?", lp)

def g_26_5():
    s, tinggi_sisi = ri(4, 12), ri(5, 15)
    luas_alas = s * s
    luas_sisi_total = 4 * (0.5 * s * tinggi_sisi)
    lp = luas_alas + luas_sisi_total
    return q(f"Limas segiempat beraturan dengan sisi alas {s} cm dan tinggi sisi tegak {tinggi_sisi} cm. "
              f"Berapa luas permukaannya (cm persegi)?", lp)

def g_26_6():
    n1 = nama()
    s = ri(3, 10)
    lp = 6 * s * s
    return q(f"{n1} akan mengecat seluruh permukaan kotak kubus dengan rusuk {s} cm. "
              f"Berapa cm persegi luas permukaan yang akan dicat?", lp)

# ---------------------------------------------------------------------------
# LEVEL 27 - Volume Bangun Ruang (Sulit)
# ---------------------------------------------------------------------------

def g_27_1():
    x = ri(2, 10)
    p, l, t = x, x + ri(1,3), x + ri(2,5)
    return q(f"Balok memiliki p={p} cm, l={l} cm, t={t} cm. Berapa volumenya (cm kubik)?", p * l * t)

def g_27_2():
    alas, tinggi_seg, tinggi_prisma = ri(4, 12), ri(3, 10), ri(5, 15)
    luas_alas = alas * tinggi_seg / 2
    return q(f"Prisma segitiga dengan luas alas {luas_alas} cm persegi dan tinggi {tinggi_prisma} cm. "
              f"Berapa volumenya (cm kubik)?", luas_alas * tinggi_prisma)

def g_27_3():
    s, t = ri(4, 12), ri(5, 15)
    luas_alas = s * s
    return q(f"Limas segiempat dengan sisi alas {s} cm dan tinggi {t} cm. Berapa volumenya "
              f"(cm kubik)? (rumus: 1/3 x luas alas x tinggi)", round(luas_alas * t / 3, 2))

def g_27_4():
    r, t = ri(3, 10), ri(5, 20)
    return q(f"Tabung berjari-jari {r} cm dan tinggi {t} cm (pi=3.14). Berapa volumenya (cm kubik)?",
              round(3.14 * r * r * t, 2))

def g_27_5():
    r, t = ri(3, 10), ri(5, 20)
    return q(f"Kerucut berjari-jari {r} cm dan tinggi {t} cm (pi=3.14). Berapa volumenya "
              f"(cm kubik)? (rumus: 1/3 x pi x r^2 x t)", round((3.14 * r * r * t) / 3, 2))

def g_27_6():
    n1 = nama()
    r, t = ri(3, 8), ri(10, 25)
    vol = round(3.14 * r * r * t, 2)
    return q(f"{n1} memiliki tangki berbentuk tabung dengan jari-jari {r} cm dan tinggi {t} cm. "
              f"Berapa cm kubik volume air maksimal yang dapat ditampung? (pi=3.14)", vol)

# ---------------------------------------------------------------------------
# LEVEL 28 - Lingkaran (Sulit)
# ---------------------------------------------------------------------------

def g_28_1():
    istilah = random.choice(["jari-jari", "diameter", "busur", "juring", "tembereng"])
    definisi = {
        "jari-jari": "jarak dari pusat ke tepi lingkaran",
        "diameter": "garis lurus yang melalui pusat dan menghubungkan dua titik pada lingkaran",
        "busur": "bagian dari keliling lingkaran",
        "juring": "daerah lingkaran yang dibatasi oleh dua jari-jari dan busur",
        "tembereng": "daerah lingkaran yang dibatasi oleh tali busur dan busur",
    }
    return q(f"Bagian lingkaran yang merupakan {definisi[istilah]} disebut ...", istilah)

def g_28_2():
    r = ri(3, 20)
    return q(f"Lingkaran berjari-jari {r} cm (pi=3.14). Berapa kelilingnya (cm)?", round(2 * 3.14 * r, 2))

def g_28_3():
    r = ri(3, 20)
    return q(f"Lingkaran berjari-jari {r} cm (pi=3.14). Berapa luasnya (cm persegi)?", round(3.14 * r * r, 2))

def g_28_4():
    r = ri(4, 20)
    sudut = random.choice([30, 60, 90, 120, 180])
    keliling = 2 * 3.14 * r
    panjang_busur = round(keliling * sudut / 360, 2)
    return q(f"Lingkaran berjari-jari {r} cm dengan sudut pusat {sudut} derajat (pi=3.14). "
              f"Berapa panjang busurnya (cm)?", panjang_busur)

def g_28_5():
    sudut_keliling = ri(20, 80)
    return q(f"Sudut keliling suatu lingkaran adalah {sudut_keliling} derajat. "
              f"Berapa besar sudut pusat yang menghadap busur yang sama? (sudut pusat = 2 x sudut keliling)",
              2 * sudut_keliling)

def g_28_6():
    n1 = nama()
    r = ri(5, 20)
    luas = round(3.14 * r * r, 2)
    return q(f"{n1} memiliki taman berbentuk lingkaran dengan jari-jari {r} m (pi=3.14). "
              f"Berapa luas taman tersebut (m persegi)?", luas)

# ---------------------------------------------------------------------------
# LEVEL 29 - Statistika & Peluang (Sulit)
# ---------------------------------------------------------------------------

def g_29_1():
    tipe = random.choice(["populasi", "sampel", "sensus"])
    definisi = {
        "populasi": "keseluruhan objek yang diteliti",
        "sampel": "sebagian dari populasi yang diteliti",
        "sensus": "pengumpulan data dari seluruh anggota populasi",
    }
    return q(f"Istilah statistika untuk {definisi[tipe]} disebut ...", tipe)

def g_29_2():
    data = [ri(1, 10) for _ in range(15)]
    target = random.choice(data)
    return q(f"Data: {', '.join(map(str,data))}. Berapa frekuensi kemunculan angka {target} dalam data tersebut?",
              data.count(target))

def g_29_3():
    total = ri(40, 100)
    persen = random.choice([20, 25, 40, 50])
    return q(f"Diagram lingkaran dari {total} siswa menunjukkan {persen}% memilih olahraga renang. "
              f"Berapa siswa yang memilih renang?", total * persen // 100)

def g_29_4():
    data = sorted([ri(1, 20) for _ in range(7)])
    return q(f"Data: {', '.join(map(str,data))}. Tentukan median dari data tersebut.", data[3])

def g_29_5():
    total = random.choice([6, 8, 10, 12])
    kejadian = ri(1, total - 1)
    return q(f"Dalam {total} kali percobaan lempar koin/dadu, kejadian tertentu muncul {kejadian} kali. "
              f"Berapa frekuensi relatif (peluang empiris) kejadian tersebut? (bentuk pecahan sederhana)",
              frac_str(Fraction(kejadian, total)))

def g_29_6():
    n1 = nama()
    total = ri(30, 60)
    suka_a, suka_b = ri(10, 20), ri(10, 20)
    return q(f"{n1} melakukan survei ke {total} siswa: {suka_a} suka bola basket dan {suka_b} suka bulu tangkis "
              f"(tidak ada yang suka keduanya, semua suka salah satu). Berapa total siswa yang disurvei "
              f"sesuai data ({suka_a}+{suka_b})?", suka_a + suka_b)

# ---------------------------------------------------------------------------
# LEVEL 30 - Trigonometri & Transformasi (Sulit)
# ---------------------------------------------------------------------------

def g_30_1():
    triples = [(3,4,5), (6,8,10), (5,12,13)]
    a, b, c = random.choice(triples)
    fungsi = random.choice(["sin", "cos", "tan"])
    sudut_depan = a  # sisi depan sudut acuan
    nilai_map = {"sin": Fraction(a, c), "cos": Fraction(b, c), "tan": Fraction(a, b)}
    return q(f"Segitiga siku-siku dengan sisi depan {a}, sisi samping {b}, sisi miring {c}. "
              f"Tentukan nilai {fungsi} dari sudut acuan (bentuk pecahan sederhana).",
              frac_str(nilai_map[fungsi]))

def g_30_2():
    sudut = random.choice([0, 30, 45, 60, 90])
    nilai = {0: {"sin":"0","cos":"1","tan":"0"},
              30: {"sin":"1/2","cos":"1/2 akar3","tan":"1/3 akar3"},
              45: {"sin":"1/2 akar2","cos":"1/2 akar2","tan":"1"},
              60: {"sin":"1/2 akar3","cos":"1/2","tan":"akar3"},
              90: {"sin":"1","cos":"0","tan":"tidak terdefinisi"}}
    fungsi = random.choice(["sin", "cos", "tan"])
    return q(f"Tentukan nilai {fungsi} {sudut} derajat.", nilai[sudut][fungsi])

def g_30_3():
    tinggi_pengamat = ri(1, 2)
    jarak = ri(10, 50)
    sudut = random.choice([30, 45, 60])
    tan_map = {30: 1/1.732, 45: 1, 60: 1.732}
    tinggi_objek = round(jarak * tan_map[sudut] + tinggi_pengamat, 2)
    return q(f"Seseorang berdiri {jarak} m dari sebuah menara dan melihat puncak menara dengan sudut elevasi "
              f"{sudut} derajat. Tinggi mata pengamat {tinggi_pengamat} m. "
              f"Berapa perkiraan tinggi menara (m, dibulatkan 2 desimal)?", tinggi_objek)

def g_30_4():
    x, y = ri(-10, 10), ri(-10, 10)
    tipe = random.choice(["translasi", "refleksi sumbu x", "refleksi sumbu y", "rotasi 180"])
    if tipe == "translasi":
        dx, dy = ri(-5, 5), ri(-5, 5)
        return q(f"Titik ({x},{y}) ditranslasikan sejauh ({dx},{dy}). Tentukan koordinat bayangannya (format: x,y)",
                  f"{x+dx},{y+dy}")
    if tipe == "refleksi sumbu x":
        return q(f"Titik ({x},{y}) dicerminkan terhadap sumbu x. Tentukan koordinat bayangannya (format: x,y)",
                  f"{x},{-y}")
    if tipe == "refleksi sumbu y":
        return q(f"Titik ({x},{y}) dicerminkan terhadap sumbu y. Tentukan koordinat bayangannya (format: x,y)",
                  f"{-x},{y}")
    return q(f"Titik ({x},{y}) dirotasi 180 derajat terhadap titik asal (0,0). "
              f"Tentukan koordinat bayangannya (format: x,y)", f"{-x},{-y}")

def g_30_5():
    x, y = ri(-8, 8), ri(-8, 8)
    dx, dy = ri(-4, 4), ri(-4, 4)
    x1, y1 = x + dx, y + dy
    x2, y2 = -x1, y1
    return q(f"Titik ({x},{y}) ditranslasi sejauh ({dx},{dy}), kemudian dicerminkan terhadap sumbu y. "
              f"Tentukan koordinat akhir (format: x,y)", f"{x2},{y2}")

def g_30_6():
    n1 = nama()
    jarak = ri(20, 60)
    sudut = 45
    tinggi = round(jarak * 1, 2)
    return q(f"{n1} berdiri {jarak} m dari sebuah pohon dan melihat puncaknya dengan sudut elevasi 45 derajat "
              f"(anggap tinggi mata pengamat 0). Berapa tinggi pohon tersebut (m)?", tinggi)

# ---------------------------------------------------------------------------
# REGISTRY - Kumpulan semua generator soal per (level, sub)
# ---------------------------------------------------------------------------

QUESTION_GENERATORS = {}
for lvl in range(0, 31):
    for sub in range(1, 7):
        fn_name = f"g_{lvl}_{sub}"
        if fn_name in globals():
            QUESTION_GENERATORS[(lvl, sub)] = globals()[fn_name]


def get_questions(level: int, sub: int, n: int = 5):
    """Menghasilkan n soal untuk sub-level tertentu."""
    fn = QUESTION_GENERATORS.get((level, sub))
    if fn is None:
        return []
    return make_set(fn, n)
