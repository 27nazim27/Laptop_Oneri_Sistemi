import streamlit as st
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import NearestNeighbors

# =========================
# VERİ
# =========================
df = pd.read_csv("laptop_price - dataset.csv")

df["Price_TL"] = df["Price (Euro)"] * 35
df["CPU_Score"] = df["CPU_Frequency (GHz)"]
df["GPU_Score"] = df["GPU_Type"].apply(lambda x: 2 if "Nvidia" in x else 1)

df["SSD"] = df["Memory"].str.extract(r'(\d+)GB SSD').fillna(0).astype(int)
df["HDD"] = df["Memory"].str.extract(r'(\d+)GB HDD').fillna(0).astype(int)

# =========================
# MODEL
# =========================
features = df[["CPU_Score","RAM (GB)","GPU_Score","SSD","HDD","Price_TL"]]

scaler = MinMaxScaler()
X = scaler.fit_transform(features)

knn = NearestNeighbors(n_neighbors=5)
knn.fit(X)

# =========================
# SAYFA AYARLARI
# =========================
st.set_page_config(page_title="Laptop Öneri Sistemi", layout="wide", page_icon="💻")

# =========================
# CSS TASARIM
# =========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* GENEL ARKA PLAN */
html, body, [data-testid="stAppViewContainer"] {
    background-color: #0d1117 !important;
    color: #e6edf3 !important;
    font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #161b22 0%, #0d1117 100%) !important;
    border-right: 1px solid #21262d !important;
}

[data-testid="stSidebar"] * {
    color: #c9d1d9 !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* SIDEBAR HEADER */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #58a6ff !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: 0.5px;
}

/* SLIDER & SELECT */
[data-testid="stSlider"] .st-bx { background: #58a6ff !important; }
.stSlider > div > div > div > div { background: #58a6ff !important; }

div[data-baseweb="select"] > div {
    background-color: #161b22 !important;
    border: 1px solid #30363d !important;
    border-radius: 8px !important;
    color: #e6edf3 !important;
}

/* CHECKBOX */
[data-testid="stCheckbox"] span {
    color: #8b949e !important;
    font-size: 0.9rem !important;
}

/* ANA BAŞLIK */
.hero-header {
    background: linear-gradient(135deg, #161b22 0%, #0d1117 60%, #0a1628 100%);
    border: 1px solid #21262d;
    border-radius: 16px;
    padding: 40px 48px;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
}

.hero-header::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 220px; height: 220px;
    background: radial-gradient(circle, rgba(88,166,255,0.12) 0%, transparent 70%);
    border-radius: 50%;
}

.hero-header::after {
    content: '';
    position: absolute;
    bottom: -40px; left: 40px;
    width: 160px; height: 160px;
    background: radial-gradient(circle, rgba(63,185,80,0.07) 0%, transparent 70%);
    border-radius: 50%;
}

.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.6rem;
    font-weight: 800;
    background: linear-gradient(90deg, #58a6ff, #79c0ff, #3fb950);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 8px 0;
    line-height: 1.1;
}

.hero-sub {
    font-size: 1.05rem;
    color: #8b949e;
    font-weight: 300;
    margin: 0;
}

/* BÖLÜM BAŞLIĞI */
.section-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #58a6ff;
    margin: 28px 0 16px 0;
}

/* LAPTOP KARTI */
.laptop-card {
    background: linear-gradient(145deg, #161b22, #0d1117);
    border: 1px solid #21262d;
    border-radius: 14px;
    padding: 28px 32px;
    margin-bottom: 16px;
    position: relative;
    transition: all 0.25s ease;
    overflow: hidden;
}

.laptop-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #58a6ff, #3fb950);
    opacity: 0;
    transition: opacity 0.25s ease;
}

.laptop-card:hover {
    border-color: #30363d;
    transform: translateY(-2px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.4);
}

.laptop-card:hover::before { opacity: 1; }

.card-header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    margin-bottom: 20px;
    flex-wrap: wrap;
    gap: 12px;
}

.card-brand {
    font-family: 'Syne', sans-serif;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #58a6ff;
    margin-bottom: 4px;
}

.card-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.2rem;
    font-weight: 700;
    color: #e6edf3;
    line-height: 1.3;
}

.card-price {
    font-family: 'Syne', sans-serif;
    font-size: 1.5rem;
    font-weight: 800;
    color: #3fb950;
    white-space: nowrap;
}

.card-price-label {
    font-size: 0.7rem;
    color: #8b949e;
    text-align: right;
    font-weight: 400;
}

.specs-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 10px;
}

.spec-item {
    display: flex;
    align-items: center;
    gap: 10px;
    background: rgba(33,38,45,0.6);
    border-radius: 8px;
    padding: 10px 14px;
}

.spec-icon {
    font-size: 1rem;
    flex-shrink: 0;
}

.spec-content {}
.spec-label {
    font-size: 0.65rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #8b949e;
    font-weight: 500;
    line-height: 1;
    margin-bottom: 2px;
}

.spec-value {
    font-size: 0.9rem;
    color: #c9d1d9;
    font-weight: 500;
    line-height: 1.2;
}

/* BOŞ DURUM */
.empty-state {
    text-align: center;
    padding: 60px 40px;
    border: 1px dashed #30363d;
    border-radius: 14px;
    color: #8b949e;
}

.empty-icon { font-size: 3rem; margin-bottom: 16px; }
.empty-text { font-size: 1.1rem; }

