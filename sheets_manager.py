# -*- coding: utf-8 -*-
"""
Modul integrasi Google Sheets sebagai database aplikasi.
Menggunakan gspread + service account credentials dari st.secrets.

Struktur 4 sheet yang dibutuhkan (dibuat otomatis jika belum ada):
- siswa       : nama | kelas | level | sub_level | status | tanggal_daftar
- riwayat     : tanggal | nama | level | sub_level | skor | status
- kode_akses  : kode | level | sub_level | harga | dibeli_oleh | status | tanggal_beli | tanggal_pakai
- pretest     : nama | skor | level_awal | sub_level_awal | tanggal
"""
import datetime
import random
import string

import gspread
import streamlit as st
from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

SHEET_HEADERS = {
    "siswa": ["nama", "kelas", "level", "sub_level", "status", "tanggal_daftar"],
    "riwayat": ["tanggal", "nama", "level", "sub_level", "skor", "status"],
    "kode_akses": ["kode", "level", "sub_level", "harga", "dibeli_oleh", "status",
                   "tanggal_beli", "tanggal_pakai"],
    "pretest": ["nama", "skor", "level_awal", "sub_level_awal", "tanggal"],
}


@st.cache_resource(show_spinner=False)
def get_client():
    """Buat koneksi gspread client dari service account di st.secrets."""
    creds_dict = dict(st.secrets["gcp_service_account"])
    creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
    return gspread.authorize(creds)


@st.cache_resource(show_spinner=False)
def get_spreadsheet():
    client = get_client()
    sheet_id = st.secrets["app_config"]["spreadsheet_id"]
    return client.open_by_key(sheet_id)


def ensure_sheets_exist():
    """Pastikan 4 sheet (dengan header) sudah ada di spreadsheet."""
    ss = get_spreadsheet()
    existing = [ws.title for ws in ss.worksheets()]
    for name, headers in SHEET_HEADERS.items():
        if name not in existing:
            ws = ss.add_worksheet(title=name, rows=1000, cols=len(headers) + 2)
            ws.append_row(headers)
        else:
            ws = ss.worksheet(name)
            first_row = ws.row_values(1)
            if first_row != headers:
                ws.update("A1", [headers])


def get_ws(name):
    return get_spreadsheet().worksheet(name)


def get_all_records(name):
    ws = get_ws(name)
    return ws.get_all_records()


# ---------------------------------------------------------------------------
# KODE AKSES
# ---------------------------------------------------------------------------

def generate_kode(level: int, sub: int) -> str:
    rand_part = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"SL{level:02d}{sub}-{rand_part}"


def buat_kode_akses(level: int, sub: int, harga: int, dibeli_oleh: str = "") -> str:
    """Membuat kode akses baru dan menyimpannya ke sheet kode_akses. Return kode."""
    ws = get_ws("kode_akses")
    kode = generate_kode(level, sub)
    tanggal = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ws.append_row([kode, level, sub, harga, dibeli_oleh, "Aktif", tanggal, ""])
    return kode


def cek_kode(kode: str):
    """Cek validitas kode akses. Return dict record jika valid & aktif, else None + alasan."""
    records = get_all_records("kode_akses")
    for i, rec in enumerate(records):
        if str(rec.get("kode", "")).strip().upper() == kode.strip().upper():
            status = rec.get("status", "")
            tanggal_beli = rec.get("tanggal_beli", "")
            if status == "Terpakai":
                return None, "Kode ini sudah pernah digunakan."
            if status == "Kadaluarsa":
                return None, "Kode ini sudah kadaluarsa."
            # cek masa berlaku 7 hari
            try:
                tgl = datetime.datetime.strptime(tanggal_beli, "%Y-%m-%d %H:%M:%S")
                if (datetime.datetime.now() - tgl).days > 7:
                    ws = get_ws("kode_akses")
                    ws.update_cell(i + 2, 6, "Kadaluarsa")
                    return None, "Kode ini sudah kadaluarsa (lebih dari 7 hari)."
            except ValueError:
                pass
            return rec, "OK"
    return None, "Kode tidak ditemukan."


def pakai_kode(kode: str, nama_siswa: str):
    """Tandai kode sebagai Terpakai."""
    ws = get_ws("kode_akses")
    records = ws.get_all_records()
    tanggal = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for i, rec in enumerate(records):
        if str(rec.get("kode", "")).strip().upper() == kode.strip().upper():
            ws.update_cell(i + 2, 6, "Terpakai")
            ws.update_cell(i + 2, 8, tanggal)
            if not rec.get("dibeli_oleh"):
                ws.update_cell(i + 2, 5, nama_siswa)
            return True
    return False


# ---------------------------------------------------------------------------
# SISWA
# ---------------------------------------------------------------------------

def cari_siswa(nama: str):
    records = get_all_records("siswa")
    for rec in records:
        if str(rec.get("nama", "")).strip().lower() == nama.strip().lower():
            return rec
    return None


def daftar_siswa_baru(nama: str, kelas: str, level: int = 0, sub_level: int = 1):
    ws = get_ws("siswa")
    tanggal = datetime.datetime.now().strftime("%Y-%m-%d")
    ws.append_row([nama, kelas, level, sub_level, "Aktif", tanggal])


def update_progress_siswa(nama: str, level: int, sub_level: int):
    ws = get_ws("siswa")
    records = ws.get_all_records()
    for i, rec in enumerate(records):
        if str(rec.get("nama", "")).strip().lower() == nama.strip().lower():
            ws.update_cell(i + 2, 3, level)
            ws.update_cell(i + 2, 4, sub_level)
            return True
    return False


# ---------------------------------------------------------------------------
# RIWAYAT
# ---------------------------------------------------------------------------

def catat_riwayat(nama: str, level: int, sub_level: int, skor: float, status: str):
    ws = get_ws("riwayat")
    tanggal = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ws.append_row([tanggal, nama, level, sub_level, skor, status])


def riwayat_siswa(nama: str):
    records = get_all_records("riwayat")
    return [r for r in records if str(r.get("nama", "")).strip().lower() == nama.strip().lower()]


# ---------------------------------------------------------------------------
# PRETEST
# ---------------------------------------------------------------------------

def catat_pretest(nama: str, skor: float, level_awal: int, sub_level_awal: int):
    ws = get_ws("pretest")
    tanggal = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ws.append_row([nama, skor, level_awal, sub_level_awal, tanggal])
