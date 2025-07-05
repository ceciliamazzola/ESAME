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
            font-weight: bold;
            color: #333;
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

def get_player_image_path(player_name):
    try:
        last, first = player_name.split(", ")
        base_name = f"{first}_{last}".replace(" ", "_")
    except:
        base_name = player_name.replace(" ", "_")
    for ext in ["png", "jpg", "jpeg"]:
        image_path = f"images/{base_name}.{ext}"
        if os.path.exists(image_path):
            return image_path
    return None


df = pd.read_csv("Draft_Combine_00_25.csv")

if df is not None:
    available_years = sorted(df['YEAR'].dropna().unique())
    selected_year = st.selectbox("Select draft year", available_years, index=len(available_years)-1)
    df_year = df[df['YEAR'] == selected_year]
    player_names = sorted(df_year['PLAYER'].dropna().unique())
    selected_player = st.selectbox("View detailed profile for a player", player_names)

    if selected_player:
        player_data = df_year[df_year['PLAYER'] == selected_player].iloc[0]
        col1, col2 = st.columns([1, 2])

        with col1:
            image_path = get_player_image_path(selected_player)
            if image_path:
                st.image(image_path, caption=selected_player, width=200)
            else:
                st.image("https://via.placeholder.com/250x350?text=No+Image", caption=selected_player, width=200)
                st.markdown(
            "<div style='color: #000; font-size: 0.9rem; margin-top: 0.5rem;'>No available picture for this player.</div>",
            unsafe_allow_html=True
        )
        with col2:
            st.subheader(f"{selected_player}")
            st.markdown(f"**Position:** {player_data['POS']}")
            st.markdown(f"**Height:** {player_data['HGT']} inches")
            st.markdown(f"**Weight:** {player_data['WGT']} lbs")
            st.markdown(f"**BMI:** {player_data['BMI']:.1f}" if pd.notna(player_data['BMI']) else "**BMI:** N/A")
            st.markdown(f"**Body Fat %:** {player_data['BF']}" if pd.notna(player_data['BF']) else "**Body Fat %:** N/A")
            st.markdown(f"**Wingspan:** {player_data['WNGSPN']} inches")

        st.markdown("---")

    selected_players = st.multiselect("Compare players from the same year", player_names, default=[selected_player])

    if selected_players:
        selected_df = df_year[df_year['PLAYER'].isin(selected_players)]
        st.subheader("Physical Attributes Comparison")

        phys_metrics = ["HGT", "WGT", "BMI", "BF", "WNGSPN", "STNDRCH"]
        selected_phys = st.multiselect("Select physical metrics to display", phys_metrics, default=["HGT", "WGT", "BMI"])

        if "HGT" in selected_phys and "WGT" in selected_phys:
            col_hgt, col_wgt = st.columns(2)
            with col_hgt:
                fig_hgt = px.bar(selected_df, x="PLAYER", y="HGT", text="HGT")
                fig_hgt.update_traces(textposition='outside', marker=dict(color='#326974'))
                fig_hgt.update_layout(
                    title="Height Comparison",
                    margin=dict(t=40),
                    plot_bgcolor='#f7f7f7',
                    paper_bgcolor='#f7f7f7',
                    font_color='#000',
                    title_font=dict(color='#000'),
                    xaxis=dict(
                        title_font=dict(color='#000'),
                        tickfont=dict(color='#000')
                    ),
                    yaxis=dict(
                        title_font=dict(color='#000'),
                        tickfont=dict(color='#000')
                    ),
                    legend=dict(font=dict(color='#000'))
                )
                st.plotly_chart(fig_hgt, use_container_width=True)

            with col_wgt:
                fig_wgt = px.bar(selected_df, x="PLAYER", y="WGT", text="WGT")
                fig_wgt.update_traces(textposition='outside', marker=dict(color='#326974'))
                fig_wgt.update_layout(
                    title="Weight Comparison",
                    margin=dict(t=40),
                    plot_bgcolor='#f7f7f7',
                    paper_bgcolor='#f7f7f7',
                    font_color='#000',
                    title_font=dict(color='#000'),
                    xaxis=dict(
                        title_font=dict(color='#000'),
                        tickfont=dict(color='#000')
                    ),
                    yaxis=dict(
                        title_font=dict(color='#000'),
                        tickfont=dict(color='#000')
                    ),
                    legend=dict(font=dict(color='#000'))
                )
                st.plotly_chart(fig_wgt, use_container_width=True)



            selected_phys = [m for m in selected_phys if m not in ["HGT", "WGT"]]

        if "BMI" in selected_phys:
            st.markdown("<div style='font-size: 20px; font-weight: bold; color: black; margin-bottom: 10px;'>BMI Overview</div>", unsafe_allow_html=True)
            for _, row in selected_df.iterrows():
                bmi_value = row['BMI'] if pd.notna(row['BMI']) else 0
                bmi_percent = min(max(bmi_value / 35, 0), 1)
                st.markdown(f"""
                    <div style='margin-bottom: 1rem;'>
                        <strong style='color:black;'>{row['PLAYER']}</strong><br>
                        <div style='position: relative; background: #ddd; border-radius: 12px; height: 28px; width: 100%;'>
                            <div style='background: #f45208; height: 100%; width: {bmi_percent*100:.1f}%; border-radius: 12px;'></div>
                            <div style='position: absolute; top: 0; left: 50%; transform: translateX(-50%); color: white; font-weight: bold; font-size: 15px; line-height: 28px;'>
                                {bmi_value:.1f} BMI
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            selected_phys = [m for m in selected_phys if m != "BMI"]

        if "WNGSPN" in selected_phys:
            st.markdown("<div style='font-size: 20px; font-weight: bold; color: black; margin-bottom: 10px;'>Wingspan Overview</div>", unsafe_allow_html=True)
            for _, row in selected_df.iterrows():
                st.markdown(f"<strong style='color: black;'>{row['PLAYER']}</strong> — <span style='color: black;'>{row['WNGSPN']} inches</span>", unsafe_allow_html=True)
                st.markdown("<div style='height: 2px; background-color: #ccc; margin: 8px 0 20px 0;'></div>", unsafe_allow_html=True)
            selected_phys = [m for m in selected_phys if m != "WNGSPN"]

        if "STNDRCH" in selected_phys:
            st.markdown("<div style='font-size: 20px; font-weight: bold; color: black; margin-bottom: 10px;'>Standing Reach Overview</div>", unsafe_allow_html=True)
            for _, row in selected_df.iterrows():
                st.markdown(f"<strong style='color: black;'>{row['PLAYER']}</strong> — <span style='color: black;'>{row['STNDRCH']} inches</span>", unsafe_allow_html=True)
                st.markdown("<div style='height: 2px; background-color: #ccc; margin: 8px 0 20px 0;'></div>", unsafe_allow_html=True)
            selected_phys = [m for m in selected_phys if m != "STNDRCH"]


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
    <span style='color: #f8961e; font-weight: bold;'>Orange</span> indicates equal.
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
                color1 = color2 = "#f8961e"  # pari

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