/* DIVIDER */
hr { border: none; border-top: 1px solid #21262d; margin: 24px 0; }

/* STREAMLIT ELEMENTLERİNİ GİZLE */
#MainMenu, footer, header { visibility: hidden; }

/* SAYAÇ BADGE */
.result-count {
    display: inline-block;
    background: rgba(88,166,255,0.1);
    border: 1px solid rgba(88,166,255,0.3);
    color: #58a6ff;
    font-family: 'Syne', sans-serif;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 1px;
    padding: 4px 12px;
    border-radius: 20px;
    margin-left: 12px;
    vertical-align: middle;
}

.section-header-row {
    display: flex;
    align-items: center;
    margin-bottom: 20px;
}

.section-main-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.3rem;
    font-weight: 700;
    color: #e6edf3;
}
</style>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR
# =========================
st.sidebar.markdown("### 🔍 Arama Kriterleri")
st.sidebar.markdown("---")

budget = st.sidebar.slider("💰 Bütçe (TL)", 5000, 100000, 30000, step=500)
usage = st.sidebar.selectbox("🎯 Kullanım Amacı", ["Oyun", "Yazılım", "Ofis"])

st.sidebar.markdown("---")
advanced = st.sidebar.checkbox("⚙️ Gelişmiş filtreleri aç")

if advanced:
    st.sidebar.markdown("**Detaylı Özellikler**")
    ram = st.sidebar.selectbox("🧠 RAM", sorted(df["RAM (GB)"].unique()))
    cpu_freq = st.sidebar.slider("⚡ CPU GHz", 1.0, 5.0, 2.5, step=0.1)
    ssd = st.sidebar.selectbox("💾 SSD (GB)", [0, 128, 256, 512, 1024])
    brand = st.sidebar.selectbox("🏷 Marka", ["Farketmez"] + list(df["Company"].unique()))
else:
    ram = 8
    cpu_freq = 2.5
    ssd = 256
    brand = "Farketmez"

# =========================
# ANA ALAN – BAŞLIK
# =========================
st.markdown("""
<div class="hero-header">
    <p class="hero-title">💻 Laptop Öneri Sistemi</p>
    <p class="hero-sub">Kriterlerine en uygun laptopu yapay zeka ile bul.</p>
</div>
""", unsafe_allow_html=True)

# =========================
# KULLANIM AMACINA GÖRE AYAR
# =========================
if usage == "Oyun":
    gpu = 2
    cpu = max(cpu_freq, 3.0)
elif usage == "Yazılım":
    gpu = 1
    cpu = max(cpu_freq, 3.2)
else:
    gpu = 1
    cpu = cpu_freq

# =========================
# KNN
# =========================
user_input = pd.DataFrame([{
    "CPU_Score": cpu,
    "RAM (GB)": ram,
    "GPU_Score": gpu,
    "SSD": ssd,
    "HDD": 0,
    "Price_TL": budget
}])

user_scaled = scaler.transform(user_input)
distances, indices = knn.kneighbors(user_scaled)
results = df.iloc[indices[0]].copy()

if brand != "Farketmez":
    results = results[results["Company"] == brand]

# =========================
# SONUÇLAR
# =========================
count_badge = f'<span class="result-count">{len(results)} SONUÇ</span>' if len(results) > 0 else ''

st.markdown(f"""
<div class="section-header-row">
    <span class="section-main-title">🎯 Önerilen Laptoplar</span>
    {count_badge}
</div>
""", unsafe_allow_html=True)

if len(results) == 0:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-icon">&#128269;</div>
        <div class="empty-text">Bu kriterlere uygun laptop bulunamadi.<br>Lutfen filtrelerinizi genisletin.</div>
    </div>
    """, unsafe_allow_html=True)
else:
    # Tüm kartları tek bir HTML bloğunda birleştir → React DOM hatası önlenir
    cards_html = '<div class="cards-wrapper">'

    for i, row in results.iterrows():
        price_eur    = int(row.get("Price (Euro)", row["Price_TL"] / 35))
        gpu_label    = str(row["GPU_Type"]) if pd.notna(row["GPU_Type"]) else "Entegre"
        price_tl_fmt = f"{int(row['Price_TL']):,}".replace(",", ".")
        price_eu_fmt = f"{price_eur:,}".replace(",", ".")
        company      = str(row["Company"])
        product      = str(row["Product"])
        cpu_type     = str(row["CPU_Type"])
        memory       = str(row["Memory"])
        ram_gb       = int(row["RAM (GB)"])

        cards_html += f"""
        <div class="laptop-card">
            <div class="card-header">
                <div>
                    <div class="card-brand">{company}</div>
                    <div class="card-title">{product}</div>
                </div>
                <div style="text-align:right;">
                    <div class="card-price">{price_tl_fmt} TL</div>
                    <div class="card-price-label">&#8776; {price_eu_fmt} &euro;</div>
                </div>
            </div>
            <div class="specs-grid">
                <div class="spec-item">
                    <span class="spec-icon">&#129504;</span>
                    <div class="spec-content">
                        <div class="spec-label">Islemci</div>
                        <div class="spec-value">{cpu_type}</div>
                    </div>
                </div>
                <div class="spec-item">
                    <span class="spec-icon">&#9889;</span>
                    <div class="spec-content">
                        <div class="spec-label">RAM</div>
                        <div class="spec-value">{ram_gb} GB</div>
                    </div>
                </div>
                <div class="spec-item">
                    <span class="spec-icon">&#127918;</span>
                    <div class="spec-content">
                        <div class="spec-label">Ekran Karti</div>
                        <div class="spec-value">{gpu_label}</div>
                    </div>
                </div>
                <div class="spec-item">
                    <span class="spec-icon">&#128190;</span>
                    <div class="spec-content">
                        <div class="spec-label">Depolama</div>
                        <div class="spec-value">{memory}</div>
                    </div>
                </div>
            </div>
        </div>"""

    cards_html += "</div>"
    st.markdown(cards_html, unsafe_allow_html=True)
