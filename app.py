# -*- coding: utf-8 -*-
"""
Aplikasi Tracking Level Siswa - Matematika
Streamlit + Google Sheets sebagai database.
"""
import datetime

import streamlit as st

import config
import questions
import sheets_manager as sm

st.set_page_config(page_title="Tracking Level Matematika", page_icon="🧮", layout="centered")

PASS_LULUS = 80  # persen


# ---------------------------------------------------------------------------
# UTIL
# ---------------------------------------------------------------------------

def rupiah(n):
    return f"Rp {n:,}".replace(",", ".")


def init_state():
    defaults = {
        "mode": None,          # "guru" atau "siswa"
        "guru_login": False,
        "siswa_nama": "",
        "quiz_soal": None,
        "quiz_level": None,
        "quiz_sub": None,
        "quiz_jawaban": {},
        "quiz_kode": None,
        "quiz_selesai": False,
        "quiz_hasil": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


init_state()

try:
    sm.ensure_sheets_exist()
    SHEETS_OK = True
    SHEETS_ERROR = None
except Exception as e:  # noqa: BLE001
    SHEETS_OK = False
    SHEETS_ERROR = str(e)


# ---------------------------------------------------------------------------
# SIDEBAR - PILIH MODE
# ---------------------------------------------------------------------------

st.sidebar.title("🧮 Menu")
mode = st.sidebar.radio("Masuk sebagai:", ["Siswa", "Guru"], index=0)
st.session_state.mode = mode.lower()

if not SHEETS_OK:
    st.error(
        "⚠️ Gagal terhubung ke Google Sheets. Pastikan `secrets.toml` sudah diisi "
        "dengan benar (lihat README).\n\nDetail error:\n" + str(SHEETS_ERROR)
    )
    st.stop()


# ---------------------------------------------------------------------------
# MODE GURU
# ---------------------------------------------------------------------------

def halaman_guru():
    st.title("👩‍🏫 Panel Guru")

    if not st.session_state.guru_login:
        pw = st.text_input("Masukkan password guru", type="password")
        if st.button("Masuk"):
            correct_pw = st.secrets.get("app_config", {}).get("guru_password", "admin123")
            if pw == correct_pw:
                st.session_state.guru_login = True
                st.rerun()
            else:
                st.error("Password salah.")
        return

    # --- Ambil data sekali di awal, dipakai bersama di semua tab ---
    siswa_records = sm.get_all_records("siswa")
    kode_records = sm.get_all_records("kode_akses")
    riwayat_records = sm.get_all_records("riwayat")

    # --- RINGKASAN DASHBOARD ---
    kode_aktif = sum(1 for r in kode_records if r.get("status") == "Aktif")
    kode_terpakai = sum(1 for r in kode_records if r.get("status") == "Terpakai")
    pendapatan = sum(
        int(r.get("harga", 0) or 0) for r in kode_records if r.get("status") == "Terpakai"
    )
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("👥 Total Siswa", len(siswa_records))
    c2.metric("🎫 Kode Aktif", kode_aktif)
    c3.metric("✅ Kode Terpakai", kode_terpakai)
    c4.metric("💰 Pendapatan", rupiah(pendapatan))
    if st.button("🔄 Muat Ulang Data", help="Ambil data terbaru dari Google Sheets"):
        sm._invalidate_cache()
        st.rerun()

    st.divider()

    tab1, tab2, tab3, tab4 = st.tabs(
        ["💳 Generate Kode Akses", "📋 Daftar Kode", "👥 Data Siswa", "📊 Riwayat"]
    )

    # --- TAB 1: Generate kode akses ---
    with tab1:
        st.subheader("Buat Kode Akses Baru")

        # Langkah 1: pilih siswa -> level & sub-level otomatis terisi
        nama_siswa_list = sorted({str(r.get("nama", "")).strip() for r in siswa_records if r.get("nama")})
        opsi_siswa = ["-- Pilih siswa terdaftar (opsional) --"] + nama_siswa_list
        pilih_siswa = st.selectbox(
            "1️⃣ Pilih Siswa",
            opsi_siswa,
            help="Pilih siswa yang sudah terdaftar supaya Level & Sub-Level "
                 "otomatis terisi sesuai progres terakhirnya."
        )

        default_level, default_sub = 0, 1
        nama_pembeli_default = ""
        if pilih_siswa != opsi_siswa[0]:
            rec = next((r for r in siswa_records if str(r.get("nama", "")).strip() == pilih_siswa), None)
            if rec:
                default_level = int(rec.get("level", 0) or 0)
                default_sub = int(rec.get("sub_level", 1) or 1)
                nama_pembeli_default = pilih_siswa
                st.caption(
                    f"📍 Progres terakhir **{pilih_siswa}**: Level {default_level}.{default_sub} — "
                    f"{config.get_sub_nama(default_level, default_sub)} "
                    f"(Level & Sub-Level di bawah otomatis diarahkan ke sini)"
                )

        st.markdown("**2️⃣ Level & Sub-Level**")
        col1, col2 = st.columns(2)
        level_list = sorted(config.LEVELS.keys())
        with col1:
            level_labels = [
                f"Level {l} — {config.get_materi(l)} ({config.get_kesulitan(l)})" for l in level_list
            ]
            level_idx_default = level_list.index(default_level) if default_level in level_list else 0
            level_idx = st.selectbox(
                "Level", range(len(level_list)), index=level_idx_default,
                format_func=lambda i: level_labels[i], key=f"pilih_level_guru_{pilih_siswa}"
            )
            lvl_pilih = level_list[level_idx]
        with col2:
            sub_list = sorted(config.LEVELS[lvl_pilih]["sub"].keys())
            sub_labels = [f"Sub {s} — {config.get_sub_nama(lvl_pilih, s)}" for s in sub_list]
            sub_idx_default = sub_list.index(default_sub) if (lvl_pilih == default_level and default_sub in sub_list) else 0
            sub_idx = st.selectbox(
                "Sub-Level", range(len(sub_list)), index=sub_idx_default,
                format_func=lambda i: sub_labels[i], key=f"pilih_sub_guru_{pilih_siswa}_{lvl_pilih}"
            )
            sub_pilih = sub_list[sub_idx]

        harga = config.get_harga(lvl_pilih)
        kesulitan = config.get_kesulitan(lvl_pilih)
        st.info(f"Tingkat kesulitan: **{kesulitan}** — Harga: **{rupiah(harga)}**")

        st.markdown("**3️⃣ Konfirmasi**")
        nama_pembeli = st.text_input("Nama siswa pembeli", value=nama_pembeli_default)

        if st.button("🎫 Generate Kode Akses", type="primary"):
            kode = sm.buat_kode_akses(lvl_pilih, sub_pilih, harga, nama_pembeli)
            st.success(f"Kode berhasil dibuat: **`{kode}`**")
            st.caption("Kode berlaku 7 hari dan hanya bisa dipakai 1 kali. "
                       "Berikan kode ini kepada siswa setelah pembayaran diterima.")
            st.rerun()

    # --- TAB 2: Daftar kode akses ---
    with tab2:
        st.subheader("Semua Kode Akses")
        if kode_records:
            colf1, colf2 = st.columns([2, 1])
            with colf1:
                cari_nama = st.text_input("🔍 Cari nama siswa / kode", key="cari_kode")
            with colf2:
                filter_status = st.multiselect(
                    "Filter status", ["Aktif", "Terpakai", "Kadaluarsa"],
                    default=["Aktif", "Terpakai", "Kadaluarsa"]
                )
            filtered = [r for r in kode_records if r.get("status") in filter_status]
            if cari_nama:
                kw = cari_nama.strip().lower()
                filtered = [
                    r for r in filtered
                    if kw in str(r.get("dibeli_oleh", "")).lower() or kw in str(r.get("kode", "")).lower()
                ]
            st.caption(f"Menampilkan {len(filtered)} dari {len(kode_records)} kode.")
            st.dataframe(list(reversed(filtered)), width='stretch')
        else:
            st.caption("Belum ada kode akses yang dibuat.")

    # --- TAB 3: Data siswa ---
    with tab3:
        st.subheader("Data Siswa")
        if siswa_records:
            cari_siswa_kw = st.text_input("🔍 Cari nama siswa", key="cari_siswa")
            filtered_siswa = siswa_records
            if cari_siswa_kw:
                kw = cari_siswa_kw.strip().lower()
                filtered_siswa = [r for r in siswa_records if kw in str(r.get("nama", "")).lower()]
            st.caption(f"Menampilkan {len(filtered_siswa)} dari {len(siswa_records)} siswa.")
            st.dataframe(filtered_siswa, width='stretch')
        else:
            st.caption("Belum ada siswa terdaftar.")

    # --- TAB 4: Riwayat ---
    with tab4:
        st.subheader("Riwayat Pengerjaan Soal")
        if riwayat_records:
            st.dataframe(list(reversed(riwayat_records)), width='stretch')
        else:
            st.caption("Belum ada riwayat.")

    st.divider()
    if st.button("Keluar dari Panel Guru"):
        st.session_state.guru_login = False
        st.rerun()


# ---------------------------------------------------------------------------
# MODE SISWA
# ---------------------------------------------------------------------------

def mulai_quiz(level, sub, kode):
    soal_list = questions.get_questions(level, sub, 5)
    st.session_state.quiz_soal = soal_list
    st.session_state.quiz_level = level
    st.session_state.quiz_sub = sub
    st.session_state.quiz_kode = kode
    st.session_state.quiz_jawaban = {}
    st.session_state.quiz_selesai = False
    st.session_state.quiz_hasil = None


def halaman_siswa():
    st.title("🎓 Tracking Level Matematika")

    nama = st.text_input("Nama lengkap kamu", value=st.session_state.siswa_nama)
    if nama:
        st.session_state.siswa_nama = nama.strip()

    if not st.session_state.siswa_nama:
        st.info("Masukkan nama untuk melanjutkan.")
        return

    siswa = sm.cari_siswa(st.session_state.siswa_nama)
    if siswa is None:
        st.warning("Nama kamu belum terdaftar.")
        kelas = st.text_input("Kelas")
        if st.button("Daftar sebagai siswa baru"):
            sm.daftar_siswa_baru(st.session_state.siswa_nama, kelas)
            st.success("Berhasil daftar! Silakan lanjutkan.")
            st.rerun()
        return

    lvl_now = int(siswa["level"])
    sub_now = int(siswa["sub_level"])
    harga_now = config.get_harga(lvl_now)
    kesulitan_now = config.get_kesulitan(lvl_now)

    st.success(
        f"Halo, **{siswa['nama']}**! Level kamu saat ini: "
        f"**Level {lvl_now}.{sub_now}** "
        f"({config.get_sub_nama(lvl_now, sub_now)})"
    )

    colA, colB = st.columns(2)
    colA.metric("💰 Harga sub-level ini", rupiah(harga_now))
    colB.metric("📶 Tingkat kesulitan", kesulitan_now)
    st.caption("Bayar sesuai harga di atas ke guru untuk mendapatkan kode akses sub-level ini.")

    # Jika sedang mengerjakan quiz, tampilkan quiz
    if st.session_state.quiz_soal and not st.session_state.quiz_selesai:
        tampilkan_quiz()
        return

    if st.session_state.quiz_selesai:
        tampilkan_hasil()
        return

    st.divider()
    st.subheader("🔑 Masukkan Kode Akses")
    st.caption(
        "Sudah membayar sub-level yang diinginkan? Masukkan kode akses dari guru di sini."
    )
    kode_input = st.text_input("Kode akses", placeholder="Contoh: SL021-A1B2C3")
    if st.button("Mulai Kerjakan Soal", type="primary"):
        rec, pesan = sm.cek_kode(kode_input)
        if rec is None:
            st.error(pesan)
        else:
            level_kode = int(rec["level"])
            sub_kode = int(rec["sub_level"])
            mulai_quiz(level_kode, sub_kode, kode_input)
            st.rerun()

    with st.expander("💰 Lihat Daftar Harga Semua Level", expanded=False):
        tabel_harga = [
            {
                "Level": lvl,
                "Materi": config.LEVELS[lvl]["materi"],
                "Kesulitan": config.LEVELS[lvl]["kesulitan"],
                "Harga/Sub-Level": rupiah(config.get_harga(lvl)),
            }
            for lvl in sorted(config.LEVELS.keys())
        ]
        st.dataframe(tabel_harga, width="stretch", hide_index=True)
        st.caption("Mudah: Rp5.000 · Sedang: Rp10.000 · Sulit: Rp15.000 per sub-level")


def tampilkan_quiz():
    level, sub = st.session_state.quiz_level, st.session_state.quiz_sub
    st.subheader(f"📝 Level {level}.{sub} — {config.get_sub_nama(level, sub)}")
    st.caption("Jawab kelima soal berikut, lalu klik Kumpulkan Jawaban. "
               "Nilai minimal 80% untuk naik ke sub-level berikutnya.")

    with st.form("form_quiz"):
        for i, item in enumerate(st.session_state.quiz_soal):
            st.markdown(f"**Soal {i+1}.** {item['soal']}")
            jawab = st.text_input(f"Jawaban soal {i+1}", key=f"jwb_{i}")
            st.session_state.quiz_jawaban[i] = jawab
        submit = st.form_submit_button("✅ Kumpulkan Jawaban", type="primary")

    if submit:
        benar = 0
        detail = []
        for i, item in enumerate(st.session_state.quiz_soal):
            jawab_siswa = st.session_state.quiz_jawaban.get(i, "")
            ok = questions.check_answer(jawab_siswa, item["jawaban"])
            if ok:
                benar += 1
            detail.append({
                "soal": item["soal"], "jawaban_benar": item["jawaban"],
                "jawaban_siswa": jawab_siswa, "benar": ok
            })
        skor = round(benar / len(st.session_state.quiz_soal) * 100, 1)
        lulus = skor >= PASS_LULUS

        sm.catat_riwayat(
            st.session_state.siswa_nama, level, sub, skor,
            "LULUS" if lulus else "ULANGI"
        )
        sm.pakai_kode(st.session_state.quiz_kode, st.session_state.siswa_nama)

        next_info = None
        if lulus:
            nxt = config.next_sub(level, sub)
            if nxt:
                sm.update_progress_siswa(st.session_state.siswa_nama, nxt[0], nxt[1])
                next_info = nxt
            else:
                next_info = "SELESAI"

        st.session_state.quiz_hasil = {
            "skor": skor, "lulus": lulus, "detail": detail,
            "level": level, "sub": sub, "next_info": next_info
        }
        st.session_state.quiz_selesai = True
        st.rerun()


def tampilkan_hasil():
    hasil = st.session_state.quiz_hasil
    st.subheader("📊 Hasil Pengerjaan")
    st.metric("Skor kamu", f"{hasil['skor']}%")

    if hasil["lulus"]:
        st.success("🎉 Selamat, kamu LULUS! Skor kamu ≥ 80%.")
        if hasil["next_info"] == "SELESAI":
            st.balloons()
            st.success("Kamu sudah menyelesaikan SEMUA level! Luar biasa! 🏆")
        elif hasil["next_info"]:
            nl, ns = hasil["next_info"]
            harga_next = config.get_harga(nl)
            st.info(f"Kamu naik ke **Level {nl}.{ns}** — {config.get_sub_nama(nl, ns)}. "
                    f"Harga sub-level ini: **{rupiah(harga_next)}**. "
                    f"Beli kode akses baru untuk melanjutkan.")
    else:
        harga_ulang = config.get_harga(hasil["level"])
        st.error(f"Skor kamu belum mencapai 80%. Kamu perlu mengulang sub-level ini "
                 f"dengan kode akses baru (harga: **{rupiah(harga_ulang)}**).")

    with st.expander("Lihat pembahasan jawaban"):
        for i, d in enumerate(hasil["detail"]):
            status_icon = "✅" if d["benar"] else "❌"
            st.markdown(f"{status_icon} **Soal {i+1}:** {d['soal']}")
            st.markdown(f"   Jawaban kamu: `{d['jawaban_siswa']}` — Kunci: `{d['jawaban_benar']}`")

    if st.button("Kembali ke Beranda"):
        st.session_state.quiz_soal = None
        st.session_state.quiz_selesai = False
        st.session_state.quiz_hasil = None
        st.session_state.quiz_jawaban = {}
        st.rerun()


# ---------------------------------------------------------------------------
# ROUTING
# ---------------------------------------------------------------------------

if st.session_state.mode == "guru":
    halaman_guru()
else:
    halaman_siswa()
