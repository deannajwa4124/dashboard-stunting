import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ============================================
# CONFIG
# ============================================
st.set_page_config(
    page_title="Dashboard Stunting",
    layout="wide",
    page_icon="🧒",
    initial_sidebar_state="expanded"
)

sns.set_style("whitegrid")

# CSS
st.markdown("""
<style>
.big-title { font-size:40px; font-weight:800; color:#2B547E; margin-bottom:-10px; }
.sub-title { font-size:18px; color:#777; margin-top:-10px; }
.metric-card {
    padding:18px; background:#f8f9fa; border-radius:13px;
    border:1px solid #ddd; text-align:center;
    box-shadow:1px 1px 5px rgba(0,0,0,0.07);
}
</style>
""", unsafe_allow_html=True)


# ============================================
# LOAD DATA
# ============================================
df_raw = pd.read_excel("data clean diskretisasi.xlsx")
df = df_raw.copy()

# ============================================
# RENAME KOLOM
# ============================================
rename_cols = {
    "Provinsi": "Provinsi",
    "Jenis Kelamin": "Jenis Kelamin",
    "Mengetahui Ttg Stunting": "Pengetahuan Stunting",
    "Kepemilikan JKesehatan": "Jaminan Kesehatan",
    "Umur_Bulan": "Umur Bulan",
    "Lingkar_Kepala_Bayi": "Lingkar Kepala Bayi",
    "BB_Lahir": "Berat Lahir",
    "PB_Lahir": "Panjang Lahir",
    "PB_Saat_Ini": "Panjang Badan Sekarang",
    "Usia_Kehamilan": "Usia Kehamilan",
    "kategori_bl": "Kategori Berat Lahir",
    "kategori_Umur_Bulan": "Kategori Umur Bulan"
}

df = df.rename(columns=rename_cols)


# ============================================
# MAPPING KATEGORI
# ============================================

# ---- Provinsi BPS (11–96) ----
map_prov = {
    11:"Aceh", 12:"Sumatera Utara", 13:"Sumatera Barat", 14:"Riau", 15:"Jambi",
    16:"Sumatera Selatan", 17:"Bengkulu", 18:"Lampung", 19:"Bangka Belitung",
    21:"Kepulauan Riau",

    31:"DKI Jakarta", 32:"Jawa Barat", 33:"Jawa Tengah", 34:"DI Yogyakarta",
    35:"Jawa Timur", 36:"Banten",

    51:"Bali", 52:"NTB", 53:"NTT",

    61:"Kalimantan Barat", 62:"Kalimantan Tengah", 63:"Kalimantan Selatan",
    64:"Kalimantan Timur", 65:"Kalimantan Utara",

    71:"Sulawesi Utara", 72:"Sulawesi Tengah", 73:"Sulawesi Selatan",
    74:"Sulawesi Tenggara", 75:"Gorontalo", 76:"Sulawesi Barat",

    81:"Maluku", 82:"Maluku Utara",

    91:"Papua Barat", 92:"Papua Barat Daya", 94:"Papua",
    95:"Papua Selatan", 96:"Papua Tengah", 97:"Papua Pegunungan"
}

map_jk = {1:"Laki-laki", 2:"Perempuan"}
map_stunting = {1:"Ya", 2:"Tidak"}
map_jkn = {
    1:"BPJS PBI",
    2:"BPJS Non PBI",
    4:"Jamkesda",
    5:"BPJS PBI + Jamkesda",
    8:"Asuransi Swasta",
    10:"BPJS Non PBI + Asuransi Swasta",
    16:"Lainnya",
    32:"Tidak ada",
    99:"Kombinasi lain"
}

# Terapkan mapping
mapping_dict = {
    "Provinsi": map_prov,
    "Jenis Kelamin": map_jk,
    "Pengetahuan Stunting": map_stunting,
    "Jaminan Kesehatan": map_jkn
}

for col, mp in mapping_dict.items():
    if col in df.columns:
        df[col] = df[col].map(mp).astype("category")

# Pastikan kategori lain tetap kategori
extra_cats = ["Kategori Berat Lahir", "Kategori Umur Bulan"]
for col in extra_cats:
    if col in df.columns:
        df[col] = df[col].astype("category")


# ============================================
# SIDEBAR
# ============================================
st.sidebar.title("⚙️ Pengaturan Dashboard")

menu = st.sidebar.radio(
    "Pilih Halaman:",
    ["🏠 Home", "📋 Data", "🔍 Filter Data", "📈 Statistik", "📊 Visualisasi", "ℹ️ About"]
)

