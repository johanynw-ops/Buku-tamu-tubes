import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="Buku Tamu Digital", layout="centered")

# ==========================
# 1. Google Sheets Connector
# ==========================
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=scope
)

client = gspread.authorize(creds)

# Gunakan ID Google Sheet kamu
SHEET_ID = "1vTCOg7uD6bX7PwYrclBNOBbR3TU3no_sSRzRYOXilq0"

try:
    sheet = client.open_by_key(SHEET_ID).sheet1
except Exception as e:
    st.error(f"❌ Google Sheet tidak ditemukan atau tidak ada akses.\n\nError: {e}")
    st.stop()

# ==========================
# 2. Sidebar Menu
# ==========================
menu = st.sidebar.radio("Menu", ["Isi Buku Tamu", "Lihat Data Tamu"])

# ==========================
# 3. FORM INPUT BUKU TAMU
# ==========================
if menu == "Isi Buku Tamu":

    st.title("📘 Buku Tamu Digital")
    st.write("Silakan isi data berikut:")

    with st.form("form_bukutamu"):
        nama = st.text_input("Nama")
        email = st.text_input("Email")
        pesan = st.text_area("Pesan / Keperluan")

        submit = st.form_submit_button("Kirim")

    if submit:
        if not nama:
            st.warning("⚠ Nama wajib diisi!")
        else:
            sheet.append_row([
                nama,
                email,
                pesan,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ])
            st.success("✅ Terima kasih! Data berhasil disimpan.")

# ==========================
# 4. HALAMAN ADMIN – MELIHAT DATA
# ==========================
elif menu == "Lihat Data Tamu":

    st.title("📄 Data Tamu Masuk")

    data = sheet.get_all_records()
    df = pd.DataFrame(data)

    if df.empty:
        st.info("Belum ada data tamu.")
    else:
        st.dataframe(df)

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("⬇ Download CSV", csv, "data_buku_tamu.csv", "text/csv")
