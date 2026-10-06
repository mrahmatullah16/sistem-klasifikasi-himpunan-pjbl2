import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib_venn import venn2, venn3

# Set Konfigurasi Halaman Streamlit
st.set_page_config(
    page_title="Sistem Klasifikasi Data Himpunan",
    page_icon="🔢",
    layout="wide"
)

# ---------------------------------------------------------
# ANIMASI & STYLING CUSTOM (ADAPTIF MODE TERANG & GELAP)
# Warna teks & latar mengikuti tema Streamlit, sehingga tetap
# jelas di mode terang maupun gelap.
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@700;800&display=swap');

    /* ===== Variabel warna (semi-transparan agar cocok di terang & gelap) ===== */
    :root {
        --teal: #0E8C8C;
        --teal-2: #0B6E8A;
        --coral: #F2674F;
        --gold: #F4B73F;
        --line: rgba(128, 128, 128, 0.30);
        --card: rgba(128, 128, 128, 0.09);
        --shadow: 0 6px 16px rgba(0, 0, 0, 0.12);
    }

    /* ===== Font: Inter untuk teks penjelasan, Plus Jakarta Sans untuk judul ===== */
    html, body, .stApp, button, input, textarea, select {
        font-family: 'Inter', 'Segoe UI', Roboto, Arial, sans-serif;
    }
    h1, h2, h3, h4 {
        font-family: 'Plus Jakarta Sans', 'Inter', 'Segoe UI', Arial, sans-serif !important;
    }
    /* Pastikan ikon bawaan Streamlit tidak ikut berubah font */
    .stApp [data-testid="stIconMaterial"] {
        font-family: 'Material Symbols Rounded' !important;
    }

    /* ===== Teks penjelasan: lebih besar, jarak baris lega, warna mengikuti tema ===== */
    .stMarkdown p, .stMarkdown li, .stText, div[data-testid="stAlert"] p {
        font-size: 1.08rem;
        line-height: 1.8;
        font-weight: 400;
        letter-spacing: 0.1px;
    }
    .stMarkdown strong { font-weight: 700; }
    div[data-testid="stCaptionContainer"] p {
        font-size: 0.95rem;
        line-height: 1.6;
        opacity: 0.8;
    }
    div[data-testid="stWidgetLabel"] p {
        font-size: 1.02rem;
        font-weight: 600;
    }

    /* ===== Latar halaman: hanya menambah cahaya lembut di atas warna tema ===== */
    .stApp {
        background-image:
            radial-gradient(circle at 8% 8%, rgba(14, 140, 140, 0.14) 0, transparent 38%),
            radial-gradient(circle at 94% 4%, rgba(242, 103, 79, 0.11) 0, transparent 34%);
        background-attachment: fixed;
    }
    .block-container {
        padding-top: 2.2rem;
        padding-left: 2.5rem;
        padding-right: 2.5rem;
        max-width: 1380px;
    }

    /* ===== Animasi halaman muncul ===== */
    .main {
        animation: fadeIn 0.8s ease-in-out;
    }
    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(10px); }
        100% { opacity: 1; transform: translateY(0); }
    }

    /* ===== Banner judul dengan lingkaran Venn bergerak ===== */
    h1 {
        position: relative;
        overflow: hidden;
        background: linear-gradient(120deg, #14213D 0%, #0E5E73 60%, #0E8C8C 100%);
        color: #FFFFFF !important;
        font-size: 2.2rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.3px;
        line-height: 1.3 !important;
        padding: 1.6rem 2rem 1.4rem 2rem !important;
        border-radius: 18px;
        box-shadow: 0 14px 30px rgba(0, 0, 0, 0.25);
        margin-bottom: 0.3rem;
    }
    h1 span, h1 div { color: #FFFFFF !important; }
    h1 a { display: none !important; }
    h1::before, h1::after {
        content: "";
        position: absolute;
        width: 190px;
        height: 190px;
        border-radius: 50%;
        pointer-events: none;
    }
    h1::before {
        right: 90px; top: -50px;
        background: rgba(244, 183, 63, 0.32);
        animation: floatA 7s ease-in-out infinite;
    }
    h1::after {
        right: 10px; top: -20px;
        background: rgba(242, 103, 79, 0.32);
        animation: floatB 8s ease-in-out infinite;
    }
    @keyframes floatA {
        0%, 100% { transform: translate(0, 0); }
        50% { transform: translate(-18px, 10px); }
    }
    @keyframes floatB {
        0%, 100% { transform: translate(0, 0); }
        50% { transform: translate(14px, -8px); }
    }

    /* ===== Sub judul & pemisah ===== */
    h3 {
        font-size: 1.45rem !important;
        font-weight: 700 !important;
        border-left: 6px solid var(--teal);
        padding-left: 0.7rem !important;
    }
    h4 {
        font-size: 1.2rem !important;
        font-weight: 700 !important;
    }
    hr {
        border: none !important;
        height: 3px !important;
        background: linear-gradient(90deg, var(--teal), var(--gold), var(--coral)) !important;
        border-radius: 3px;
        opacity: 0.6;
        margin: 1.4rem 0 !important;
    }

    /* ===== Sidebar ===== */
    section[data-testid="stSidebar"] {
        background-image: linear-gradient(180deg, rgba(14, 140, 140, 0.14), rgba(14, 140, 140, 0.02));
        border-right: 1px solid var(--line);
    }
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        border-left: none;
        padding-left: 0 !important;
        font-size: 1.25rem !important;
    }
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown li {
        font-size: 1rem;
        line-height: 1.75;
    }

    /* ===== Kartu Metric ===== */
    div[data-testid="stMetric"] {
        background: var(--card);
        border: 1px solid var(--line);
        border-top: 5px solid var(--teal);
        padding: 14px 16px;
        border-radius: 14px;
        box-shadow: var(--shadow);
        transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
        animation: popIn 0.6s cubic-bezier(.2, .8, .2, 1) both;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-6px) scale(1.02);
        box-shadow: 0px 14px 24px rgba(14, 140, 140, 0.28);
        border-top-color: var(--coral);
    }
    div[data-testid="stMetric"] label p {
        font-size: 1rem !important;
        font-weight: 600 !important;
        opacity: 0.85;
    }
    div[data-testid="stMetricValue"],
    div[data-testid="stMetricValue"] div {
        font-size: 1.7rem !important;
        font-weight: 800 !important;
    }
    @keyframes popIn {
        0% { opacity: 0; transform: translateY(18px) scale(0.96); }
        100% { opacity: 1; transform: translateY(0) scale(1); }
    }
    div[data-testid="stHorizontalBlock"] > div:nth-child(1) div[data-testid="stMetric"] { animation-delay: 0.05s; }
    div[data-testid="stHorizontalBlock"] > div:nth-child(2) div[data-testid="stMetric"] { animation-delay: 0.15s; }
    div[data-testid="stHorizontalBlock"] > div:nth-child(3) div[data-testid="stMetric"] { animation-delay: 0.25s; }
    div[data-testid="stHorizontalBlock"] > div:nth-child(4) div[data-testid="stMetric"] { animation-delay: 0.35s; }
    div[data-testid="stHorizontalBlock"] > div:nth-child(5) div[data-testid="stMetric"] { animation-delay: 0.45s; }

    /* ===== Radio berbentuk tombol (pill) ===== */
    div[role="radiogroup"] { gap: 0.5rem; }
    div[role="radiogroup"] label[data-baseweb="radio"] {
        background: var(--card);
        border: 2px solid var(--line);
        border-radius: 999px;
        padding: 0.45rem 1.1rem;
        margin: 0;
        cursor: pointer;
        transition: all 0.25s ease;
    }
    div[role="radiogroup"] label[data-baseweb="radio"] > div:first-child {
        display: none;
    }
    div[role="radiogroup"] label[data-baseweb="radio"] p {
        font-size: 1.02rem;
        font-weight: 600;
        line-height: 1.5;
    }
    div[role="radiogroup"] label[data-baseweb="radio"]:hover {
        border-color: var(--teal);
        transform: translateY(-2px);
        box-shadow: 0 6px 14px rgba(14, 140, 140, 0.22);
    }
    div[role="radiogroup"] label[data-baseweb="radio"]:has(input:checked) {
        background: linear-gradient(120deg, var(--teal), var(--teal-2));
        border-color: var(--teal);
        box-shadow: 0 8px 16px rgba(14, 140, 140, 0.35);
    }
    div[role="radiogroup"] label[data-baseweb="radio"]:has(input:checked) p,
    div[role="radiogroup"] label[data-baseweb="radio"]:has(input:checked) div {
        color: #FFFFFF !important;
    }

    /* ===== Input ===== */
    div[data-baseweb="select"] > div {
        border: 2px solid var(--line);
        border-radius: 12px;
        min-height: 46px;
        transition: border-color 0.25s ease, box-shadow 0.25s ease;
    }
    div[data-baseweb="select"] > div:hover,
    div[data-baseweb="select"] > div:focus-within {
        border-color: var(--teal);
        box-shadow: 0 0 0 4px rgba(14, 140, 140, 0.20);
    }
    span[data-baseweb="tag"] {
        background: var(--teal) !important;
        border-radius: 8px;
    }
    span[data-baseweb="tag"] span { color: #FFFFFF !important; font-weight: 600; }
    div[data-testid="stFileUploaderDropzone"] {
        border: 2px dashed var(--teal);
        border-radius: 14px;
        transition: background 0.3s ease, transform 0.3s ease;
    }
    div[data-testid="stFileUploaderDropzone"]:hover {
        background: rgba(14, 140, 140, 0.14);
        transform: scale(1.01);
    }

    /* ===== Slider ===== */
    div[data-testid="stSlider"] div[role="slider"] {
        background: var(--coral) !important;
        box-shadow: 0 0 0 5px rgba(242, 103, 79, 0.25);
        transition: box-shadow 0.25s ease;
    }
    div[data-testid="stSlider"] div[role="slider"]:hover {
        box-shadow: 0 0 0 9px rgba(242, 103, 79, 0.25);
    }

    /* ===== Expander ===== */
    div[data-testid="stExpander"] {
        border: 1px solid var(--line);
        border-radius: 14px;
        background: var(--card);
        box-shadow: var(--shadow);
        animation: slideUp 0.5s ease both;
    }
    div[data-testid="stExpander"] summary p {
        font-size: 1.08rem;
        font-weight: 400 !important;
    }

    /* ===== Tabel & grafik ===== */
    div[data-testid="stDataFrame"] {
        border: 1px solid var(--line);
        border-radius: 14px;
        padding: 4px;
        box-shadow: var(--shadow);
        animation: slideUp 0.6s ease both;
    }
    div[data-testid="stImage"] img,
    div[data-testid="stPyplot"] img {
        background: #FFFFFF;
        border: 1px solid var(--line);
        border-radius: 16px;
        padding: 10px;
        box-shadow: var(--shadow);
        animation: slideUp 0.7s ease both;
    }
    @keyframes slideUp {
        0% { opacity: 0; transform: translateY(16px); }
        100% { opacity: 1; transform: translateY(0); }
    }

    /* ===== Tombol ===== */
    div[data-testid="stDownloadButton"] button,
    div[data-testid="stButton"] button {
        background: linear-gradient(120deg, var(--coral), #E8503A);
        color: #FFFFFF;
        border: none;
        border-radius: 12px;
        padding: 0.7rem 1.4rem;
        box-shadow: 0 8px 16px rgba(242, 103, 79, 0.32);
        transition: transform 0.25s ease, box-shadow 0.25s ease;
    }
    div[data-testid="stDownloadButton"] button p,
    div[data-testid="stButton"] button p {
        color: #FFFFFF !important;
        font-size: 1.02rem;
        font-weight: 700;
    }
    div[data-testid="stDownloadButton"] button:hover,
    div[data-testid="stButton"] button:hover {
        transform: translateY(-3px);
        box-shadow: 0 14px 22px rgba(242, 103, 79, 0.42);
    }
    div[data-testid="stDownloadButton"] button:active { transform: translateY(0) scale(0.98); }

    /* ===== Tombol unduh: kecil, outline teal, isi teal menyapu dari kiri saat hover ===== */
    div[data-testid="stDownloadButton"] button {
        position: relative;
        overflow: hidden;
        background: transparent;
        border: 2px solid var(--teal);
        border-radius: 10px;
        padding: 0.4rem 1.1rem;
        min-height: 0;
        box-shadow: none;
        animation: none;
        transition: transform 0.25s ease, box-shadow 0.25s ease;
    }
    div[data-testid="stDownloadButton"] button::before {
        content: "";
        position: absolute;
        inset: 0;
        background: linear-gradient(120deg, var(--teal), var(--teal-2));
        transform: translateX(-101%);
        transition: transform 0.4s cubic-bezier(.2, .8, .2, 1);
    }
    div[data-testid="stDownloadButton"] button > * {
        position: relative;
        z-index: 1;
    }
    div[data-testid="stDownloadButton"] button p {
        color: var(--teal) !important;
        font-size: 0.92rem;
        font-weight: 600;
        line-height: 1.5;
        transition: color 0.3s ease;
    }
    div[data-testid="stDownloadButton"] button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(14, 140, 140, 0.30);
        animation: none;
    }
    div[data-testid="stDownloadButton"] button:hover::before { transform: translateX(0); }
    div[data-testid="stDownloadButton"] button:hover p { color: #FFFFFF !important; }
    div[data-testid="stDownloadButton"] button:active { transform: translateY(0) scale(0.98); }

    /* ===== Kotak pesan: animasi sederhana (muncul memudar + naik sedikit) ===== */
    div[data-testid="stAlert"] {
        border-radius: 14px;
        box-shadow: var(--shadow);
        animation: alertRise 0.5s ease-out both;
    }
    @keyframes alertRise {
        0% { opacity: 0; transform: translateY(10px); }
        100% { opacity: 1; transform: translateY(0); }
    }

    /* ===== Rumus LaTeX ===== */
    .katex-display {
        background: var(--card);
        border: 1px solid var(--line);
        border-left: 6px solid var(--gold);
        border-radius: 14px;
        padding: 1rem 0.8rem;
        box-shadow: var(--shadow);
        overflow-x: auto;
    }

    /* ===== Hormati pengguna yang mematikan animasi ===== */
    @media (prefers-reduced-motion: reduce) {
        *, *::before, *::after {
            animation: none !important;
            transition: none !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# Judul Utama
st.title("🔢 Sistem Klasifikasi Data dengan Himpunan (PJBL-2)")
st.caption("Proyek Matematika Diskrit - Kelompok 2")

# Sidebar: Identitas & Pilihan Dataset
st.sidebar.header("📋 Pengaturan & Informasi")
st.sidebar.markdown("**Kelompok 2:**")
st.sidebar.markdown("""
1. Iman Zandra (25210387)
2. M. Rahmatullah (25210376)
3. T. Ilham Ramadhan (25210362)
4. Satya Utama Efendi (25210342)
5. Ali Rifaiz Syahputra (25210345)
6. Saifal Iman (25210151)
7. Mahdi Sayyidul Sirja (25210160)
""")

# Fitur Upload Custom CSV / Switcher Dataset
st.sidebar.subheader("📂 Sumber Data")
opsi_sumber = st.sidebar.radio("Pilih Sumber Dataset:", ["Dataset Bawaan (Preset)", "Upload File CSV Sendiri"])

@st.cache_data
def load_data(file_path):
    try:
        return pd.read_csv(file_path)
    except Exception:
        # Fallback dummy data jika file CSV tidak ditemukan
        return pd.DataFrame({
            'ID': ['01', '02', '03'],
            'Nama_Produk': ['Produk A', 'Produk B', 'Produk C'],
            'Kategori': ['Kat 1', 'Kat 2', 'Kat 1'],
            'Harga': [100000, 200000, 150000],
            'Rating': [4.5, 4.2, 4.8]
        })

if opsi_sumber == "Dataset Bawaan (Preset)":
    pilihan_dataset = st.sidebar.selectbox(
        "Ganti Dataset Contoh:",
        ["Dataset 1: Elektronik & Aksesori", "Dataset 2: Fashion & Pakaian"]
    )
    if pilihan_dataset == "Dataset 1: Elektronik & Aksesori":
        df = load_data("dataset1_elektronik.csv")
    else:
        df = load_data("dataset2_fashion.csv")
else:
    uploaded_file = st.sidebar.file_uploader("Unggah File CSV Dataset:", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.toast("⚡ File CSV berhasil diunggah!", icon="🎉")
    else:
        st.sidebar.warning("⚠️ Silakan unggah file CSV. Menggunakan data default sementara.")
        df = load_data("dataset1_elektronik.csv")

# Kustomisasi Warna Diagram Venn pada Sidebar
st.sidebar.subheader("🎨 Skema Warna Diagram Venn")
skema_warna = st.sidebar.selectbox("Pilih Warna Venn:", ["Set1", "Set2", "Pastel1", "Viridis", "Accent"])

# Tampilkan Dataset Awal
st.subheader("📊 Dataset Semesta (U)")
st.dataframe(df, use_container_width=True)

# Kriteria Pemfilteran Himpunan
st.markdown("---")
st.subheader("🎯 Pemodelan & Filter Himpunan")

col_f1, col_f2, col_f3 = st.columns(3)

# Pastikan kolom sesuai tipe data
kolom_kategori = 'Kategori' if 'Kategori' in df.columns else df.columns[2]
kolom_harga = 'Harga' if 'Harga' in df.columns else df.columns[3]
kolom_rating = 'Rating' if 'Rating' in df.columns else df.columns[4]

with col_f1:
    st.markdown("### Himpunan A")
    kat_pilihan = st.multiselect("Pilih Kategori (Himpunan A):", 
                               options=df[kolom_kategori].unique(), 
                               default=[df[kolom_kategori].unique()[0]])

with col_f2:
    st.markdown("### Himpunan B")
    harga_max = st.slider("Batas Maksimal Harga (Rp) (Himpunan B):", 
                          min_value=int(df[kolom_harga].min()), 
                          max_value=int(df[kolom_harga].max()), 
                          value=int(df[kolom_harga].median()))

with col_f3:
    st.markdown("### Himpunan C")
    rating_min = st.slider("Minimum Rating (Himpunan C):", 
                           min_value=float(df[kolom_rating].min()), 
                           max_value=float(df[kolom_rating].max()), 
                           value=float(df[kolom_rating].mean()), step=0.1)

# Pembentukan Set Elemen (ID Produk)
kolom_id = 'ID' if 'ID' in df.columns else df.columns[0]
set_U = set(df[kolom_id])
set_A = set(df[df[kolom_kategori].isin(kat_pilihan)][kolom_id])
set_B = set(df[df[kolom_harga] <= harga_max][kolom_id])
set_C = set(df[df[kolom_rating] >= rating_min][kolom_id])

# Fitur Tambahan: Ringkasan Statistik Metrics Card
st.markdown("#### 📈 Ringkasan Ukuran Himpunan")
col_m1, col_m2, col_m3, col_m4, col_m5 = st.columns(5)
col_m1.metric("Semesta |U|", f"{len(set_U)} Produk")
col_m2.metric("Ukuran |A|", f"{len(set_A)} Produk")
col_m3.metric("Ukuran |B|", f"{len(set_B)} Produk")
col_m4.metric("Ukuran |C|", f"{len(set_C)} Produk")
col_m5.metric("Irisan |A∩B∩C|", f"{len(set_A & set_B & set_C)} Produk")


# Fungsi bantu untuk menampilkan anggota himpunan sebagai teks
def tampil_anggota(himpunan):
    if len(himpunan) == 0:
        return "∅ (himpunan kosong)"
    return ", ".join(sorted(map(str, himpunan)))


# FITUR BARU 1: Daftar Anggota Tiap Himpunan
with st.expander("🔍 Lihat Daftar Anggota Tiap Himpunan (ID Produk)"):
    st.markdown(f"**Himpunan A** ({len(set_A)} anggota): {tampil_anggota(set_A)}")
    st.markdown(f"**Himpunan B** ({len(set_B)} anggota): {tampil_anggota(set_B)}")
    st.markdown(f"**Himpunan C** ({len(set_C)} anggota): {tampil_anggota(set_C)}")

st.markdown("---")

# Menggunakan Radio Navigasi Berpenampilan Segmented / Tab
# Hal ini memungkinkan Streamlit mendeteksi secara presisi kapan Tab 3 diklik oleh pengguna
pilihan_tab = st.radio(
    "Navigasi Fitur Aplikasi:",
    ["⚡ Operasi Himpunan", "🎨 Diagram Venn Otomatis", "🧮 Prinsip Inklusi-Eksklusi (PIE)", "⚖️ Verifikasi Hukum Himpunan"],
    horizontal=True
)

# TAB 1: OPERASI HIMPUNAN
if pilihan_tab == "⚡ Operasi Himpunan":
    st.subheader("Katalog Operasi Himpunan")
    
    jenis_operasi = st.selectbox(
        "Pilih Operasi Himpunan:",
        [
            "Gabungan A ∪ B",
            "Irisan A ∩ B",
            "Selisih A - B",
            "Selisih B - A",
            "Komplemen A'",
            "Komplemen B'",
            "Komplemen C'",
            "Irisan 3 Himpunan A ∩ B ∩ C",
            "Gabungan 3 Himpunan A ∪ B ∪ C"
        ]
    )
    
    if jenis_operasi == "Gabungan A ∪ B":
        hasil_set = set_A | set_B
        rumus_label = "A ∪ B"
    elif jenis_operasi == "Irisan A ∩ B":
        hasil_set = set_A & set_B
        rumus_label = "A ∩ B"
    elif jenis_operasi == "Selisih A - B":
        hasil_set = set_A - set_B
        rumus_label = "A - B"
    elif jenis_operasi == "Selisih B - A":
        hasil_set = set_B - set_A
        rumus_label = "B - A"
    elif jenis_operasi == "Komplemen A'":
        hasil_set = set_U - set_A
        rumus_label = "A'"
    elif jenis_operasi == "Komplemen B'":
        hasil_set = set_U - set_B
        rumus_label = "B'"
    elif jenis_operasi == "Komplemen C'":
        hasil_set = set_U - set_C
        rumus_label = "C'"
    elif jenis_operasi == "Irisan 3 Himpunan A ∩ B ∩ C":
        hasil_set = set_A & set_B & set_C
        rumus_label = "A ∩ B ∩ C"
    elif jenis_operasi == "Gabungan 3 Himpunan A ∪ B ∪ C":
        hasil_set = set_A | set_B | set_C
        rumus_label = "A ∪ B ∪ C"

    df_hasil = df[df[kolom_id].isin(hasil_set)]
    
    st.markdown(f"**Hasil Operasi ({rumus_label}):** {len(hasil_set)} Produk Ditemukan")
    st.dataframe(df_hasil, use_container_width=True)
    
    # Fitur Tambahan: Export Hasil ke CSV
    csv_data = df_hasil.to_csv(index=False).encode('utf-8')
    st.download_button(
        label=f"📥 Unduh Hasil Filter ({rumus_label}) sebagai CSV",
        data=csv_data,
        file_name=f"hasil_operasi_{rumus_label.replace(' ', '_')}.csv",
        mime="text/csv"
    )

# TAB 2: DIAGRAM VENN OTOMATIS
elif pilihan_tab == "🎨 Diagram Venn Otomatis":
    st.subheader("Visualisasi Diagram Venn")
    
    opsi_venn = st.radio("Tampilkan Diagram Venn untuk:", ["2 Himpunan (A & B)", "3 Himpunan (A, B, & C)"])
    
    fig, ax = plt.subplots(figsize=(8, 6))
    cmap = plt.get_cmap(skema_warna)
    
    if opsi_venn == "2 Himpunan (A & B)":
        v2 = venn2(subsets=(len(set_A - set_B), len(set_B - set_A), len(set_A & set_B)),
                   set_labels=('Himpunan A', 'Himpunan B'), ax=ax)
        if v2:
            for patch, color in zip(v2.patches, [cmap(0.2), cmap(0.5), cmap(0.8)]):
                if patch:
                    patch.set_facecolor(color)
                    patch.set_alpha(0.6)
        plt.title("Diagram Venn 2 Himpunan (A & B)")
    else:
        v3 = venn3(subsets=(
            len(set_A - (set_B | set_C)),                  # 100
            len(set_B - (set_A | set_C)),                  # 010
            len((set_A & set_B) - set_C),                 # 110
            len(set_C - (set_A | set_B)),                  # 001
            len((set_A & set_C) - set_B),                 # 101
            len((set_B & set_C) - set_A),                 # 011
            len(set_A & set_B & set_C)                    # 111
        ), set_labels=('Himpunan A', 'Himpunan B', 'Himpunan C'), ax=ax)
        if v3:
            for patch in v3.patches:
                if patch:
                    patch.set_alpha(0.6)
        plt.title("Diagram Venn 3 Himpunan (A, B, & C)")
        
    st.pyplot(fig)

    # FITUR BARU 2: Rincian anggota tiap daerah pada diagram Venn
    st.markdown("#### 📌 Rincian Anggota Tiap Daerah Diagram")
    if opsi_venn == "2 Himpunan (A & B)":
        daerah_venn = [
            ("Hanya A (A - B)", set_A - set_B),
            ("Hanya B (B - A)", set_B - set_A),
            ("Irisan A ∩ B", set_A & set_B),
            ("Di luar A dan B", set_U - (set_A | set_B)),
        ]
    else:
        daerah_venn = [
            ("Hanya A", set_A - (set_B | set_C)),
            ("Hanya B", set_B - (set_A | set_C)),
            ("Hanya C", set_C - (set_A | set_B)),
            ("Irisan A ∩ B saja", (set_A & set_B) - set_C),
            ("Irisan A ∩ C saja", (set_A & set_C) - set_B),
            ("Irisan B ∩ C saja", (set_B & set_C) - set_A),
            ("Irisan A ∩ B ∩ C", set_A & set_B & set_C),
            ("Di luar A, B, dan C", set_U - (set_A | set_B | set_C)),
        ]
    df_daerah = pd.DataFrame({
        "Daerah": [nama for nama, _ in daerah_venn],
        "Jumlah": [len(isi) for _, isi in daerah_venn],
        "Anggota (ID Produk)": [tampil_anggota(isi) for _, isi in daerah_venn],
    })
    st.dataframe(df_daerah, use_container_width=True, hide_index=True)

# TAB 3: PRINSIP INKLUSI-EKSKLUSI (PIE)
elif pilihan_tab == "🧮 Prinsip Inklusi-Eksklusi (PIE)":
    st.subheader("Kalkulasi Prinsip Inklusi-Eksklusi (PIE)")
    
    st.markdown("Formula Perhitungan Unik 3 Himpunan:")
    st.latex(r"|A \cup B \cup C| = |A| + |B| + |C| - |A \cap B| - |A \cap C| - |B \cap C| + |A \cap B \cap C|")
    
    # Elemen PIE
    nA = len(set_A)
    nB = len(set_B)
    nC = len(set_C)
    nAB = len(set_A & set_B)
    nAC = len(set_A & set_C)
    nBC = len(set_B & set_C)
    nABC = len(set_A & set_B & set_C)
    
    total_pie = nA + nB + nC - nAB - nAC - nBC + nABC
    total_riil = len(set_A | set_B | set_C)
    
    st.markdown("### Rincian Perhitungan:")
    col_p1, col_p2 = st.columns(2)
    
    with col_p1:
        st.write(f"- |A| = {nA}")
        st.write(f"- |B| = {nB}")
        st.write(f"- |C| = {nC}")
        st.write(f"- |A ∩ B| = {nAB}")
    with col_p2:
        st.write(f"- |A ∩ C| = {nAC}")
        st.write(f"- |B ∩ C| = {nBC}")
        st.write(f"- |A ∩ B ∩ C| = {nABC}")
        
    st.info(f"**Substitusi Rumus:** {nA} + {nB} + {nC} - {nAB} - {nAC} - {nBC} + {nABC} = **{total_pie}**")
    
    # ANIMASI HANYA MUNCUL KETIKA PENGGUNA MEMILIH / MENGKLIK TAB 3 INI
    if total_pie == total_riil:
        st.balloons()  # Balon langsung meluncur tepat saat Tab 3 diklik
        st.success(f"✅ **Verifikasi Berhasil!** Hasil perhitungan PIE ({total_pie}) persis sama dengan jumlah gabungan riil di tabel ({total_riil}).")
    else:
        st.snow()      # Salju turun jika verifikasi gagal
        st.error(f"❌ **Verifikasi Gagal!** Perhitungan PIE ({total_pie}) tidak sesuai dengan jumlah gabungan riil di tabel ({total_riil}).")

# TAB 4 (FITUR BARU 3): VERIFIKASI HUKUM HIMPUNAN
elif pilihan_tab == "⚖️ Verifikasi Hukum Himpunan":
    st.subheader("Verifikasi Hukum-Hukum Himpunan pada Data")
    st.markdown(
        "Setiap hukum dihitung langsung dari himpunan A, B, dan C hasil filter di atas. "
        "Jika ruas kiri dan ruas kanan beranggotakan sama persis, hukum tersebut **terbukti** pada data ini."
    )

    daftar_hukum = [
        ("De Morgan 1", "(A ∪ B)' = A' ∩ B'",
         set_U - (set_A | set_B), (set_U - set_A) & (set_U - set_B)),
        ("De Morgan 2", "(A ∩ B)' = A' ∪ B'",
         set_U - (set_A & set_B), (set_U - set_A) | (set_U - set_B)),
        ("Distributif 1", "A ∩ (B ∪ C) = (A ∩ B) ∪ (A ∩ C)",
         set_A & (set_B | set_C), (set_A & set_B) | (set_A & set_C)),
        ("Distributif 2", "A ∪ (B ∩ C) = (A ∪ B) ∩ (A ∪ C)",
         set_A | (set_B & set_C), (set_A | set_B) & (set_A | set_C)),
        ("Komplemen Ganda", "(A')' = A",
         set_U - (set_U - set_A), set_A),
        ("Hukum Komplemen", "A ∪ A' = U",
         set_A | (set_U - set_A), set_U),
    ]

    baris_hukum = []
    for nama_hukum, rumus_hukum, kiri, kanan in daftar_hukum:
        baris_hukum.append({
            "Hukum": nama_hukum,
            "Persamaan": rumus_hukum,
            "|Ruas Kiri|": len(kiri),
            "|Ruas Kanan|": len(kanan),
            "Status": "✅ Terbukti" if kiri == kanan else "❌ Tidak sama",
        })

    st.dataframe(pd.DataFrame(baris_hukum), use_container_width=True, hide_index=True)

    if all(kiri == kanan for _, _, kiri, kanan in daftar_hukum):
        st.success("✅ **Semua hukum himpunan terbukti** pada dataset dan filter yang sedang dipakai.")
    else:
        st.error("❌ Ada hukum yang tidak sama. Periksa kembali dataset atau filter yang dipilih.")