hapus_cols = st.sidebar.multiselect("Variabel tidak dibutuhkan:", df.columns)
if hapus_cols:
    df = df.drop(columns=hapus_cols)


# ============================================
# 1. HOME
# ============================================
if menu == "🏠 Home":
    st.markdown('<p class="big-title">Dashboard Stunting</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Ringkasan umum dataset</p>', unsafe_allow_html=True)
    st.write(" ")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Jumlah Baris", len(df))
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Jumlah Variabel", df.shape[1])
        st.markdown("</div>", unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Variabel Numerik", df.select_dtypes(include="number").shape[1])
        st.markdown("</div>", unsafe_allow_html=True)

    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Variabel Kategorik", df.select_dtypes(include="category").shape[1])
        st.markdown("</div>", unsafe_allow_html=True)

    st.subheader("📌 Statistik Numerik")
    st.dataframe(df.describe().T, use_container_width=True)

    # Informasi
    st.markdown("""
    ### 📝 Interpretasi Umum Dataset
    Dataset ini menggambarkan karakteristik anak serta faktor-faktor yang berkaitan
    dengan stunting, seperti umur, berat lahir, panjang badan, dan kondisi orang tua.
    Informasi tambahan seperti jenis kelamin, provinsi, dan kepemilikan jaminan kesehatan
    memberi gambaran konteks sosial dari data.

    Statistik numerik di atas membantu melihat bagaimana persebaran nilai penting seperti
    **umur**, **berat lahir**, dan **panjang badan**. Nilai mean, median, dan standar deviasi
    dapat digunakan untuk memahami apakah data tersebar merata atau terkonsentrasi pada
    kelompok tertentu.
    """)

# ============================================
# 2. DATA
# ============================================
elif menu == "📋 Data":
    st.title("📋 Data Lengkap")
    st.dataframe(df, use_container_width=True, height=600)


# ============================================
# 3. FILTER
# ============================================
elif menu == "🔍 Filter Data":
    st.title("🔍 Filter Interaktif")

    kategori_cols = df.select_dtypes("category").columns.tolist()
    num_cols = df.select_dtypes("number").columns.tolist()

    c1, c2, c3 = st.columns(3)

    # Filter Kategori 1
    with c1:
        var_kat1 = st.selectbox(
            "Pilih variabel kategori 1:",
            kategori_cols,
            key="kat1_var"
        )
        val_kat1 = st.multiselect(
            f"Nilai untuk {var_kat1}:",
            df[var_kat1].unique(),
            key="kat1_val"
        )

    # Filter Kategori 2
    with c2:
        var_kat2 = st.selectbox(
            "Pilih variabel kategori 2:",
            kategori_cols,
            key="kat2_var"
        )
        val_kat2 = st.multiselect(
            f"Nilai untuk {var_kat2}:",
            df[var_kat2].unique(),
            key="kat2_val"
        )

    # Filter Numerik
    with c3:
        var_num = st.selectbox(
            "Pilih variabel numerik:",
            num_cols,
            key="num_var"
        )
        min_v, max_v = st.slider(
            f"Rentang nilai {var_num}:",
            float(df[var_num].min()), float(df[var_num].max()),
            (float(df[var_num].min()), float(df[var_num].max())),
            key="num_slider"
        )

    # Apply Filter
    df_f = df.copy()

    if val_kat1:
        df_f = df_f[df_f[var_kat1].isin(val_kat1)]

    if val_kat2:
        df_f = df_f[df_f[var_kat2].isin(val_kat2)]

    df_f = df_f[df_f[var_num].between(min_v, max_v)]

    # OUTPUT FILTER
    st.subheader("📌 Hasil Filter")
    st.dataframe(df_f, use_container_width=True)

    # Statistik Hasil Filter
    if not df_f.empty:
        st.subheader("📊 Ringkasan Hasil Filter")

        colA, colB, colC = st.columns(3)
        colA.metric("Jumlah Data", len(df_f))
        colB.metric(f"Rata-rata {var_num}", round(df_f[var_num].mean(), 2))
        colC.metric(f"Median {var_num}", round(df_f[var_num].median(), 2))

        # Informasi
        st.markdown(f"""
        ### 📝 Kesimpulan Filter
        - **{var_kat1}** dipilih: `{", ".join(val_kat1) if val_kat1 else "Semua"}`
        - **{var_kat2}** dipilih: `{", ".join(val_kat2) if val_kat2 else "Semua"}`
        - **Rentang {var_num}**: {min_v} s/d {max_v}

        Data tersaring sebanyak **{len(df_f)} observasi**. Rata-rata nilai
        variabel **{var_num}** menunjukkan kecenderungan umum kelompok data yang dipilih,
        sehingga dapat membantu memahami pola stunting pada subset tertentu.
        """)

# ============================================
# 4. STATISTIK
# ============================================
elif menu == "📈 Statistik":
    st.title("📈 Statistik Deskriptif")

    num_cols = df.select_dtypes(include="number").columns
    st.subheader("📌 Statistik Numerik Lengkap")
    st.dataframe(df[num_cols].describe().T, use_container_width=True)

    st.subheader("📌 Boxplot Semua Variabel Numerik")
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.boxplot(data=df[num_cols], ax=ax)
    st.pyplot(fig)

    # Informasi
    st.markdown("""
    ### 📝 Interpretasi Boxplot
    Boxplot di atas menunjukkan sebaran data serta outlier yang mungkin muncul
    pada variabel numerik, seperti **umur**, **berat lahir**, dan **panjang badan**.
    Outlier dapat mengindikasikan kondisi ekstrem yang patut diperhatikan,
    misalnya berat lahir yang sangat rendah atau umur yang tidak lazim.

    Distribusi yang melebar juga memberikan gambaran bahwa karakteristik anak
    sangat bervariasi, dan hal ini penting ketika melakukan analisis stunting secara mendalam.
    """)


# ============================================
# 5. VISUALISASI
# ============================================
elif menu == "📊 Visualisasi":
    st.title("📊 Visualisasi Interaktif")

    chart_type = st.selectbox("Pilih jenis grafik:", ["Bar Chart", "Pie Chart", "Histogram", "Boxplot"])
    var = st.selectbox("Pilih variabel:", df.columns)

    fig, ax = plt.subplots(figsize=(8, 4))

    # BAR
    if chart_type == "Bar Chart":
        if df[var].dtype.name == "category":
            df[var].value_counts().plot(kind="bar", ax=ax, color="#4A90E2", edgecolor="black")
            ax.set_title(f"Bar Chart - {var}")
            ax.grid(axis="y", linestyle="--", alpha=0.6)
        else:
            st.error("❌ Hanya untuk kategori.")

    # PIE
    elif chart_type == "Pie Chart":
        if df[var].dtype.name == "category":
            df[var].value_counts().plot(kind="pie", ax=ax, autopct="%1.1f%%")
            ax.set_ylabel("")
            ax.set_title(f"Pie Chart - {var}")
        else:
            st.error("❌ Hanya untuk kategori.")

    # HISTOGRAM
    elif chart_type == "Histogram":
        if df[var].dtype != "category":
            sns.histplot(df[var], kde=True, ax=ax, color="#FF6F61")
            ax.set_title(f"Histogram - {var}")
        else:
            st.error("❌ Hanya untuk numerik.")

    # BOXPLOT
    elif chart_type == "Boxplot":
        if df[var].dtype != "category":
            sns.boxplot(x=df[var], ax=ax, color="#FFA07A")
            ax.set_title(f"Boxplot - {var}")
        else:
            st.error("❌ Hanya untuk numerik.")

    st.pyplot(fig)

    # Informasi
    st.markdown(f"""
    ### 📝 Interpretasi Grafik
    Grafik **{chart_type}** untuk variabel **{var}** menunjukkan pola distribusi
    atau komposisi kategori yang dapat membantu memahami faktor yang berhubungan
    dengan stunting. Grafik ini memudahkan identifikasi pola-pola penting seperti
    dominasi jenis kelamin tertentu, persebaran umur, atau karakteristik fisik anak.
    """)

# ============================================
# 6. ABOUT
# ============================================
elif menu == "ℹ️ About":
    st.title("ℹ️ Tentang Dashboard")
    st.info("""
    Dashboard ini dibuat untuk visualisasi data Stunting.
    Fitur-fitur:
    - Statistik deskriptif otomatis
    - Visualisasi interaktif
    - Filter kategori & numerik

    Dashboard ini juga dibuat sebagai bentuk pemenuhan Tugas Ujian Akhir Semester Mata Kuliah Komputasi Statistika.
    Semoga apa yang ada di dalam dashboard ini dapat dipertanggungjawabkan dan memudahkan serta menunjang pengetahuan yang menggunakannya.
""")
from pyngrok import ngrok

ngrok.set_auth_token("3675dsZ2B6e5QvxHq6jrAgp4CJD_s8kYo9Dj4UXgLDS9FZWj")

# Buat tunnel
public_url = ngrok.connect(8501)
public_url
