"""Web Story PMT Jawa Timur 2025. Membaca CSV yang telah dihitung; tidak melatih model."""
from pathlib import Path
from datetime import datetime
import base64
import re
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="PMT Jawa Timur | Web Story", page_icon="🌿", layout="wide", initial_sidebar_state="expanded")
ROOT = Path(__file__).resolve().parent
DATA, ASSETS = ROOT / "data", ROOT / "assets"
GREEN, GOLD, BLUE = "#315944", "#C8A05A", "#6D9297"
COLORS = {"GPBoost": GREEN, "XGBoost Global": GOLD, "XGBoost Lokal": BLUE}
NAMES = {3501:'Pacitan',3502:'Ponorogo',3503:'Trenggalek',3504:'Tulungagung',3505:'Blitar',3506:'Kediri',3507:'Malang',3508:'Lumajang',3509:'Jember',3510:'Banyuwangi',3511:'Bondowoso',3512:'Situbondo',3513:'Probolinggo',3514:'Pasuruan',3515:'Sidoarjo',3516:'Mojokerto',3517:'Jombang',3518:'Nganjuk',3519:'Madiun',3520:'Magetan',3521:'Ngawi',3522:'Bojonegoro',3523:'Tuban',3524:'Lamongan',3525:'Gresik',3526:'Bangkalan',3527:'Sampang',3528:'Pamekasan',3529:'Sumenep',3571:'Kota Kediri',3572:'Kota Blitar',3573:'Kota Malang',3574:'Kota Probolinggo',3575:'Kota Pasuruan',3576:'Kota Mojokerto',3577:'Kota Madiun',3578:'Kota Surabaya',3579:'Kota Batu'}

# ---------- Data helpers ----------

@st.cache_data
def read_csv(name):
    return pd.read_csv(DATA / name)

def get_eval():
    frames = [read_csv("Evaluasi_Global_GPBoost.csv"), read_csv("Evaluasi_Global_XGBoost.csv"), read_csv("Evaluasi_XGBoost_Lokal.csv")]
    for frame, name in zip(frames, COLORS): frame["Model_Tampil"] = name
    return pd.concat(frames, ignore_index=True)

def region_name(value):
    match = re.search(r"(?<!\d)(35\d{2})(?!\d)", str(value))
    return NAMES.get(int(match.group(1)), str(value)) if match else str(value)

def region_code(value):
    match = re.search(r"(?<!\d)(35\d{2})(?!\d)", str(value))
    return int(match.group(1)) if match else None

def _norm(name: str) -> str:
    return re.sub(r"[^a-z0-9]", "", name.lower())

def find_asset(*keywords, exts=(".png", ".jpg", ".jpeg", ".webp")):
    """Cari file di folder assets yang namanya mengandung salah satu keyword,
    tanpa peduli huruf besar/kecil, spasi, atau underscore.
    Jadi 'Logo STI.png', 'logo_sti.PNG', 'LogoSTI.jpg' dan sejenisnya tetap ketemu."""
    if not ASSETS.exists():
        return "", None
    candidates = sorted(p for p in ASSETS.iterdir() if p.is_file() and p.suffix.lower() in exts)
    for keyword in keywords:
        target = _norm(keyword)
        for path in candidates:
            if target in _norm(path.stem):
                suffix = "png" if path.suffix.lower() == ".png" else "jpeg"
                data_uri = f"data:image/{suffix};base64,{base64.b64encode(path.read_bytes()).decode()}"
                return data_uri, path
    return "", None

