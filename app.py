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

    tab1, tab2, tab3, tab4 = st.tabs(
        ["💳 Generate Kode Akses", "📋 Daftar Kode", "👥 Data Siswa", "📊 Riwayat"]
    )

    # --- TAB 1: Generate kode akses ---
    with tab1:
        st.subheader("Buat Kode Akses Baru")
        opsi = config.all_level_options()
        labels = [f"Level {lvl} - Sub {sub} ({config.get_sub_nama(lvl, sub)})" for lvl, sub in opsi]
        idx = st.selectbox("Pilih Level & Sub-Level", range(len(opsi)), format_func=lambda i: labels[i])
        lvl_pilih, sub_pilih = opsi[idx]
        harga = config.get_harga(lvl_pilih)
        kesulitan = config.get_kesulitan(lvl_pilih)
        st.info(f"Tingkat kesulitan: **{kesulitan}** — Harga: **{rupiah(harga)}**")
        nama_pembeli = st.text_input("Nama siswa pembeli (opsional, bisa diisi nanti)")
        if st.button("🎫 Generate Kode Akses", type="primary"):
            kode = sm.buat_kode_akses(lvl_pilih, sub_pilih, harga, nama_pembeli)
            st.success(f"Kode berhasil dibuat: **{kode}**")
            st.caption("Kode berlaku 7 hari dan hanya bisa dipakai 1 kali. "
                       "Berikan kode ini kepada siswa setelah pembayaran diterima.")

    # --- TAB 2: Daftar kode akses ---
    with tab2:
        st.subheader("Semua Kode Akses")
        records = sm.get_all_records("kode_akses")
        if records:
            filter_status = st.multiselect(
                "Filter status", ["Aktif", "Terpakai", "Kadaluarsa"],
                default=["Aktif", "Terpakai", "Kadaluarsa"]
            )
            filtered = [r for r in records if r.get("status") in filter_status]
            st.dataframe(filtered, width='stretch')
        else:
            st.caption("Belum ada kode akses yang dibuat.")

    # --- TAB 3: Data siswa ---
    with tab3:
        st.subheader("Data Siswa")
        records = sm.get_all_records("siswa")
        if records:
            st.dataframe(records, width='stretch')
        else:
            st.caption("Belum ada siswa terdaftar.")

    # --- TAB 4: Riwayat ---
    with tab4:
        st.subheader("Riwayat Pengerjaan Soal")
        records = sm.get_all_records("riwayat")
        if records:
            st.dataframe(list(reversed(records)), width='stretch')
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

    st.success(
        f"Halo, **{siswa['nama']}**! Level kamu saat ini: "
        f"**Level {siswa['level']}.{siswa['sub_level']}** "
        f"({config.get_sub_nama(int(siswa['level']), int(siswa['sub_level']))})"
    )

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

    with st.expander("💰 Lihat Daftar Harga Sub-Level"):
        for lvl in sorted(config.LEVELS.keys()):
            info = config.LEVELS[lvl]
            st.markdown(f"**Level {lvl} — {info['materi']}** ({info['kesulitan']}, "
                        f"{rupiah(config.get_harga(lvl))}/sub-level)")


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
            st.info(f"Kamu naik ke **Level {nl}.{ns}** — {config.get_sub_nama(nl, ns)}. "
                    f"Beli kode akses baru untuk melanjutkan.")
    else:
        st.error("Skor kamu belum mencapai 80%. Kamu perlu mengulang sub-level ini "
                  "dengan kode akses baru.")

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
