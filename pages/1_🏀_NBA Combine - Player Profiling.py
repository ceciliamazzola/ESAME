import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from sklearn.preprocessing import MinMaxScaler

st.set_page_config(page_title="Player Profiling - Next Gen Draft",
                   layout='wide')

# Stile coerente con la homepage
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@600&display=swap" rel="stylesheet">
    <style>
        html, body, .stApp {
            background-color: #f7f7f7 !important;
            color: #333 !important;
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
        .metric-label {
            font-family: 'Orbitron', sans-serif;
            font-weight: bold;
            font-size: 1.3rem;
            color: #333 !important;
            margin-top: 12px;
            margin-bottom: 4px;
        }
        .bar-wrapper {
            background-color: #ddd;
            height: 28px;
            border-radius: 14px;
            overflow: hidden;
            position: relative;
        }
        .bar {
            height: 100%;
            font-weight: bold;
            text-align: right;
            padding-right: 12px;
            line-height: 28px;
            font-size: 16px;
            color: transparent;
        }
        .bar-value {
            position: absolute;
            right: 10px;
            top: 0;
            height: 28px;
            line-height: 28px;
            font-size: 16px;
            font-weight: bold;
            color: #333;
        }
        label, .stSelectbox label, .stMultiSelect label {
            color: #000 !important;
            font-weight: bold;
        }
        .css-1wa3eu0-option, .css-1n76uvr {
            color: #000 !important;
        }
        .css-1pahdxg-control, .css-1s2u09g-control, .css-1uccc91-singleValue {
            color: #000 !important;
        }
        .css-1r6slb0 {
            color: #000 !important;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
/* Etichette dei widget */
label, .stSelectbox label, .stMultiSelect label {
    color: #000 !important;
    font-weight: bold;
}

/* Opzioni nei menu a discesa */
.css-1wa3eu0-option, .css-1n76uvr {
    color: #000 !important;
}

/* Testo selezionato nei dropdown */
.css-1pahdxg-control, .css-1s2u09g-control, .css-1uccc91-singleValue {
    color: #000 !important;
}

/* Testo nei multi-select */
.css-1r6slb0 {
    color: #000 !important;
}

/* Nome giocatore sopra le barre */
.metric-label {
    color: #000 !important;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='title-custom'>PLAYER PROFILING</div>", unsafe_allow_html=True)

st.markdown("<div class='subtitle-effect'>Analyze the physical and athletic profiles of draft prospects</div>", unsafe_allow_html=True)

# Bottone indietro
st.markdown("""
    <form action="/" method="get">
        <button type="submit" style="
            padding: 10px 20px;
            background-color: #f7f7f7;
            color: black;
            border: 2px solid black !important;
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

import os
import glob

import os
import glob

def get_player_image_path(player_name):
    """
    Restituisce il percorso dell'immagine di un giocatore, cercando:
      1) nomi esatti con underscore o trattino
      2) wildcard con underscore o trattino
    Se non trova nulla, torna 'images/empty.png' e flag di fallback a True.
    """
    # Provo a fare split "Cognome, Nome"
    try:
        last, first = player_name.split(", ")
        base_name = f"{first}_{last}"
    except ValueError:
        # Se non c'è la virgola, considero tutto come nome unico
        base_name = player_name.replace(" ", "_")

    # Normalizzo doppie underscore o spazi residui
    base_name = "_".join(part for part in base_name.split("_") if part)

    exts = ("png", "jpg", "jpeg")
    # Variazioni da provare: con underscore e con trattino
    name_variants = { base_name, base_name.replace("_", "-") }

    # 1) Ricerca esatta
    for name in name_variants:
        for ext in exts:
            path = os.path.join("images", f"{name}.{ext}")
            if os.path.exists(path):
                return path, False

    # 2) Ricerca wildcard
    for name in name_variants:
        for ext in exts:
            pattern = os.path.join("images", f"*{name}*.{ext}")
            matches = glob.glob(pattern)
            if matches:
                # potresti ordinarli se vuoi
                return matches[0], False

    # 3) Fallback
    return "images/empty.png", True


import matplotlib.pyplot as plt
df = pd.read_csv("Draft_Combine_00_25.csv")

import os
import glob
import streamlit as st
import pandas as pd

# Funzione per recuperare immagine giocatore
def get_player_image_path(player_name):
    try:
        last, first = player_name.split(", ")
        base_name = f"{first}_{last}"
    except ValueError:
        base_name = player_name.replace(" ", "_")
    base_name = "_".join(part for part in base_name.split("_") if part)
    exts = ("png", "jpg", "jpeg")
    variants = {base_name, base_name.replace("_", "-")}
    for name in variants:
        for ext in exts:
            path = os.path.join("images", f"{name}.{ext}")
            if os.path.exists(path):
                return path, False
    for name in variants:
        for ext in exts:
            matches = glob.glob(os.path.join("images", f"*{name}*.{ext}"))
            if matches:
                return matches[0], False
    return "images/empty.png", True

# Caricamento dataset

import os
import glob
import streamlit as st
import pandas as pd

# Funzione per recuperare immagine giocatore
def get_player_image_path(player_name):
    try:
        last, first = player_name.split(", ")
        base_name = f"{first}_{last}"
    except ValueError:
        base_name = player_name.replace(" ", "_")
    base_name = "_".join(part for part in base_name.split("_") if part)
    exts = ("png", "jpg", "jpeg")
    variants = {base_name, base_name.replace("_", "-")}
    for name in variants:
        for ext in exts:
            path = os.path.join("images", f"{name}.{ext}")
            if os.path.exists(path):
                return path, False
    for name in variants:
        for ext in exts:
            matches = glob.glob(os.path.join("images", f"*{name}*.{ext}"))
            if matches:
                return matches[0], False
    return "images/empty.png", True




# Selezione anno
years = sorted(df['YEAR'].dropna().unique())
selected_year = st.selectbox("Select Draft Year", years, index=len(years)-1)
df_year = df[df['YEAR'] == selected_year]

# Selezione giocatore singolo
player_names = sorted(df_year['PLAYER'].dropna().unique())
selected_player = st.selectbox("View detailed profile for a player", player_names)

if selected_player:
    data = df_year[df_year['PLAYER'] == selected_player].iloc[0]
    c1, c2 = st.columns([1,2])
    with c1:
        img_path, fallback = get_player_image_path(selected_player)
        st.image(img_path, caption=selected_player, width=200)
        if fallback:
            st.markdown("<div style='color:#666; font-size:0.9rem;'>No available picture for this player.</div>", unsafe_allow_html=True)
    with c2:
        st.subheader(selected_player)
        st.markdown(f"**Position:** {data['POS']}")
        st.markdown(f"**Height:** {data['HGT']} inches")
        st.markdown(f"**Weight:** {data['WGT']} lbs")
        bmi = f"{data['BMI']:.1f}" if pd.notna(data['BMI']) else "N/A"
        st.markdown(f"**BMI:** {bmi}")
        bf = f"{data['BF']:.1f}" if pd.notna(data['BF']) else "N/A"
        st.markdown(f"**Body Fat %:** {bf}")
        st.markdown(f"**Wingspan:** {data['WNGSPN']} inches")
    st.markdown("---")


# Confronto multiplo con barre orizzontali normalizzate al valore massimo del dataset
# Confronto multiplo con barre orizzontali normalizzate al massimo dataset
selected_players = st.multiselect(
    "Compare players from the same year", player_names,
    default=[selected_player] if selected_player else []
)
if selected_players:
    df_sel = df_year[df_year['PLAYER'].isin(selected_players)]
    st.subheader("Physical Attributes Comparison")

    # Definizione metriche con massimo globale\    
    metrics = {
        'HGT':    {'label': 'Height',   'unit': 'inches', 'max': df['HGT'].max()},
        'WGT':    {'label': 'Weight',   'unit': 'lbs',    'max': df['WGT'].max()},
        'BMI':    {'label': 'BMI',      'unit': '',       'max': df['BMI'].max()},
        'WNGSPN': {'label': 'Wingspan','unit': 'inches', 'max': df['WNGSPN'].max()},
        'STNDRCH':{'label': 'Standing Reach', 'unit': 'inches', 'max': df['STNDRCH'].max()}
    }



    # Seleziona metriche da visualizzare
    chosen = st.multiselect(
        "Select physical metrics to display (bars normalized to dataset max)",
        options=list(metrics.keys()),
        default=list(metrics.keys())
    )
    if not chosen:
        st.info("Select at least one metric to display.")
    else:
        # Visualizza ogni metrica con barre orizzontali
        for metric in chosen:
            cfg = metrics[metric]
            # Sottotitolo in nero
            unit_str = f" ({cfg['unit']})" if cfg['unit'] else ""
            st.markdown(
                f"<div class='metric-label'>{cfg['label']} ({cfg['unit']})</div>",
                unsafe_allow_html=True
            )
            # Barre per ciascun giocatore
            for _, row in df_sel.iterrows():
                val = row[metric] if pd.notna(row[metric]) else 0
                pct = val / cfg['max'] if cfg['max'] else 0
                pct = max(0, min(pct, 1))
                display = f"{val:.1f} {cfg['unit']}" if cfg['unit'] else f"{val:.1f}"
                bar_html = f"""
                <div style='margin-bottom:0.75rem;'>
                  <strong>{row['PLAYER']}</strong>
                  <div style='position:relative; background:#ddd; border-radius:8px; height:28px; overflow:hidden;'>
                    <div style='background:#326974; width:{pct*100:.1f}%; height:100%;'></div>
                    <div style='position:absolute; top:0; left:50%; transform:translateX(-50%); color:white; font-weight:bold; line-height:28px;'>
                      {display}
                    </div>
                  </div>
                </div>
                """
                st.markdown(bar_html, unsafe_allow_html=True)
            st.markdown("---")
else:
    st.warning("Select at least one player to compare.")



# Caricamento dati
import streamlit as st
import pandas as pd

st.subheader("Athletic Performance Comparison")
df = pd.read_csv("Draft_Combine_00_25.csv")

# Selezione anno e giocatori
available_years = sorted(df['YEAR'].dropna().unique())
selected_year = st.selectbox("Select draft year", available_years, index=len(available_years) - 1, key="athletic_year")
df_year = df[df['YEAR'] == selected_year]
player_names = sorted(df_year['PLAYER'].dropna().unique())
selected_players = st.multiselect("Select 2 players to compare", player_names, max_selections=2)

# Etichette metriche e selezione
metric_labels = {
    "STNDVERT": "Standing Vertical Jump",
    "LPVERT": "Max Vertical Jump",
    "LANE": "Lane Agility Time",
    "SHUTTLE": "Shuttle Run",
    "SPRINT": "Three-Quarter Sprint",
}
athletic_metrics = list(metric_labels.keys())
selected_metrics = st.multiselect("Select athletic metrics to compare", athletic_metrics, default=athletic_metrics)
st.markdown("""
<p style='margin-top: -10px; margin-bottom: 20px; font-size: 15px; color: black;'>
    <span style='color: #43aa8b; font-weight: bold;'>Green</span> indicates better performance, 
    <span style='color: #f94144; font-weight: bold;'>Red</span> indicates worse, 
    <span style='color: #9d9891; font-weight: bold;'>Grey</span> indicates equal.
</p>
""", unsafe_allow_html=True)

# Stile CSS personalizzato
st.markdown("""
    <style>
        .metric-label {
            font-weight: bold;
            color: #333;
            margin-top: 12px;
            margin-bottom: 4px;
        }
    </style>
""", unsafe_allow_html=True)

# Massimi assoluti noti
max_values_dict = {
    "STNDVERT": 41.50,
    "LPVERT": 48.00,
    "LANE": 14.45,
    "SHUTTLE": 3.76,
    "SPRINT": 4.00
}

# Visualizzazione se selezionati due giocatori e metriche
if len(selected_players) == 2 and selected_metrics:
    player1_data = df_year[df_year['PLAYER'] == selected_players[0]][selected_metrics]
    player2_data = df_year[df_year['PLAYER'] == selected_players[1]][selected_metrics]

    if not player1_data.empty and not player2_data.empty:
        combined = pd.concat([player1_data, player2_data]).dropna(axis=1)
        used_metrics = combined.columns.tolist()

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"<div class='metric-label' style='font-size: 18px; color: black;'>{selected_players[0]}</div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='metric-label' style='font-size: 18px; color: black;'>{selected_players[1]}</div>", unsafe_allow_html=True)

        for metric in used_metrics:
            label = metric_labels.get(metric, metric)
            val1 = player1_data[metric].values[0]
            val2 = player2_data[metric].values[0]

            max_val = max_values_dict.get(metric, 1)
            percent1 = min(100, (val1 / max_val) * 100)
            percent2 = min(100, (val2 / max_val) * 100)

            # Migliore = verde, Peggiore = rosso, Parità = arancione
            best_is_lower = metric in ["LANE", "SHUTTLE", "SPRINT"]

            if (val1 < val2 and best_is_lower) or (val1 > val2 and not best_is_lower):
                color1 = "#43aa8b"  # verde
                color2 = "#f94144"  # rosso
            elif (val2 < val1 and best_is_lower) or (val2 > val1 and not best_is_lower):
                color1 = "#f94144"
                color2 = "#43aa8b"
            else:
                color1 = color2 = "#9d9891"  # pari

            # Visualizza barre per Player 1
            with col1:
                st.markdown(f"<div class='metric-label'>{label}</div>", unsafe_allow_html=True)
                st.markdown(f"""
                    <div style='margin-bottom: 18px; display: flex; align-items: center;'>
                        <div style='flex: 1; background-color: #ddd; border-radius: 20px; overflow: hidden; height: 28px;'>
                            <div style='width: {percent1:.1f}%; background-color: {color1}; height: 100%;'></div>
                        </div>
                        <div style='margin-left: 8px; font-weight: bold; font-size: 16px; color: black;'>{val1:.1f}</div>
                    </div>
                """, unsafe_allow_html=True)

            # Visualizza barre per Player 2
            with col2:
                st.markdown(f"<div class='metric-label'>&nbsp;</div>", unsafe_allow_html=True)
                st.markdown(f"""
                    <div style='margin-bottom: 18px; display: flex; align-items: center;'>
                        <div style='flex: 1; background-color: #ddd; border-radius: 20px; overflow: hidden; height: 28px;'>
                            <div style='width: {percent2:.1f}%; background-color: {color2}; height: 100%;'></div>
                        </div>
                        <div style='margin-left: 8px; font-weight: bold; font-size: 16px; color: black;'>{val2:.1f}</div>
                    </d
                """, unsafe_allow_html=True)
    else:
        st.markdown("<p style='color: #000;'>One or both players have incomplete data for selected metrics.</p>", unsafe_allow_html=True)
else:
    st.markdown("<p style='color: #000;'>Please select two players and at least one metric to compare.</p>", unsafe_allow_html=True)