def sidebar_motif_svg():
    """Corak batik sederhana (bentuk gunung & pura) untuk hiasan bawah sidebar, dibuat langsung
    lewat SVG supaya tidak bergantung pada file gambar tambahan."""
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 110" preserveAspectRatio="none">
        <polygon points="0,110 0,55 35,15 55,45 80,8 100,50 130,20 150,60 175,25 200,55 225,18 250,48 275,12 300,52 320,30 320,110" fill="#ffffff" fill-opacity="0.05"/>
        <rect x="150" y="32" width="6" height="30" fill="#ffffff" fill-opacity="0.07"/>
        <polygon points="132,32 174,32 153,14" fill="#ffffff" fill-opacity="0.08"/>
        <polygon points="138,44 168,44 153,30" fill="#ffffff" fill-opacity="0.07"/>
    </svg>'''
    return f"data:image/svg+xml;base64,{base64.b64encode(svg.encode()).decode()}"

def hero_illustration_svg():
    """Ilustrasi panorama Jawa Timur (gunung, pura, laut, sawah) sebagai vektor SVG.
    Dipakai sebagai latar hero: berbeda dari foto raster, SVG tidak pernah pecah/buram
    walau direntangkan selebar apa pun, karena tidak berbasis piksel."""
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 520" preserveAspectRatio="xMidYMid slice">
        <defs>
            <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="#EAF1E6"/>
                <stop offset="55%" stop-color="#DCE8DA"/>
                <stop offset="100%" stop-color="#CFE0D4"/>
            </linearGradient>
            <radialGradient id="sun" cx="50%" cy="50%" r="50%">
                <stop offset="0%" stop-color="#F3D998" stop-opacity="0.95"/>
                <stop offset="100%" stop-color="#F3D998" stop-opacity="0"/>
            </radialGradient>
            <linearGradient id="mtnBack" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="#9DB6A2"/>
                <stop offset="100%" stop-color="#82A088"/>
            </linearGradient>
            <linearGradient id="mtnMid" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="#5E7F68"/>
                <stop offset="100%" stop-color="#4B6B54"/>
            </linearGradient>
            <linearGradient id="mtnFront" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="#3A5A44"/>
                <stop offset="100%" stop-color="#2C4633"/>
            </linearGradient>
            <linearGradient id="sea" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="#8FB2AE"/>
                <stop offset="100%" stop-color="#6D9297"/>
            </linearGradient>
            <linearGradient id="field" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="#4F7856"/>
                <stop offset="100%" stop-color="#385E42"/>
            </linearGradient>
        </defs>

        <rect width="1600" height="520" fill="url(#sky)"/>
        <circle cx="1180" cy="150" r="170" fill="url(#sun)"/>
        <circle cx="1180" cy="150" r="46" fill="#F6E2AA" opacity="0.9"/>

        <ellipse cx="230" cy="90" rx="90" ry="16" fill="#ffffff" opacity="0.35"/>
        <ellipse cx="290" cy="100" rx="60" ry="12" fill="#ffffff" opacity="0.3"/>
        <ellipse cx="980" cy="70" rx="110" ry="18" fill="#ffffff" opacity="0.3"/>

        <path d="M0,300 L120,190 L230,270 L340,150 L470,260 L600,170 L760,290 L900,180 L1060,280 L1220,140 L1360,260 L1600,190 L1600,340 L0,340 Z" fill="url(#mtnBack)" opacity="0.75"/>
        <path d="M700,340 L830,120 L900,190 L1000,90 L1120,340 Z" fill="url(#mtnMid)"/>
        <path d="M960,150 C985,128 1015,128 1040,150 L1010,120 C1000,110 990,110 980,120 Z" fill="#EDE7DD" opacity="0.85"/>
        <path d="M980,120 C995,95 1005,95 1020,120 C1030,138 1040,150 1055,168 C1010,152 985,152 945,168 C960,150 970,138 980,120 Z" fill="#B9C9BE" opacity="0.5"/>

        <path d="M0,360 L180,230 L360,330 L520,200 L680,320 L840,240 L1000,340 L1170,220 L1340,330 L1600,260 L1600,400 L0,400 Z" fill="url(#mtnFront)"/>

        <rect x="0" y="380" width="1600" height="140" fill="url(#sea)"/>
        <path d="M0,392 Q40,386 80,392 T160,392 T240,392 T320,392 T400,392" stroke="#F5F1E7" stroke-opacity="0.25" stroke-width="3" fill="none"/>
        <path d="M0,414 Q40,408 80,414 T160,414 T240,414 T320,414 T400,414" stroke="#F5F1E7" stroke-opacity="0.2" stroke-width="3" fill="none"/>
        <path d="M900,398 Q950,392 1000,398 T1100,398 T1200,398 T1300,398 T1400,398" stroke="#F5F1E7" stroke-opacity="0.22" stroke-width="3" fill="none"/>

        <g transform="translate(1240,255)">
            <rect x="-6" y="60" width="12" height="90" fill="#3B2A22"/>
            <polygon points="-46,60 46,60 0,-10" fill="#2C4633"/>
            <polygon points="-34,40 34,40 0,-30" fill="#3A5A44"/>
            <polygon points="-22,20 22,20 0,-46" fill="#4B6B54"/>
            <rect x="-14" y="60" width="28" height="26" fill="#2C4633"/>
        </g>
        <g transform="translate(1330,270) scale(0.8)">
            <rect x="-6" y="60" width="12" height="80" fill="#3B2A22"/>
            <polygon points="-40,60 40,60 0,-6" fill="#385E42"/>
            <polygon points="-28,36 28,36 0,-28" fill="#4B6B54"/>
            <rect x="-12" y="60" width="24" height="22" fill="#2C4633"/>
        </g>

        <path d="M0,430 C120,405 260,450 400,420 C540,392 680,440 820,412 C960,388 1100,432 1260,410 C1380,394 1500,418 1600,404 L1600,520 L0,520 Z" fill="url(#field)"/>
        <path d="M0,460 C140,438 300,472 460,448 C620,424 760,462 920,440 C1080,420 1240,456 1400,436 C1470,428 1540,432 1600,430 L1600,520 L0,520 Z" fill="#2C4633" opacity="0.9"/>

        <g fill="#2C4633" opacity="0.85">
            <path d="M60,455 q6,-16 12,0 q6,-16 12,0 z"/>
            <path d="M110,462 q6,-16 12,0 q6,-16 12,0 z"/>
            <path d="M170,452 q6,-16 12,0 q6,-16 12,0 z"/>
        </g>
    </svg>'''
    return f"data:image/svg+xml;base64,{base64.b64encode(svg.encode()).decode()}"

# ---------- Styling ----------

_sidebar_pattern_data, _ = find_asset("corak", "pattern", "batik", "motif")
_motif_svg = sidebar_motif_svg()

if _sidebar_pattern_data:
    _sidebar_bg_image = f"linear-gradient(165deg, rgba(37,68,50,.93), rgba(25,56,45,.93)), url('{_sidebar_pattern_data}')"
    _sidebar_bg_repeat = "no-repeat, repeat"
    _sidebar_bg_size = "cover, 220px 220px"
    _sidebar_bg_position = "center, center"
