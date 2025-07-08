import streamlit as st

# Applica font Orbitron e stile globale petrolio + testo bianco
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@600&display=swap" rel="stylesheet">
    <style>
        .stApp {
            background-color: #2f6974 !important;
        }

        div, p, span, label {
            color: #ffffff !important;
        }

        input {
            background-color: #2f6974 !important;
            color: #ffffff !important;
            border: 1px solid #ffffff !important;
        }

        h3 {
            font-family: 'Orbitron', sans-serif !important;
            color: #f45208 !important;
        }

        .info-box {
            background-color: #2f6974;
            padding: 20px;
            border-radius: 10px;
            color: white;
            font-family: 'Arial', sans-serif;
        }
    </style>
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
st.markdown("<br>", unsafe_allow_html=True)  # Una riga vuota

# Box informativo con stile coerente
st.markdown("""
<div class="info-box">
    <h3>📌 Project Information</h3>
    <p>
        Questo progetto è stato sviluppato nell’ambito di un corso di laurea del 
        <strong>Politecnico di Milano</strong>. I dati utilizzati provengono dai siti ufficiali della 
        <strong>NBA</strong> e sono stati impiegati esclusivamente per finalità didattiche e di ricerca.
    </p>
    <p>
        Di seguito sono riportati i contatti dei membri del team di sviluppo.
    </p>
    <p>
        Cecilia Mazzola: cecilia.mazzola@mail.polimi.it<br>
        Filippo Toniolo: filippo.toniolo@mail.polimi.it
    </p>
</div>
""", unsafe_allow_html=True)



import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from PIL import Image
import base64
from io import BytesIO
import os

# Percorsi portabili
current_dir    = Path(__file__).parent
df_path        = current_dir.parent / "draft_history_fin.csv"
logo_folder    = current_dir.parent / "logos"
images_folder  = current_dir.parent / "images"   # ← nuova variabile per le immagini dei giocatori
image_path     = current_dir.parent / "bandiere" / "mappa.png"
default_player_image = images_folder / "empty.png"

# 🌐 Stile personalizzato Orbitron
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@600&display=swap" rel="stylesheet">
    <style>
        .stApp { background-color: #f7f7f7; }
        /* … (resto del CSS invariato) … */
    </style>
""", unsafe_allow_html=True)

# Titoli e bottoni (invariati) …

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

    # Funzione per trovare il logo
    def find_logo(abbrev):
        for ext in [".png", ".jpg", ".jpeg", ".svg"]:
            path = logo_folder / f"{abbrev}{ext}"
            if path.exists():
                return path
        return None

    # Nuova funzione per trovare l’immagine del giocatore
    def find_player_image(name):
        file_name = name.replace(" ", "_")
        for ext in [".png", ".jpg", ".jpeg"]:
            path = images_folder / f"{file_name}{ext}"
            if path.exists():
                return path
        # se non trova nulla, restituisce il default
        return default_player_image if default_player_image.exists() else None

    for _, r in filtered.iterrows():
        col1, col2, col3 = st.columns([1, 4, 2])

        # 1) Colonna immagine giocatore
        player_img_path = find_player_image(r["Player"])
        if player_img_path:
            img = Image.open(player_img_path)
            img.thumbnail((80, 80), Image.LANCZOS)
            col1.image(img, use_container_width=False)
        else:
            col1.markdown(
                f"<div style='text-align:center; font-size:20px; font-weight:bold; color:#777;'>No.{int(r['Overall Pick'])}</div>",
                unsafe_allow_html=True
            )

        # 2) Colonna dati testuali: No.{pick} - Player
                # 2) Colonna dati testuali: No.{pick} – Player + round + affiliation
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


        # 3) Colonna logo squadra (invariata)
        logo_path = find_logo(r["Team Abbreviation"])
        if logo_path:
            logo = Image.open(logo_path)
            logo.thumbnail((80, 80), Image.LANCZOS)
            col3.image(logo, use_container_width=False)
        else:
            col3.markdown(
                f"<div style='text-align:center; font-size:16px; color:#333; padding-top:12px;'>{r['Team Abbreviation']}</div>",
                unsafe_allow_html=True
            )

        st.markdown("<hr style='border-color: #ccc; margin:10px 0;'>", unsafe_allow_html=True)

except Exception as e:
    st.error(f"Failed to load data: {e}")
