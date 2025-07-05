import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Drafted Players - Player List", layout='wide')

# Styling CSS from example
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@600&display=swap" rel="stylesheet">
    <style>
        html, body, .stApp {
            background-color: #f7f7f7 !important;
            color: #000 !important;
        }
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Orbitron', sans-serif !important;
            color: #f45208 !important;
        }
        .subtitle-effect {
            font-family: 'Orbitron', sans-serif;
            font-size: 1.2rem;
            color: #333;
            text-align: center;
            margin-bottom: 1rem;
        }
        .title-custom {
            font-family: 'Orbitron', sans-serif;
            font-size: 2.5rem;
            font-weight: 700;
            color: #f45208;
            text-align: center;
            margin-bottom: 0.5rem;
        }
        .player-container {
            display: flex;
            align-items: center;
            margin-bottom: 1rem;
            padding: 10px;
            background-color: #fff;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            color: #000 !important;
        }
        .player-photo {
            width: 100px;
            height: 100px;
            object-fit: cover;
            border-radius: 8px;
            margin-right: 15px;
        }
        .player-info {
            flex: 1;
            color: #000 !important;
        }
        .player-score, .player-pick {
            width: 120px;
            text-align: center;
            font-weight: bold;
            color: #000 !important;
        }
        .stMarkdown, .css-1cpxqw2, .css-q8sbsg {
            color: #000 !important;
        }

        /* 🟡 Etichette dei selectbox */
        label, .stSelectbox label, .stSelectbox div[data-baseweb="select"] {
            color: #000 !important;
            font-weight: bold;
        }

        /* 🟡 Testo messaggi informativi (come info/warning) */
        .stAlert {
            color: #000 !important;
        }
        .stAlert > div {
            color: #000 !important;
        }
    </style>
""", unsafe_allow_html=True)



st.markdown("<div class='title-custom'>Drafted Players</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle-effect'>Browse players selected in the NBA Draft</div>", unsafe_allow_html=True)

# Function to locate player images
def get_player_image_path(player_name):
    try:
        last, first = player_name.split(", ")
        base = f"{first}_{last}".replace(" ", "_")
    except:
        base = player_name.replace(" ", "_")
    for ext in ["png", "jpg", "jpeg"]:
        img_path = f"images/{base}.{ext}"
        if os.path.exists(img_path):
            return img_path
    return None

# Path to default empty image (replace with actual path as needed)
EMPTY_IMAGE_PATH = "/workspaces/ESAME/empty.png"

# Load CSV
df_path = "/workspaces/ESAME/college_players_final.csv"
try:
    df = pd.read_csv(df_path)
except Exception as e:
    st.error(f"Error loading CSV: {e}")
    st.stop()

# Verify required columns
required = ['player_name', 'team', 'conf', 'weighted_scouting_score', 'pick', 'draft_year']
missing = [col for col in required if col not in df.columns]
if missing:
    st.error(f"Missing required columns: {', '.join(missing)}")
    st.stop()

# Year selection (season year)
available_years = sorted(df['year'].dropna().unique())
selected_year = st.selectbox("Select season year to analyze", available_years, index=len(available_years)-1)

# Filter drafted players and ordering option
df_year = df[(df['year'] == selected_year) & (df['pick'].notna())]
order_option = st.selectbox("Sort players by", ['Pick number', 'Weighted score'])
if order_option == 'Pick number':
    df_year = df_year.sort_values('pick')
else:
    df_year = df_year.sort_values('weighted_scouting_score', ascending=False)

if df_year.empty:
    st.info("No drafted players found for the selected year.")
else:
    for _, row in df_year.iterrows():
        # Determine image path or fallback to empty image
        img_candidate = get_player_image_path(row['player_name'])
        img = img_candidate if img_candidate and os.path.exists(img_candidate) else EMPTY_IMAGE_PATH

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