else:
    _sidebar_bg_image = (
        "radial-gradient(circle, rgba(255,255,255,.06) 0 3px, transparent 4px), "
        "radial-gradient(circle, rgba(255,255,255,.05) 0 3px, transparent 4px), "
        f"url('{_motif_svg}'), "
        "linear-gradient(165deg,#254432,#19382D)"
    )
    _sidebar_bg_repeat = "repeat, repeat, no-repeat, no-repeat"
    _sidebar_bg_size = "90px 90px, 130px 130px, 100% 130px, cover"
    _sidebar_bg_position = "0 0, 45px 45px, bottom center, center"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Fraunces:wght@500;600;700&display=swap');

*, *::before, *::after {{ -webkit-font-smoothing:antialiased; -moz-osx-font-smoothing:grayscale; text-rendering:optimizeLegibility; }}

html,body,[class*="css"],.stApp {{font-family:'DM Sans',sans-serif;font-size:18px;color:#253d30}}
.stApp {{background:#F5F1E7}}
.block-container {{max-width:1560px;padding:1.4rem clamp(1rem, 3vw, 2.6rem) 3rem}}
h1,h2,h3 {{font-family:'Fraunces',Georgia,serif;color:#234331}}
h1 {{font-size:clamp(1.7rem, 1.2rem + 2vw, 2.4rem)!important}}
h2 {{font-size:clamp(1.4rem, 1rem + 1.4vw, 1.85rem)!important}}
h3 {{font-size:clamp(1.15rem, .95rem + .8vw, 1.35rem)!important}}
p,li,label {{font-size:1.08rem!important;line-height:1.75}}

/* ---- Sidebar ---- */
[data-testid="stSidebar"] {{
    background-color:#254432;
    background-image:{_sidebar_bg_image};
    background-repeat:{_sidebar_bg_repeat};
    background-size:{_sidebar_bg_size};
    background-position:{_sidebar_bg_position};
    border-right:1px solid #365B46;
}}
[data-testid="stSidebar"] * {{color:#FAF6E9!important}}
[data-testid="stSidebar"] h2 {{font-size:1.4rem!important;margin-bottom:2px}}
[data-testid="stSidebar"] .stCaption, [data-testid="stSidebar"] small {{font-size:.95rem!important;letter-spacing:.05em}}
[data-testid="stSidebar"] [data-testid="stImage"] img {{border-radius:14px;background:#F4F1DF;padding:6px;object-fit:contain}}
.logo-badge{{width:76px;height:76px;border-radius:16px;background:#F4F1DF;color:#254432;display:flex;align-items:center;justify-content:center;font-family:'Fraunces',Georgia,serif;font-weight:700;font-size:1.5rem}}

/* ---- Blok merek (logo + kampus) di atas sidebar, rata tengah ---- */
.sidebar-brand{{display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;width:100%;gap:2px;padding:8px 4px 4px;margin:0 auto}}
.sidebar-brand img{{display:block;margin:0 auto;width:92px;height:92px;object-fit:contain;border-radius:16px;background:#F4F1DF;padding:8px}}
.sidebar-kampus{{display:block;width:100%;text-align:center;font-family:'Fraunces',Georgia,serif;font-weight:700;font-size:1.05rem!important;letter-spacing:.02em;color:#F7F3E7!important;margin-top:8px;line-height:1.3}}
.sidebar-title{{display:block;width:100%;text-align:center;font-family:'Fraunces',Georgia,serif;font-weight:600;font-size:1.3rem!important;color:#FAF6E9!important;margin-top:10px}}
.sidebar-subtitle{{display:block;width:100%;text-align:center;font-size:.9rem!important;letter-spacing:.08em;color:#CFE0D2!important;margin-top:2px}}
</style>
""", unsafe_allow_html=True)

# Sisa styling (tidak bergantung pada asset) ditaruh di blok terpisah supaya lebih mudah dirawat.
st.markdown("""
<style>
[data-testid="stSidebar"] .stButton>button {width:100%;text-align:left;justify-content:flex-start;font-size:1.1rem!important;font-weight:600;letter-spacing:.01em;border-radius:14px;padding:.9rem 1.15rem;border:0;min-height:54px;background:transparent;color:#F7F3E7!important;transition:background .15s ease}
[data-testid="stSidebar"] .stButton>button:hover {background:#3E6350!important}
[data-testid="stSidebar"] .stButton>button[kind="primary"] {background:#F4F1DF!important;color:#274432!important;font-weight:700;box-shadow:0 4px 10px #00000022}
[data-testid="stSidebar"] .stButton>button[kind="primary"] p {color:#274432!important;font-size:1.1rem!important}

/* ---- Metric cards ---- */
.metric-card{display:flex;align-items:center;gap:16px;background:#FFFDF6;border:1px solid #E5DECC;border-radius:18px;padding:20px 22px;box-shadow:0 5px 15px #2948340C;height:100%}
.metric-icon{flex:none;width:50px;height:50px;border-radius:50%;background:#E9F0E6;color:#254432;display:flex;align-items:center;justify-content:center;font-size:1.4rem;font-weight:700}
.metric-label{font-size:1.05rem;color:#4d6350;font-weight:700}
.metric-value{font-size:2rem;color:#254432;font-weight:700;font-family:'Fraunces',Georgia,serif;line-height:1.3}
.metric-note{font-size:.95rem;color:#71826f}

/* ---- Content cards ---- */
[data-testid="stPlotlyChart"], [data-testid="stDataFrame"], [data-testid="stTable"] {background:#FFFDF6;border:1px solid #E5DECC;border-radius:17px;padding:14px}

/* ---- Tabel: dibuat lebih menonjol (header gelap, teks tebal, baris zebra), sudut tajam, tanpa kolom nomor ---- */
[data-testid="stTable"] {padding:0;overflow:hidden;border-radius:0!important}
[data-testid="stTable"] table {width:100%;border-collapse:separate;border-spacing:0;font-size:1.1rem!important}
[data-testid="stTable"] table thead tr th:first-child,
[data-testid="stTable"] table tbody tr th:first-child {display:none!important}
[data-testid="stTable"] thead tr th {background:#254432!important;color:#FAF6E9!important;font-weight:700!important;text-transform:uppercase;letter-spacing:.03em;font-size:.95rem!important;padding:14px 16px!important;border:0!important}
[data-testid="stTable"] tbody tr td {padding:12px 16px!important;font-weight:600!important;color:#20362A!important;border-bottom:1px solid #EDE7D6!important}
[data-testid="stTable"] tbody tr:nth-child(even) {background:#F6F2E4!important}
[data-testid="stTable"] tbody tr:hover td {background:#EAE3CB!important}
[data-testid="stDataFrame"] {font-size:1.1rem;font-weight:500}

/* ---- Menyamakan tinggi kartu/kolom sejajar secara otomatis (mengikuti konten TERPANJANG, tidak ada teks kepotong) ---- */
[data-testid="stHorizontalBlock"] {align-items:stretch!important}
[data-testid="column"] {display:flex!important}
[data-testid="column"] > div {width:100%}
[data-testid="column"] [data-testid="stVerticalBlock"] {height:100%;display:flex;flex-direction:column}
[data-testid="column"] [data-testid="element-container"],
[data-testid="column"] [data-testid="stMarkdown"],
[data-testid="column"] [data-testid="stMarkdownContainer"] {display:contents}
.card {display:flex;flex-direction:column;flex:1 1 auto;height:auto}
.card p {flex:1}
.hero {border-radius:24px;padding:clamp(26px,4vw,46px) clamp(24px,4.5vw,48px);min-height:260px;background-color:#E7EBDB;background-position:center;background-size:cover;background-repeat:no-repeat;border:1px solid #DBE2D2;display:flex;flex-direction:column;justify-content:center;margin-bottom:20px;image-rendering:auto}
.hero h1 {max-width:920px;font-size:clamp(1.55rem,1.05rem+2.2vw,2.55rem)!important;line-height:1.26;margin:.5rem 0 .8rem}
.hero p {max-width:840px;color:#405D49;font-size:clamp(1rem,.85rem+.7vw,1.2rem)!important;margin:0}
.eyebrow {font-size:.95rem;letter-spacing:.16em;font-weight:700;color:#52775A}

.card {background:#FFFDF6;border:1px solid #E5DECC;border-radius:18px;padding:26px;box-shadow:0 5px 16px #2948340B}
.card h3 {margin:6px 0 10px;font-size:1.25rem!important}
.card p {color:#3f4f42;margin:0;font-size:1.08rem!important;line-height:1.65}
.card-badge{width:36px;height:36px;border-radius:50%;background:#254432;color:#F7F3E7;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:1.05rem;margin-bottom:12px}
.card-icon{font-size:1.6rem;color:#52775A;margin-bottom:8px}

/* ---- Step flow (Alur Penelitian) ---- */
.step-row{display:flex;align-items:flex-start;justify-content:space-between;gap:6px;margin-top:14px;flex-wrap:wrap}
.step{display:flex;flex-direction:column;align-items:center;text-align:center;flex:1;min-width:90px}
.step-circle{width:54px;height:54px;border-radius:50%;background:#EFE9D6;color:#254432;display:flex;align-items:center;justify-content:center;font-family:'Fraunces',Georgia,serif;font-weight:700;font-size:1.4rem;margin-bottom:9px;border:2px solid #C8A05A}
.step-title{font-weight:700;color:#254432;font-size:1.05rem}
.step-caption{color:#5b6c58;font-size:.92rem}
.step-arrow{color:#BFC9AC;font-size:1.6rem;margin-top:14px}

.section-title{font:700 1.8rem 'Fraunces',Georgia,serif;color:#234331;margin:30px 0 18px;padding-left:16px;border-left:5px solid #C8A05A}
.story-note {background:#E5EBDD;border-left:5px solid #6B936F;border-radius:0 14px 14px 0;padding:18px 22px;margin:16px 0;color:#2c4330;font-size:1.08rem;line-height:1.75}
.small-muted {color:#4d5f4b;font-size:1rem}

/* ---- Choice controls: segmented / pill style ---- */
div[data-testid="stRadio"] > label, div[data-testid="stSelectbox"] label {font-weight:700;color:#254432;font-size:1.1rem!important;margin-bottom:6px}
div[data-testid="stRadio"] div[role="radiogroup"]{gap:10px;flex-wrap:wrap;margin-top:4px}
div[data-testid="stRadio"] div[role="radiogroup"] label{background:#FFFDF6;border:1.5px solid #E1DAC6;border-radius:999px;padding:12px 26px;margin:0!important;transition:.15s ease;cursor:pointer}
div[data-testid="stRadio"] div[role="radiogroup"] label:hover{border-color:#8FA98F;background:#F2EEDD}
div[data-testid="stRadio"] div[role="radiogroup"] label>div:first-child{display:none!important}
div[data-testid="stRadio"] div[role="radiogroup"] label p{font-size:1.08rem!important;font-weight:600;color:#2c4934!important}
div[data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked){background:#254432;border-color:#254432}
div[data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) p{color:#F7F3E7!important}

div[data-testid="stSelectbox"] div[data-baseweb="select"]{border-radius:14px!important;border:1.5px solid #E1DAC6!important;background:#FFFDF6!important;min-height:48px!important}
div[data-testid="stSelectbox"] div[data-baseweb="select"] *{font-size:1.08rem!important}
div[data-testid="stSelectbox"] div[data-baseweb="select"]:hover{border-color:#8FA98F!important}

/* ---- Footer ---- */
.footer-plain{margin-top:36px;padding-top:22px;border-top:1px solid #DCD4B9}
.footer-row{display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:16px 24px}
.footer-col{flex:1 1 220px;min-width:200px}
.footer-col.center{text-align:center}
.footer-col.right{text-align:right}
.footer-title{font-family:'Fraunces',Georgia,serif;font-size:1.05rem;font-weight:700;color:#254432}
.footer-sub{color:#5b6c58;font-size:.92rem;margin-top:3px;line-height:1.5}
.footer-copyright{display:block;width:100%;text-align:center;margin-top:20px;padding:14px 10px;background:#EFE9D6;border-radius:0;color:#254432!important;font-weight:700;font-size:.95rem;text-decoration:none!important;border-top:1px solid #DCD4B9}
.footer-copyright:hover{background:#E5DEC4}

/* ---- Responsif saat layar/jendela diperkecil ---- */
html, body {overflow-x:hidden}
.block-container {overflow-x:hidden}
[data-testid="stHorizontalBlock"] {flex-wrap:wrap!important;row-gap:16px}
[data-testid="column"] {min-width:min(100%,230px)!important}

@media (max-width: 1200px) {
  .block-container {padding-left:1.1rem;padding-right:1.1rem}
  .hero h1 {max-width:100%}
}
@media (max-width: 900px) {
  .hero {min-height:auto}
  .metric-card {flex-direction:column;text-align:center;gap:8px}
  .step-row {flex-direction:column;gap:14px}
  .step-arrow {display:none}
  .card {padding:20px}
  [data-testid="column"] {min-width:min(100%,260px)!important}
  [data-testid="stSidebar"] .stButton>button {font-size:1.02rem!important;min-height:48px}
  [data-testid="stTable"] table, [data-testid="stDataFrame"] {font-size:.98rem!important}
  div[data-testid="stRadio"] div[role="radiogroup"] label {padding:10px 18px}
}
@media (max-width: 600px) {
  .section-title{font-size:1.4rem!important;margin:22px 0 14px}
  .hero{padding:22px 20px}
  .footer-plain{padding-top:16px}
  .footer-row{flex-direction:column;gap:12px}
  .footer-col, .footer-col.center, .footer-col.right{text-align:left}
  [data-testid="column"] {min-width:100%!important}
  .block-container {padding-left:.9rem;padding-right:.9rem}
}

/* Tabel dan grafik: jangan sampai memaksa lebar minimum melebihi layar */
[data-testid="stTable"], [data-testid="stDataFrame"], [data-testid="stPlotlyChart"] {max-width:100%;overflow-x:auto}
</style>
""", unsafe_allow_html=True)

# ---------- Sidebar navigation ----------

if "page" not in st.session_state: st.session_state.page = "Beranda"

logo_data, logo_path = find_asset("logosti", "logo sti", "sti")
if not logo_data:
    logo_data, logo_path = find_asset("logo")

with st.sidebar:
    if logo_data:
        logo_html = f'<img src="{logo_data}" alt="logo" />'
    else:
        logo_html = '<div class="logo-badge">STI</div>'
    st.markdown(
        f'''<div class="sidebar-brand">
            {logo_html}
            <div class="sidebar-kampus">Politeknik Statistika STIS</div>
            <div class="sidebar-title">PMT Jawa Timur</div>
            <div class="sidebar-subtitle">WEB STORY PENELITIAN · 2025</div>
        </div>''',
        unsafe_allow_html=True,
    )
    st.divider()
    for label, icon in [("Beranda","⌂"),("Perbandingan Model","▥"),("Evaluasi Penargetan","◎"),("Interpretasi Model","✎"),("Kabupaten/Kota","◆"),("Ringkasan Hasil","▤")]:
        if st.button(f"{icon}   {label}", key=f"nav_{label}", type="primary" if st.session_state.page==label else "secondary", use_container_width=True):
            st.session_state.page=label
            st.rerun()
    st.divider()
    st.markdown("**SUMBER DATA**")
    st.caption("Susenas–Podes 2025")
    st.markdown("**CAKUPAN**")
    st.caption("38 kabupaten/kota di Jawa Timur")

page = st.session_state.page

# ---------- Reusable components ----------

def card(title, body, badge=None, icon=None, fixed_height=None):
    badge_html = f'<div class="card-badge">{badge}</div>' if badge else ""
    icon_html = f'<div class="card-icon">{icon}</div>' if icon else ""
    style = f' style="min-height:{fixed_height}px;box-sizing:border-box"' if fixed_height else ""
    st.markdown(f'<div class="card"{style}>{badge_html}{icon_html}<h3>{title}</h3><p>{body}</p></div>', unsafe_allow_html=True)

def metric_card(icon, label, value, note):
    st.markdown(
        f'''<div class="metric-card">
            <div class="metric-icon">{icon}</div>
            <div>
                <div class="metric-label">{label}</div>
                <div class="metric-value">{value}</div>
                <div class="metric-note">{note}</div>
            </div>
        </div>''',
        unsafe_allow_html=True,
    )

def heading(title, subtitle):
    st.title(title); st.write(subtitle); st.divider()

AXIS_STYLE = dict(
    tickfont=dict(size=15, color="#20362A", family="DM Sans"),
    title_font=dict(size=16, color="#1A2F22", family="DM Sans"),
    linecolor="#2c4934", linewidth=1.6, showline=True,
    gridcolor="#E4DEC9", zeroline=False,
)

def style_axes(fig):
    """Membuat teks & garis sumbu x/y lebih tebal, besar, dan kontras; judul grafik ditengahkan di atas."""
    fig.update_xaxes(**AXIS_STYLE)
    fig.update_yaxes(**AXIS_STYLE)
    fig.update_layout(title=dict(font=dict(size=19, color="#1A2F22"), x=0.5, xanchor="center", y=0.97, yanchor="top"))
    return fig

def show_table(df):
    """Tabel dengan header gelap, teks tebal, baris zebra, tanpa nomor indeks, dan sudut tajam."""
    display_df = df.copy()
    display_df.index = [""] * len(display_df)
    st.table(display_df)

def plot_bar(df, metric, title):
    fig = px.bar(df, x="Model_Tampil", y=metric, color="Model_Tampil", color_discrete_map=COLORS, text_auto=".3f", labels={"Model_Tampil":"Model", metric:metric})
    fig.update_layout(title=title, template="plotly_white", paper_bgcolor="#FFFDF6", plot_bgcolor="#FFFDF6", showlegend=False, height=440, font=dict(size=16, color="#294534"), margin=dict(l=30, r=30, t=65, b=40))
    fig.update_traces(textposition="outside", cliponaxis=False, textfont=dict(size=15, color="#1A2F22"))
    style_axes(fig)
    st.plotly_chart(fig, use_container_width=True)

def render_footer():
    tahun = datetime.now().year
    st.markdown(
        f'''<div class="footer-plain">
            <div class="footer-row">
                <div class="footer-col">
                    <div class="footer-title">PMT Jawa Timur</div>
                    <div class="footer-sub">Web Story Penelitian · Proxy Mean Test dengan Gaussian Process Boosting</div>
                </div>
                <div class="footer-col right">
                    <div class="footer-title">Politeknik Statistika STIS</div>
                    <div class="footer-sub">Susenas–Podes 2025 · 38 Kabupaten/Kota di Jawa Timur</div>
                </div>
            </div>
            <a class="footer-copyright" href="mailto:anggimaryaputriarivia@gmail.com" target="_blank" rel="noopener noreferrer">
                ✉ &nbsp; © {tahun} Anggi Marya Putri Arivia — klik untuk menghubungi lewat email
            </a>
        </div>''',
        unsafe_allow_html=True,
    )

# ---------- Pages ----------

if page == "Beranda":
    hero_data = hero_illustration_svg()
    bg = f"linear-gradient(90deg,rgba(246,246,229,.97) 0%,rgba(246,246,229,.9) 42%,rgba(246,246,229,.22) 100%),url('{hero_data}')"
    st.markdown(
        f'''<div class="hero" style="background-image:{bg}">
            <div class="eyebrow">WEB STORY PENELITIAN · JAWA TIMUR 2025</div>
            <h1>Pengembangan Model Proxy Mean Test dengan Algoritma Gaussian Process Boosting untuk Pemeringkatan Kesejahteraan Keluarga di Provinsi Jawa Timur</h1>
            <p>Menelusuri prediksi pengeluaran, pemeringkatan kesejahteraan, ketepatan penargetan, dan variasi antarkabupaten/kota.</p>
        </div>''',
        unsafe_allow_html=True,
    )

    a, b, c, d = st.columns(4)
    with a: metric_card("⌂", "Rumah Tangga", "31.481", "responden")
    with b: metric_card("◈", "Kabupaten/Kota", "38", "wilayah")
    with c: metric_card("▤", "Variabel Prediktor", "58", "variabel")
    with d: metric_card("▥", "Data Uji", "6.297", "rumah tangga")

    st.markdown('<div class="section-title">Mengenal Penelitian</div>', unsafe_allow_html=True)
    a, b = st.columns([1.1, 1], gap="medium")
    with a:
        card(
            "Mengapa Penelitian Ini Penting?",
            "Proxy Means Test (PMT) memperkirakan kesejahteraan keluarga dari karakteristik rumah tangga yang dapat diamati. Penelitian ini mengembangkan GPBoost dan membandingkannya dengan XGBoost Global serta 38 model XGBoost Lokal.",
            icon="✎",
        )
    with b:
        st.markdown(
            '''<div class="card">
                <h3>Alur Penelitian</h3>
                <div class="step-row">
                    <div class="step"><div class="step-circle">1</div><div class="step-title">Data</div><div class="step-caption">Susenas–Podes 2025</div></div>
                    <div class="step-arrow">›</div>
                    <div class="step"><div class="step-circle">2</div><div class="step-title">Pemodelan</div><div class="step-caption">GPBoost & XGBoost</div></div>
                    <div class="step-arrow">›</div>
                    <div class="step"><div class="step-circle">3</div><div class="step-title">Evaluasi</div><div class="step-caption">Regresi & penargetan</div></div>
                    <div class="step-arrow">›</div>
                    <div class="step"><div class="step-circle">4</div><div class="step-title">Interpretasi</div><div class="step-caption">Gain, SHAP, ICC</div></div>
                </div>
            </div>''',
            unsafe_allow_html=True,
        )

    st.markdown('<div class="section-title">Eksplorasi Hasil Penelitian</div>', unsafe_allow_html=True)
    items = [
        ("01", "▥", "Perbandingan Model", "Bandingkan ketepatan prediksi dan pemeringkatan antar model."),
        ("02", "◎", "Evaluasi Penargetan", "Pelajari hasil identifikasi kelompok 20% dan 40% keluarga."),
        ("03", "✎", "Interpretasi Model", "Telusuri variabel penting melalui Gain, SHAP, dan efek acak wilayah."),
        ("04", "◆", "Kabupaten/Kota", "Jelajahi evaluasi 38 model XGBoost Lokal di tiap wilayah."),
        ("05", "▤", "Ringkasan Hasil", "Lihat seluruh metrik utama dalam satu tampilan komprehensif."),
    ]
    cols = st.columns(5, gap="small")
    for col, (badge, icon, title, body) in zip(cols, items):
        with col:
            card(title, body, badge=badge, icon=icon, fixed_height=400)
            if st.button("Lihat detail →", key="go_"+title, use_container_width=True):
                st.session_state.page = title; st.rerun()

    st.markdown('<div class="story-note">“Dari data, lahir pemahaman. Dari pemahaman, tumbuh penargetan yang lebih tepat.”</div>', unsafe_allow_html=True)

elif page == "Perbandingan Model":
    heading("Perbandingan Kinerja Model", "Evaluasi GPBoost, XGBoost Global, dan XGBoost Lokal berdasarkan hasil yang sudah dihitung.")
    ev = get_eval()
    metric = st.selectbox("Pilih metrik", ["RMSE", "MAE", "R_Square", "Spearman", "Kendall"])
    plot_bar(ev, metric, f"Perbandingan {metric}")
    show_table(ev[["Model_Tampil", "RMSE", "MAE", "R_Square", "Spearman", "Kendall"]].round(4))

    st.markdown('<div class="section-title">Aktual dan Prediksi</div>', unsafe_allow_html=True)
    pilihan = st.radio("Pilih model untuk grafik aktual dan prediksi", ["GPBoost", "XGBoost Global"], horizontal=True, key="pilihan_aktual_prediksi")
    nama_file = "Prediksi_Test_GPBoost.csv" if pilihan == "GPBoost" else "Prediksi_Test_XGBoost.csv"
    pred = read_csv(nama_file)

    fig = px.scatter(
        pred, x="log_KAPITA_Aktual", y="log_KAPITA_Prediksi", opacity=0.35,
        color_discrete_sequence=[GREEN],
        labels={"log_KAPITA_Aktual": "Log pengeluaran aktual", "log_KAPITA_Prediksi": "Log pengeluaran prediksi"},
    )
    fig.update_layout(template="plotly_white", paper_bgcolor="#FFFDF6", plot_bgcolor="#FFFDF6", height=480, font=dict(size=15, color="#294534"), margin=dict(l=20, r=20, t=30, b=40))
    style_axes(fig)
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Prediksi dan nilai aktual ditampilkan pada skala logaritma.")

elif page == "Evaluasi Penargetan":
    heading("Evaluasi Penargetan", "Mengevaluasi identifikasi 20% dan 40% keluarga dengan pengeluaran terendah.")
    ev = get_eval()
    coverage = st.radio("Cakupan sasaran", ["20%", "40%"], horizontal=True)
    choices = {"Inclusion Error": "IE", "Exclusion Error": "EE", "Akurasi": "Acc", "AUC-ROC": "AUC_ROC"}
    label = st.selectbox("Metrik penargetan", list(choices)); col = f"{choices[label]}_{coverage}"
    plot_bar(ev, col, f"{label} · Cakupan {coverage}")
    cols = ["Model_Tampil"] + [f"{p}_{coverage}" for p in choices.values()]
    show_table(ev[cols].round(4))
    st.markdown('<div class="story-note"><b>Interpretasi:</b> Inclusion Error menggambarkan nonsasaran yang terpilih, sedangkan Exclusion Error menggambarkan sasaran yang terlewat. Nilai pada grafik mengikuti satuan dalam CSV hasil evaluasi.</div>', unsafe_allow_html=True)

elif page == "Interpretasi Model":
    heading("Interpretasi Model", "Mengidentifikasi variabel penting menurut Gain dan mean absolute SHAP.")
    model = st.radio("Pilih model", ["GPBoost", "XGBoost"], horizontal=True)
    fi = read_csv(f"FeatureImportance_{model}.csv").nlargest(12, "Persentase_Gain").sort_values("Persentase_Gain")
    shap = read_csv(f"SHAP_{model}.csv").nlargest(12, "Mean_Abs_SHAP").sort_values("Mean_Abs_SHAP")
    a, b = st.columns(2)
    with a:
        fig = px.bar(fi, x="Persentase_Gain", y="Variabel", orientation="h", title="12 variabel utama · Gain", color_discrete_sequence=[GREEN])
        fig.update_layout(template="plotly_white", paper_bgcolor="#FFFDF6", plot_bgcolor="#FFFDF6", height=580, font=dict(size=16), title_font=dict(size=18), yaxis_title="", xaxis_title="Gain (%)")
        style_axes(fig)
        st.plotly_chart(fig, use_container_width=True)
    with b:
        fig = px.bar(shap, x="Mean_Abs_SHAP", y="Variabel", orientation="h", title="12 variabel utama · SHAP", color_discrete_sequence=[GOLD])
        fig.update_layout(template="plotly_white", paper_bgcolor="#FFFDF6", plot_bgcolor="#FFFDF6", height=580, font=dict(size=16), title_font=dict(size=18), yaxis_title="", xaxis_title="Mean absolute SHAP")
        style_axes(fig)
        st.plotly_chart(fig, use_container_width=True)
    st.caption("Gain dan mean absolute SHAP mengukur kepentingan prediktor, bukan hubungan sebab-akibat. CSV ini tidak berisi nilai SHAP individual untuk beeswarm.")
    if model == "GPBoost":
        st.markdown('<div class="section-title">Variasi antarkabupaten/kota</div>', unsafe_allow_html=True)
        re_df = read_csv("RandomEffects_GPBoost.csv")
        residual = float(re_df.loc[re_df["Komponen"] == "Error_var", "Parameter"].iloc[0])
        district = float(re_df.loc[re_df["Komponen"] == "kode_kab", "Parameter"].iloc[0])
        icc = 100 * district / (district + residual)
        a, b, c = st.columns(3)
        with a: metric_card("▤", "Varians residual", f"{residual:.4f}", "")
        with b: metric_card("◆", "Varians kab/kota", f"{district:.4f}", "")
        with c: metric_card("◎", "ICC", f"{icc:.2f}%", "")
        st.markdown(f'<div class="story-note">ICC sebesar <b>{icc:.2f}%</b> adalah proporsi variasi residual pada skala logaritma yang berkaitan dengan perbedaan antarkabupaten/kota setelah prediktor model diperhitungkan.</div>', unsafe_allow_html=True)

elif page == "Kabupaten/Kota":
    heading("Analisis 38 Kabupaten/Kota", "Evaluasi model XGBoost Lokal dengan nama wilayah")
    region = read_csv("Evaluasi_38KabKota_XGBoost.csv").copy()
    region["Nama Wilayah"] = region["Cakupan"].map(region_name)
    if region["Nama Wilayah"].nunique() != 38:
        st.warning("Sebagian nama wilayah belum dapat dipetakan. Periksa isi kolom Cakupan pada CSV.")
    metric = st.selectbox("Pilih metrik wilayah", ["RMSE", "MAE", "R_Square", "Spearman", "Kendall", "IE_20%", "EE_20%", "Acc_20%", "IE_40%", "EE_40%", "Acc_40%"])
    ordered = region.sort_values(metric)
    fig = px.bar(ordered, x=metric, y="Nama Wilayah", orientation="h", color_discrete_sequence=[GREEN], hover_data=["Cakupan"], title=f"{metric} menurut kabupaten/kota")
    fig.update_layout(template="plotly_white", paper_bgcolor="#FFFDF6", plot_bgcolor="#FFFDF6", height=1120, font=dict(size=15), margin=dict(l=25, r=30, t=65, b=35), yaxis_title="")
    style_axes(fig)
    st.plotly_chart(fig, use_container_width=True)
    selected = st.selectbox("Lihat rincian satu wilayah", sorted(region["Nama Wilayah"].unique()))
    show_table(region.loc[region["Nama Wilayah"] == selected, ["Nama Wilayah", "RMSE", "MAE", "R_Square", "Spearman", "Kendall", "IE_20%", "EE_20%", "Acc_20%", "IE_40%", "EE_40%", "Acc_40%"]].round(4))
    with st.expander("Lihat tabel seluruh wilayah"):
        show_table(region[["Nama Wilayah", "RMSE", "MAE", "R_Square", "Spearman", "Kendall", "IE_20%", "EE_20%", "Acc_20%", "IE_40%", "EE_40%", "Acc_40%"]].round(4))

else:
    heading("Ringkasan Hasil Penelitian", "Seluruh metrik utama dalam satu tampilan, tanpa menghitung ulang model.")
    ev = get_eval()
    fields = ["Model_Tampil", "RMSE", "MAE", "R_Square", "Spearman", "Kendall", "IE_20%", "EE_20%", "Acc_20%", "AUC_ROC_20%", "IE_40%", "EE_40%", "Acc_40%", "AUC_ROC_40%"]
    show_table(ev[fields].round(4))
    st.markdown('<div class="story-note">Perbandingan angka di atas bersifat deskriptif. Evaluasi wilayah lokal dan model global perlu dibaca sesuai rancangan data uji masing-masing.</div>', unsafe_allow_html=True)

render_footer()