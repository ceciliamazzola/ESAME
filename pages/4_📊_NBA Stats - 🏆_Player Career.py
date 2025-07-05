import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os
import base64
# ----------------------
# Page Configuration
# ----------------------
st.set_page_config(
    page_title="PLAYER CAREER",
    layout="wide"
)

# 🌐 Tema chiaro personalizzato
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@600&display=swap" rel="stylesheet">
    <style>
        .stApp { background-color: #f7f7f7; }
        h1 { font-family: 'Orbitron', sans-serif !important; color: #f45208 !important; font-size: 2.5rem !important; }
        .streamlit-expanderHeader, .css-18e3th9, .css-10trblm { color: #333 !important; }
        .css-1d391kg hr { border-color: #ccc !important; }
        label, .stSelectbox label { color: #000 !important; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)



# ----------------------
# Data Loading
# ----------------------
@st.cache_data

def load_data(path: str):
    df = pd.read_csv(path)
    df = df[df['season'] >= 2000].copy()

    df['fg_mul'] = df['fg_percent'] * df['g']
    df['ft_mul'] = df['ft_percent'] * df['g']

    games_df = df.groupby('player_x', as_index=False).agg(TotalGames=('g','sum'))

    fg_df = df.groupby('player_x', as_index=False).agg(
        FGSum=('fg_mul','sum'),
        Games=('g','sum')
    )
    fg_df['FG%'] = fg_df['FGSum'] / fg_df['Games'] * 100

    pct_df = (
        df.drop_duplicates('player_x')
          .loc[:, ['player_x','career_x2p_percent','career_x3p_percent','career_ft_percent','career_e_fg_percent']]
          .rename(columns={
              'career_x2p_percent':'2P%',
              'career_x3p_percent':'3P%',
              'career_ft_percent':'FT%',
              'career_e_fg_percent':'eFG%'
          })
    )

    pg_df = (
        df.drop_duplicates('player_x')
          .loc[:, ['player_x','career_pts_per_g','career_trb_per_g',
                   'career_ast_per_g','career_tov_per_g','career_orb','career_drb']]
          .rename(columns={
              'career_pts_per_g':'PTS/G',
              'career_trb_per_g':'TRB/G',
              'career_ast_per_g':'AST/G',
              'career_tov_per_g':'TOV/G',
              'career_orb':'ORB',
              'career_drb':'DRB'
          })
    )

    career_df = fg_df.merge(pct_df, on='player_x').merge(pg_df, on='player_x')
    career_df = career_df.merge(games_df, on='player_x')
    career_df['ORB/G'] = career_df['ORB'] / career_df['TotalGames']
    career_df['DRB/G'] = career_df['DRB'] / career_df['TotalGames']

    career_df = career_df.rename(columns={'player_x':'player'})
    career_df = career_df.drop(columns=['FGSum','Games','TotalGames','ORB','DRB'])

    return career_df

career_df = load_data('Player Final.csv')

# ----------------------
# Title and Selector
# ----------------------
st.markdown("""
    <div style='font-family: Orbitron, sans-serif; font-size: 2.5rem; font-weight: 700; color: #f45208; text-align: center; margin-bottom: 0.5rem;'>
        PLAYER CAREER
    </div>
""", unsafe_allow_html=True)
# ----------------------
# Subtitle
# ----------------------
st.markdown("""
    <div style='font-family: Orbitron, sans-serif; font-size: 1.1rem; font-weight: bold;color: #333; text-align: center; margin-bottom: 2rem;'>
        Analyze each player’s career performance compared to NBA league averages across multiple metrics
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
st.markdown("<br>", unsafe_allow_html=True)  # Una riga vuota

# Player selector
st.markdown("<label style='color: black; font-weight: bold;'>Select a player:</label>", unsafe_allow_html=True)
players = sorted(career_df['player'].unique())
selected_player = st.selectbox("", options=players, index=players.index("LeBron James") if "LeBron James" in players else 0)

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
>>>>>>> fa26ecd (Backmenubutton)
# ----------------------
# Player Image
# ----------------------
# ----------------------
# Player Image (Centered)
# ----------------------
img_file = None
for ext in ['png', 'jpg', 'jpeg']:
    candidate = f"{selected_player}.{ext}"
    if os.path.isfile(candidate):
        img_file = candidate
        break

if not img_file:
    try:
        last, first = selected_player.split(", ")
        base_name = f"{first}_{last}".replace(" ", "_")
    except:
        base_name = selected_player.replace(" ", "_")

    for ext in ['png', 'jpg', 'jpeg']:
        candidate = f"images/{base_name}.{ext}"
        if os.path.isfile(candidate):
            img_file = candidate
            break

# Mostra immagine centrata o testo centrato
# ----------------------
# Player Image (Perfectly Centered)
# ----------------------
center_container = st.container()

with center_container:
    if img_file:
        st.markdown(f"""
            <div style='text-align: center;'>
                <img src='data:image/png;base64,{base64.b64encode(open(img_file, "rb").read()).decode()}' 
                     width='250' style='margin-bottom: 8px;'/>
                <div style='font-size: 18px; color: black; font-weight: bold;'>{selected_player}</div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style='text-align: center; color: black; font-size: 16px; margin-top: 10px;'>
                Photo not available for the selected player.
            </div>
        """, unsafe_allow_html=True)

# ----------------------
# Radar Charts
# ----------------------
# ----------------------
# Radar Charts with Orbitron Font in Titles

# ----------------------
st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    perc_metrics = ['FG%','2P%','3P%','FT%','eFG%']
    player_perc = career_df.loc[career_df['player']==selected_player, perc_metrics].iloc[0]
    league_avg_perc = career_df[perc_metrics].mean()
    radar_perc = pd.DataFrame({
        'Metric': perc_metrics*2,
        'Value': list(player_perc) + list(league_avg_perc),
        'Group': [selected_player]*len(perc_metrics) + ['NBA Avg']*len(perc_metrics)
    })
    fig_perc = px.line_polar(
        radar_perc,
        r='Value',
        theta='Metric',
        color='Group',
        line_close=True,
        labels={'Group': 'Legend'}
    )
    fig_perc.update_layout(
        title=dict(
            text="Shooting % vs NBA Avg",
            x=0,
            xanchor="left",
            font=dict(family="Orbitron, sans-serif", size=22, color="black")
        ),
        plot_bgcolor="#f7f7f7",
        paper_bgcolor="#f7f7f7",
        font=dict(family="Orbitron, sans-serif", size=16, color='black'),
        polar=dict(
            radialaxis=dict(tickfont=dict(size=14, color='black')),
            angularaxis=dict(tickfont=dict(size=14, color='black'))
        ),
        legend=dict(font=dict(size=14, color='black'), title_font=dict(size=14, color='black'))
    )
    st.plotly_chart(fig_perc, use_container_width=True)

with col2:
    pg_metrics = ['PTS/G','TRB/G','AST/G','TOV/G','ORB/G','DRB/G']
    player_pg = career_df.loc[career_df['player']==selected_player, pg_metrics].iloc[0]
    league_avg_pg = career_df[pg_metrics].mean()
    radar_pg = pd.DataFrame({
        'Metric': pg_metrics*2,
        'Value': list(player_pg) + list(league_avg_pg),
        'Group': [selected_player]*len(pg_metrics) + ['NBA Avg']*len(pg_metrics)
    })
    fig_pg = px.line_polar(
        radar_pg,
        r='Value',
        theta='Metric',
        color='Group',
        line_close=True,
        labels={'Group': 'Legend'}
    )
    fig_pg.update_layout(
        title=dict(
            text="Per Game Stats vs NBA Avg",
            x=0,
            xanchor="left",
            font=dict(family="Orbitron, sans-serif", size=22, color="black")
        ),
        plot_bgcolor="#f7f7f7",
        paper_bgcolor="#f7f7f7",
        font=dict(family="Orbitron, sans-serif", size=16, color='black'),
        polar=dict(
            radialaxis=dict(tickfont=dict(size=14, color='black')),
            angularaxis=dict(tickfont=dict(size=14, color='black'))
        ),
        legend=dict(font=dict(size=14, color='black'), title_font=dict(size=14, color='black'))
    )
    st.plotly_chart(fig_pg, use_container_width=True)


# … codice precedente ai radar …
from pathlib import Path

current_dir = Path(__file__).parent
logo_dir = current_dir.parent / "logos"

# Carico di nuovo il raw dataframe (non solo career_df), per poter pescare le stagioni
@st.cache_data
def load_raw(path: str):
    return pd.read_csv(path)

raw_df = load_raw('Player Final.csv')

# Dropdown per la stagione, filtrata in base al giocatore selezionato
available_seasons = (
    raw_df[raw_df['player_x'] == selected_player]['season']
    .dropna()
    .astype(int)
    .sort_values(ascending=False)
    .unique()
)

st.markdown("---")
st.markdown("""
    <h3 style="color: black; font-family: 'Orbitron', sans-serif; margin-top: 2rem;">
        Season Stats
    </h3>
""", unsafe_allow_html=True)

selected_season = st.selectbox("Pick a season:", available_seasons)

# Recupero i dati di quella stagione
season_row = raw_df[
    (raw_df['player_x'] == selected_player) &
    (raw_df['season'] == selected_season)
].iloc[0]

# Preparo le metriche
season_stats = {
    "Team": season_row["tm"],
    "G (Games)": int(season_row["g"]),
    "MPG": round(season_row["mp"] / season_row["g"], 1),
    "PPG": round(season_row["pts"] / season_row["g"], 1),
    "RPG": round(season_row["trb"] / season_row["g"], 1),
    "APG": round(season_row["ast"] / season_row["g"], 1),
    "SPG": round(season_row["stl"] / season_row["g"], 1),
    "BPG": round(season_row["blk"] / season_row["g"], 1),
    "TO/G": round(season_row["tov"] / season_row["g"], 1),
    "FG%": round(season_row["fg_percent"] * 100, 1),
    "3P%": round(season_row["x3p_percent"] * 100, 1),
    "FT%": round(season_row["ft_percent"] * 100, 1),
}

# CSS custom
st.markdown("""
    <style>
    .stat-card {
        background: #f7f9fc;
        border-left: 4px solid #ff4500;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 12px;
        text-align: center;
    }
    .stat-label { color: #555; font-size: 0.9rem; }
    .stat-value { color: #1f2c56; font-size: 1.8rem; font-weight: bold; }
    .team-logo { margin-bottom: 8px; height: 50px; }
    </style>
""", unsafe_allow_html=True)
# CSS per grid e card armoniche
st.markdown("""
    <style>
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 16px;
        margin-top: 16px;
    }
    .stat-card {
        background: #f7f9fc;
        border-left: 4px solid #ff4500;
        border-radius: 8px;
        padding: 16px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 160px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .stat-label {
        color: #555;
        font-size: 0.9rem;
        margin-top: 8px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .stat-value {
        color: #1f2c56;
        font-size: 1.8rem;
        font-weight: bold;
        margin-top: 4px;
    }
    .team-logo {
        height: 50px;
        margin-bottom: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# Genera l’HTML della grid con data-URI per i loghi
cards_html = '<div class="stats-grid">'
for label, value in season_stats.items():
    cards_html += '<div class="stat-card">'
    if label == "Team":
        # cerco il file logo
        logo_path, logo_ext = None, None
        for ext in ("png", "jpg", "jpeg"):
            candidate = logo_dir / f"{value}.{ext}"
            if candidate.is_file():
                logo_path, logo_ext = candidate, ext
                break

        if logo_path:
            # leggo e converto in base64
            with open(logo_path, "rb") as f:
                data = f.read()
            b64 = base64.b64encode(data).decode()
            mime = "jpeg" if logo_ext in ("jpg","jpeg") else "png"
            cards_html += f'<img src="data:image/{mime};base64,{b64}" class="team-logo" alt="{value} logo">'
        cards_html += f'<div class="stat-value">{value}</div>'
        cards_html += '<div class="stat-label">Team</div>'

    else:
        cards_html += f'<div class="stat-value">{value}</div>'
        cards_html += f'<div class="stat-label">{label}</div>'

    cards_html += '</div>'
cards_html += '</div>'

st.markdown(cards_html, unsafe_allow_html=True)

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Arc, PathPatch
from matplotlib.path import Path
from matplotlib.collections import PatchCollection
from matplotlib.colors import ListedColormap, BoundaryNorm
from scipy.stats import percentileofscore

# ---------------------------
# Load and prepare dataset
# ---------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("NBA_Shot_Locations_SMALL.csv")
    df = df.dropna(subset=["Player Name", "X Location", "Y Location"])
    df["Game Date"] = pd.to_datetime(df["Game Date"], format="%Y%m%d")
    df["Season"] = df["Game Date"].apply(
        lambda x: f"{x.year}-{str(x.year + 1)[-2:]}" if x.month < 8 else f"{x.year}-{str(x.year + 1)[-2:]}"
    )
    return df

df = load_data()

# --- CSS Injection for Black Text ---
st.markdown("""
<style>
    .stRadio [data-baseweb="radio"] > div {
        color: black !important;
    }
    .stRadio [data-baseweb="radio"] > div > div {
        color: black !important;
    }
    .stCheckbox > label > div[data-testid="stMarkdownContainer"] > p {
        color: black !important;
    }
    .stCheckbox > label {
        color: black !important;
    }
    .stCheckbox div[data-testid="stMarkdownContainer"] {
        color: black !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------
# UI: Filters
# ---------------------------

st.title("NBA Shot Map and Hexmap")

# --- Importa il font Orbitron da Google Fonts ---
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Orbitron&display=swap" rel="stylesheet">
<style>
.orbitron-title {
    font-family: 'Orbitron', sans-serif;
    color: black;
    text-align: center;
    font-size: 20px;
    margin-top: 1em;
    margin-bottom: 0.5em;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<span style='color:black; margin-bottom: 0.1em;'><strong>Select Player</strong></span>", unsafe_allow_html=True)
players = sorted(df["Player Name"].unique())
selected_player = st.selectbox("Player", players, label_visibility="collapsed")

seasons = sorted(df["Season"].unique())
all_seasons_checked = st.checkbox("Show All Seasons", value=True)

if all_seasons_checked:
    selected_seasons = seasons
else:
    st.markdown("<span style='color:black; margin-bottom: 0.1em;'><strong>Select Seasons</strong></span>", unsafe_allow_html=True)
    selected_seasons = st.multiselect("Seasons", seasons, default=[seasons[0]], label_visibility="collapsed")

st.markdown("<span style='color:black; margin-bottom: 0.1em;'><strong>Shot Type</strong></span>", unsafe_allow_html=True)
shot_type_options_plain = ["All", "Made", "Missed"]
selected_shot_type = st.radio("Shot Type", shot_type_options_plain, label_visibility="collapsed", horizontal=True, key="shot_type_radio")
shot_type = selected_shot_type

st.markdown("<span style='color:black; margin-bottom: 0.1em;'><strong>Court Area</strong></span>", unsafe_allow_html=True)
zones = sorted(df["Shot Zone Basic"].dropna().unique())
selected_zones = st.multiselect("Court Area", zones, default=zones, label_visibility="collapsed")

# ---------------------------
# Filtered shot chart
# ---------------------------
filtered_df = df[
    (df["Player Name"] == selected_player) &
    (df["Season"].isin(selected_seasons)) &
    (df["Shot Zone Basic"].isin(selected_zones))
]

if shot_type == "Made":
    filtered_df = filtered_df[filtered_df["Shot Made Flag"] == 1]
elif shot_type == "Missed":
    filtered_df = filtered_df[filtered_df["Shot Made Flag"] == 0]

if filtered_df.empty:
    st.warning("No data found for this selection.")
    st.stop()

# ---------------------------
# Court drawing
# ---------------------------
def draw_court(ax=None, color="black", lw=2, outer_lines=False, court_fill_color="#f7f7f7"):
    if ax is None:
        ax = plt.gca()
    court_background = Rectangle((-250, -47.5), 500, 470, facecolor=court_fill_color, edgecolor='none', zorder=0)
    ax.add_patch(court_background)

    court_elements = [
        Circle((0, 0), radius=7.5, linewidth=lw, color=color, fill=False),
        Rectangle((-30, -12.5), 60, 0, linewidth=lw, color=color),
        Rectangle((-80, -47.5), 160, 190, linewidth=lw, color=color, fill=False),
        Rectangle((-60, -47.5), 120, 190, linewidth=lw, color=color, fill=False),
        Arc((0, 142.5), 120, 120, theta1=0, theta2=180, linewidth=lw, color=color),
        Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=lw, color=color),
        Rectangle((-220, -47.5), 0, 140, linewidth=lw, color=color),
        Rectangle((220, -47.5), 0, 140, linewidth=lw, color=color),
        Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=lw, color=color)
    ]
    if outer_lines:
        court_elements.append(Rectangle((-250, -47.5), 500, 470, linewidth=lw, color=color, fill=False))

    for elem in court_elements:
        ax.add_patch(elem)

    ax.set_xlim(-250, 250)
    ax.set_ylim(-47.5, 422.5)
    ax.set_aspect('equal')
    ax.axis('off')

# ---------------------------
# Shot Chart Plot
# ---------------------------
st.markdown(f"<div class='orbitron-title'>Shot Chart: {selected_player}</div>", unsafe_allow_html=True)
fig, ax = plt.subplots(figsize=(3, 3))
fig.set_facecolor("#f7f7f7")
draw_court(ax, color="black", court_fill_color="#f7f7f7")

made = filtered_df[filtered_df["Shot Made Flag"] == 1]
missed = filtered_df[filtered_df["Shot Made Flag"] == 0]

ax.scatter(missed["X Location"], missed["Y Location"], c='red', marker="x", s=10, label="Missed", zorder=2)
ax.scatter(made["X Location"], made["Y Location"], edgecolors='green', facecolors='none', marker='o', s=10, label="Made", zorder=2)
ax.legend(loc="upper right")

with st.container():
    st.markdown("<div style='width: 250px; margin: auto;'>", unsafe_allow_html=True)
    st.pyplot(fig)
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------
# Hexmap helper
# ---------------------------
def sized_hexbin(ax, hc, hc2, cmap, norm):
    offsets = hc.get_offsets()
    orgpath = hc.get_paths()[0]
    verts = orgpath.vertices
    values1 = hc.get_array()
    values2 = hc2.get_array()
    patches = []

    filtered_list = list(filter(lambda num: num != 0, values1))
    for offset, val in zip(offsets, values1):
        if int(val) == 0:
            continue
        perc = percentileofscore(filtered_list, val)
        scale = 0.3 if perc < 33.33 else 1.0 if perc > 66.66 else 0.6
        v1 = verts * scale + offset
        path = Path(v1, orgpath.codes)
        patch = PathPatch(path)
        patches.append(patch)

    pc = PatchCollection(patches, cmap=cmap, norm=norm)
    pc.set_array(values2)
    ax.add_collection(pc)
    hc.remove()
    hc2.remove()

# ---------------------------
# Hexmap Plot
# ---------------------------
st.markdown(f"<div class='orbitron-title'>Hexmap FG% vs League Avg — {selected_player} (all seasons)</div>", unsafe_allow_html=True)

st.markdown("""
<span style='color:black'><strong>Color Legend (FG% vs League Avg)</strong></span><br>
<span style='color:black'>🔵 Dark Blue: Much lower than league average</span><br>
<span style='color:black'>🔹 Light Blue: Slightly below average</span><br>
<span style='color:black'>🟡 Yellow: Around league average</span><br>
<span style='color:black'>🟠 Orange: Slightly above average</span><br>
<span style='color:black'>🔴 Red: Much higher than league average</span>
""", unsafe_allow_html=True)

player_all = df[df["Player Name"] == selected_player]
league_avg = df.copy()

LA = league_avg.groupby(["Shot Zone Area", "Shot Zone Range"]).agg(FGA=("Shot Made Flag", "count"), FGM=("Shot Made Flag", "sum"))
LA["FGP"] = LA["FGM"] / LA["FGA"]

player = player_all.groupby(["Shot Zone Area", "Shot Zone Range", "Shot Made Flag"]).size().unstack(fill_value=0)
player["FGA"] = player.sum(axis=1)
player["FGM"] = player.get(1, 0)
player["FGP"] = player["FGM"] / player["FGA"]

player_vs_league = (player["FGP"] - LA["FGP"]) * 100
merged = pd.merge(player_all, player_vs_league.rename("FGP_diff"), on=["Shot Zone Area", "Shot Zone Range"], how="left")

valid_hex = merged.dropna(subset=["X Location", "Y Location", "FGP_diff"])
x = valid_hex["X Location"]
y = valid_hex["Y Location"]
fgp = valid_hex["FGP_diff"]

if not valid_hex.empty and np.isfinite(fgp).all():
    fig3, ax3 = plt.subplots(figsize=(3, 3))
    fig3.set_facecolor("#f7f7f7")
    draw_court(ax3, color="black", court_fill_color="#f7f7f7")

    cmap = ListedColormap(['#2b7cb6', '#abd9e9', '#ffffbf', '#fdaf61', '#f46d43', '#d73027', '#a50026'])
    boundaries = [-np.inf, -9, -3, 0, 3, 9, 15, np.inf]
    norm = BoundaryNorm(boundaries, cmap.N)

    hb1 = ax3.hexbin(x, y, gridsize=40, cmap=cmap, norm=norm, extent=[-275, 275, -50, 425], zorder=2)
    hb2 = ax3.hexbin(x, y, C=fgp, gridsize=40, cmap=cmap, norm=norm, extent=[-275, 275, -50, 425], zorder=2)
    sized_hexbin(ax3, hb1, hb2, cmap, norm)

  

    with st.container():
        st.markdown("<div style='width: 250px; margin: auto;'>", unsafe_allow_html=True)
        st.pyplot(fig3)
        st.markdown("</div>", unsafe_allow_html=True)
else:
    st.warning("Not enough valid data to render hexmap.")
