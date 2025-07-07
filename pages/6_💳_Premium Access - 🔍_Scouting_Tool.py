import streamlit as st
import pandas as pd
from pathlib import Path
from PIL import Image
import json
import os

# ⚙️ Configurazione pagina
st.set_page_config(page_title="Drafted Players - Player List", layout='wide')

# 🧠 Inizializza stato login se mancante
if "is_logged_in" not in st.session_state:
    st.session_state.is_logged_in = False

# 🌈 Colori dinamici in base al login
bg_color = "#2f6974" if not st.session_state["is_logged_in"] else "#f7f7f7"
text_color = "white" if not st.session_state["is_logged_in"] else "#000000"

# 🌐 Styling dinamico
st.markdown(f"""
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@600&display=swap" rel="stylesheet">
    <style>
        html, body, .stApp {{
            background-color: {bg_color} !important;
            color: {text_color} !important;
        }}
        h1, h2, h3, h4, h5, h6 {{
            font-family: 'Orbitron', sans-serif !important;
            color: #f45208 !important;
        }}
        .subtitle-effect {{
            font-family: 'Orbitron', sans-serif;
            font-size: 1.2rem;
            color: {text_color};
            text-align: center;
            margin-bottom: 1rem;
        }}
        .title-custom {{
            font-family: 'Orbitron', sans-serif;
            font-size: 2.5rem;
            font-weight: 700;
            color: #f45208;
            text-align: center;
            margin-bottom: 0.5rem;
        }}
        label, .stSelectbox label {{
            color: {text_color} !important;
            font-weight: bold;
        }}
        button[data-testid="baseButton-secondary"] {{
            background-color: #f45208 !important;
            color: white !important;
            font-weight: bold !important;
            font-family: 'Orbitron', sans-serif !important;
            border-radius: 6px !important;
            padding: 0.5rem 1.5rem !important;
            border: none !important;
            transition: background-color 0.3s ease;
        }}
        button[data-testid="baseButton-secondary"]:hover {{
            background-color: #ff6d2e !important;
        }}
    </style>
""", unsafe_allow_html=True)

# 🔐 BLOCCO LOGIN
if not st.session_state.is_logged_in:
    st.markdown("## Login Required")

    with st.form("login_form"):
        login_email = st.text_input("Email")
        login_password = st.text_input("Password", type="password")

        col1, col2 = st.columns([1, 2])
        with col1:
            login_btn = st.form_submit_button("🔓 Enter")
        with col2:
            st.markdown("<div style='font-size:14px; color: gray; padding-top: 6px", unsafe_allow_html=True)

        if login_btn:
            if os.path.exists("utenti.json"):
                try:
                    with open("utenti.json") as f:
                        user_data = json.load(f)

                    if login_email == user_data["email"] and login_password == user_data["password"]:
                        st.session_state.is_logged_in = True
                        st.experimental_rerun()
                    else:
                        st.markdown("""
                            <div style='
                                background-color: #f0f0f0;
                                color: black;
                                padding: 12px;
                                border-radius: 6px;
                                font-weight: bold;
                                font-size: 15px;
                                margin-top: 10px;
                            '>
                                ❌ Invalid credentials.
                            </div>
                        """, unsafe_allow_html=True)
                except Exception:
                    st.markdown("""
                        <div style='
                            background-color: #f0f0f0;
                            color: black;
                            padding: 12px;
                            border-radius: 6px;
                            font-weight: bold;
                            font-size: 15px;
                            margin-top: 10px;
                        '>
                            Please Click<strong> Enter again<strong>. 
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div style='
                        background-color: #f0f0f0;
                        color: black;
                        padding: 12px;
                        border-radius: 6px;
                        font-weight: bold;
                        font-size: 15px;
                        margin-top: 10px;
                    '>
                        ⚠️ No registered user found. Please go to the Premium Access page first.
                    </div>
                """, unsafe_allow_html=True)

    st.stop()



# --- CONTENUTO PRINCIPALE DELLA PAGINA (solo dopo login) ---

st.markdown("<div class='title-custom'>Drafted Players</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle-effect'>Browse players selected in the NBA Draft</div>", unsafe_allow_html=True)

# 📁 Percorsi relativi
current_dir = Path(__file__).parent
root_dir = current_dir.parent
df_path = root_dir / "college_players_final.csv"
empty_image_path = root_dir / "empty.png"
images_folder = root_dir / "images"

# 📊 Carica CSV
try:
    df = pd.read_csv(df_path)
except Exception as e:
    st.error(f"Errore nel caricamento del CSV: {e}")
    st.stop()

# 🖼 Immagine fallback
empty_img = Image.open(empty_image_path) if empty_image_path.exists() else None

# 🔍 Trova immagine del giocatore
def get_player_image_path(player_name):
    try:
        last, first = player_name.split(", ")
        base = f"{first}_{last}".replace(" ", "_")
    except:
        base = player_name.replace(" ", "_")
    for ext in ["png", "jpg", "jpeg"]:
        img_path = images_folder / f"{base}.{ext}"
        if img_path.exists():
            return img_path
    return None

# ✅ Controllo colonne
required = ['player_name', 'team', 'conf', 'weighted_scouting_score', 'pick', 'draft_year', 'year']
missing = [col for col in required if col not in df.columns]
if missing:
    st.error(f"Missing required columns: {', '.join(missing)}")
    st.stop()

# 📅 Selezione anno
available_years = sorted(df['year'].dropna().unique())
selected_year = st.selectbox("Select season year to analyze", available_years, index=len(available_years)-1)

# 🧹 Filtro + ordinamento
df_year = df[(df['year'] == selected_year) & (df['pick'].notna())]
order_option = st.selectbox("Sort players by", ['Pick number', 'Weighted score'])
if order_option == 'Pick number':
    df_year = df_year.sort_values('pick')
else:
    df_year = df_year.sort_values('weighted_scouting_score', ascending=False)

if df_year.empty:
    st.markdown("""
        <div style='
            background-color: #e0e0e0;
            padding: 12px;
            border-radius: 8px;
            color: black;
            font-weight: bold;
            font-size: 16px;
        '>
            No drafted players found for the selected year.
        </div>
    """, unsafe_allow_html=True)
else:
    for _, row in df_year.iterrows():
        img_candidate = get_player_image_path(row['player_name'])
        img = img_candidate if img_candidate and os.path.exists(img_candidate) else empty_image_path

        draft_year = int(row['draft_year']) if not pd.isna(row['draft_year']) else 'N/A'
        with st.container():
            col1, col2, col3, col4 = st.columns([1, 3, 1, 1])
            with col1:
                st.image(img, width=100)
            with col2:
                st.markdown(f"**{row['player_name']}**")
                st.markdown(f"{row['team']} - {row['conf']}")
            with col3:
                st.markdown(f"Score: {row['weighted_scouting_score']:.2f}")
            with col4:
                st.markdown(f"Pick: {int(row['pick'])} ({draft_year})")
