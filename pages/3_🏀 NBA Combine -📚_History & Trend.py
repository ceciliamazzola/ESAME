import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from PIL import Image
import base64
from io import BytesIO
import os

# Percorsi portabili
st.set_page_config(layout="wide")
current_dir = Path(__file__).parent
df_path = current_dir.parent / "draft_history_fin.csv"
logo_folder = current_dir.parent / "logos"
players_img_folder = current_dir.parent / "images"  # <-- Cartella immagini giocatori
image_path = current_dir.parent / "bandiere" / "mappa.png"

# 🌐 Stile personalizzato Orbitron
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@600&display=swap" rel="stylesheet">
    <style>
        .stApp { background-color: #f7f7f7; }

        h1 { font-family: 'Orbitron', sans-serif !important; color: #f45208 !important; font-size: 2.5rem !important; }

        label, .stSelectbox label {
            color: black !important;
            font-weight: 600 !important;
        }

        .css-1jqq78o-control, .css-1pahdxg-control,
        .css-qbdosj-Input, .css-1dimb5e-singleValue {
            color: black !important;
            font-weight: 500;
        }

        .css-1d391kg hr { border-color: #ccc !important; }
    </style>
""", unsafe_allow_html=True)

# Titolo
st.markdown("""
    <div style='font-family: Orbitron, sans-serif; font-size: 2.5rem; font-weight: 700; color: #f45208; text-align: center; margin-bottom: 0.5rem;'>
        DRAFT HISTORY & TRENDS
    </div>
""", unsafe_allow_html=True)

# Sottotitolo
st.markdown("""
    <div style='font-family: Orbitron, sans-serif; font-size: 1.1rem; color: #333; text-align: center; margin-bottom: 1.5rem;'>
        Explore historical draft trends and discover every pick year by year
    </div>
""", unsafe_allow_html=True)

# Bottone indietro
st.markdown("""
    <form action="/" method="get">
        <button type="submit" style="
            padding: 10px 20px;
            background-color: #f45208;
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: bold;
            font-size: 16px;
            font-family: 'Orbitron', sans-serif;
            cursor: pointer;">
            ⬅️ Back to Menu
        </button>
    </form>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Dati draft
try:
    df = pd.read_csv(df_path)
    years = df["Year"].dropna().unique().astype(int)
    year = st.selectbox("Select a year", sorted(years))

    filtered_by_year = df[df["Year"] == year]
    round_options = sorted(filtered_by_year["Round Number"].dropna().unique().astype(int))
    round_selected = st.selectbox("Select a Round", round_options, index=0)

    filtered = (
        filtered_by_year[filtered_by_year["Round Number"] == round_selected]
        .drop(columns=["Unnamed: 0", "Round.1"], errors="ignore")
        .sort_values("Overall Pick")
    )

    st.markdown(
        f"<p style='color:black; font-size:24px; font-weight:bold;'>Draft {year} - Round {round_selected}</p>",
        unsafe_allow_html=True
    )

    def find_logo(abbrev):
        for ext in [".png", ".jpg", ".jpeg", ".svg"]:
            path = logo_folder / f"{abbrev}{ext}"
            if path.exists():
                return path
        return None

    for _, r in filtered.iterrows():
        col1, col2, col3 = st.columns([1, 4, 2])

        # Nome file immagine giocatore (Nome_Cognome)
        player_filename = r['Player'].replace(" ", "_")
        player_img_path = players_img_folder / f"{player_filename}.png"

        # Se l'immagine non esiste, usa empty.png
        if not player_img_path.exists():
            player_img_path = players_img_folder / "empty.png"

        # Colonna 1: immagine giocatore
        img = Image.open(player_img_path)
        img.thumbnail((80, 80), Image.LANCZOS)
        col1.image(img, use_container_width=False)

        # Colonna 2: nome e info pick
        col2.markdown(f"""
                <div style="padding: 4px 8px;">
                    <div style="font-size:18px; font-weight:bold; color: #222;">
                        {int(r['Overall Pick'])} – {r['Player']}
                    </div>
                    <div style="font-size:14px; color: #555;">
                        {int(r['Round Number'])}° Round, Pick {int(r['Round Pick'])}
                    </div>
                    <div style="font-size:14px; color: #555; font-style:italic;">
                        from: {r.get('Affiliation', 'N/A')}
                    </div>
                </div>
            """, unsafe_allow_html=True)

        # Colonna 3: logo squadra
        logo_path = find_logo(r["Team Abbreviation"])
        if logo_path:
            img = Image.open(logo_path)
            img.thumbnail((80, 80), Image.LANCZOS)
            col3.image(img, use_container_width=False)
        else:
            col3.markdown(f"<div style='text-align:center; font-size:16px; color:#333; padding-top:12px;'>{r['Team Abbreviation']}</div>", unsafe_allow_html=True)

        st.markdown("<hr style='border-color: #ccc; margin:10px 0;'>", unsafe_allow_html=True)

except Exception as e:
    st.error(f"Failed to load data: {e}")


# 📊 Grafico affiliations
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
    <label style='font-size:18px; font-weight:bold; color:black; font-family:Source Sans;'>
        Select how many affiliations to display:
    </label>
""", unsafe_allow_html=True)

top_n = st.selectbox("", [5, 10, 15], label_visibility="collapsed")
top_affiliations = df['Affiliation'].value_counts().head(top_n).reset_index()
top_affiliations.columns = ['Affiliation', 'Players']

# Sort the DataFrame in descending order by 'Players'
top_affiliations = top_affiliations.sort_values(by='Players', ascending=False)


st.markdown(f"""
    <h3 style='font-family: Orbitron, sans-serif; color:#000000; margin-bottom: 0.5em;'>
        Top {top_n} Player Affiliations Before Draft (2000-2024)
    </h3>
""", unsafe_allow_html=True)

custom_blue_scale = [
    [0.00, "#e1f5fe"],  # azzurro chiarissimo
    [0.07, "#cceaf6"],
    [0.13, "#b7dfef"],
    [0.20, "#a2d4e7"],
    [0.27, "#8dc9e0"],
    [0.33, "#78bec8"],
    [0.40, "#63b3c0"],
    [0.47, "#4ea8b8"],
    [0.53, "#479aa9"],
    [0.60, "#408c9a"],
    [0.67, "#397e8b"],
    [0.73, "#336f7c"],
    [0.80, "#2f6974"],
    [0.87, "#2f6974"],
    [1.00, "#2f6974"]
]


# Grafico bar aggiornato
fig = px.bar(
    top_affiliations,
    x='Players',
    y='Affiliation',
    orientation='h',
    text='Players',
    color='Players',
    color_continuous_scale=custom_blue_scale,
    category_orders={"Affiliation": top_affiliations['Affiliation'].tolist()}
)

fig.update_traces(
    textposition='outside',
    textfont_color='black'
)

fig.update_layout(
    plot_bgcolor='#f7f7f7',
    paper_bgcolor='#f7f7f7',
    font=dict(
        family='Orbitron, sans-serif',
        color='black'
    ),
    xaxis=dict(
        title=dict(text='Players', font=dict(color='black')),
        showgrid=False,
        tickfont=dict(color='black')
    ),
    yaxis=dict(
        title=dict(text='Affiliation', font=dict(color='black')),
        showgrid=False,
        tickfont=dict(color='black')
    ),
    coloraxis_colorbar=dict(
        title=dict(text='Players', font=dict(color='black')),
        tickfont=dict(color='black')
    ),
    showlegend=False,
    margin=dict(t=20, b=40, l=100, r=40)
)

st.plotly_chart(fig, use_container_width=True)




# 🌍 Mappa immagine
st.markdown("""
    <h3 style='font-family: Orbitron, sans-serif; color:#000000; margin-top: 2em;'>
        Player origin before draft (2000-2024)
    </h3>
""", unsafe_allow_html=True)

def image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

if image_path.exists():
    image = Image.open(image_path)

    st.markdown(f"""
        <div style='display: flex; justify-content: center; align-items: center;'>
            <img src='data:image/png;base64,{image_to_base64(image)}' style='max-width: 90%; height: auto;'/>
        </div>
    """, unsafe_allow_html=True)
else:
    st.warning("Image not found. Please check the path.")
