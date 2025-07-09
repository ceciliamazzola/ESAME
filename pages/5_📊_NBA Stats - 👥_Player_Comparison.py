import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------
# Page Configuration
# ----------------------
st.set_page_config(
    page_title="NBA Player Shooting & Free Throw Dashboard",
    layout="wide"
)

# ----------------------
# Custom Style
# ----------------------
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@600&display=swap" rel="stylesheet">
    <style>
        .stApp { background-color: #f7f7f7; }
        h1 { font-family: 'Orbitron', sans-serif !important; color: #f45208 !important; font-size: 2.5rem !important; }
        label, .stSelectbox label { color: #000 !important; font-weight: bold; }
        .css-1d391kg hr { border-color: #ccc !important; }
    </style>
""", unsafe_allow_html=True)

# ----------------------
# Title
# ----------------------
st.markdown("""
    <div style='font-family: Orbitron, sans-serif; font-size: 2.5rem; font-weight: 700; color: #f45208; text-align: center; margin-bottom: 1rem;'>
        NBA PLAYER STATS
    </div>
""", unsafe_allow_html=True)

# ----------------------
# Subtitle
# ----------------------
st.markdown("""
    <div style='font-family: Orbitron, sans-serif; font-size: 1.1rem; color: #333; text-align: center; margin-bottom: 2rem;'>
        Explore up-to-date shooting and free throw statistics for NBA players
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
# ----------------------
# Load data
# ----------------------
@st.cache_data
def load_data(path: str):
    df = pd.read_csv(path)
    df = df[df['season'] >= 2000].copy()

    df_season_fg = (
        df.groupby(['player_x','season'], as_index=False)
          .apply(lambda x: pd.Series({'FG%': (x['fg_percent'] * x['g']).sum() / x['g'].sum() * 100}))
          .reset_index(drop=True)
    )

    df_season_split = (
        df.groupby(['player_x','season'], as_index=False)
          .apply(lambda x: pd.Series({
              '2P%': (x['x2p_percent'] * x['g']).sum() / x['g'].sum() * 100,
              '3P%': (x['x3p_percent'] * x['g']).sum() / x['g'].sum() * 100
          }))
          .reset_index(drop=True)
    )

    df_season_ft = (
        df.groupby(['player_x','season'], as_index=False)
          .apply(lambda x: pd.Series({'FT%': (x['ft_percent'] * x['g']).sum() / x['g'].sum() * 100}))
          .reset_index(drop=True)
    )

    career_list = []
    for player, grp in df.groupby('player_x'):
        total_games = grp['g'].sum()
        career_fg = (grp['fg_percent'] * grp['g']).sum() / total_games * 100
        career_list.append({'player_x': player, 'FG%': career_fg})
    career_fg_df = pd.DataFrame(career_list)

    career_cols = (
        df[['player_x', 'career_x2p_percent', 'career_x3p_percent', 'career_ft_percent']]
          .drop_duplicates(subset=['player_x'])
          .rename(columns={
              'career_x2p_percent': '2P%',
              'career_x3p_percent': '3P%',
              'career_ft_percent': 'FT%'
          })
    )

    career_df = career_fg_df.merge(career_cols, on='player_x')
    career_df.rename(columns={'player_x': 'player'}, inplace=True)

    for df_split in (df_season_fg, df_season_split, df_season_ft):
        df_split.rename(columns={'player_x': 'player'}, inplace=True)

    return df, career_df, df_season_fg, df_season_split, df_season_ft

raw_df, career_df, df_season_fg, df_season_split, df_season_ft = load_data('Player Final.csv')

# ----------------------
# Filters and Player Selection
# ----------------------
positions = sorted(raw_df['pos'].dropna().unique())
selected_positions = st.multiselect("Select positions:", positions, default=positions)
filtered = raw_df[raw_df['pos'].isin(selected_positions)]
st.write(f"**Players available:** {filtered['player_x'].nunique()}")

st.markdown(f"""
    <div style='color: black; font-weight: 600; font-size: 16px;'>
        Players available: {filtered['player_x'].nunique()}
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <div style='color: black; font-weight: 700; font-size: 24px; margin-top: 0.5rem; font-family: Orbitron, sans-serif;'>
        Select Players
    </div>
""", unsafe_allow_html=True)
players = sorted(filtered['player_x'].unique())
default_players = [p for p in ["LeBron James", "Stephen Curry", "Kevin Durant"] if p in players]
selected = st.multiselect(
    "Choose up to 7 players:",
    players,
    default=default_players,
    max_selections=7
)

# ----------------------
# Helper: Plotly style
# ----------------------
def update_layout(fig, title):
    fig.update_layout(
        title=dict(
            text=title,
            x=0,
            xanchor='left',
            font=dict(family="Orbitron, sans-serif", size=20, color="black")
        ),
        font=dict(color="black", family="sans-serif"),
        paper_bgcolor="#f7f7f7",
        plot_bgcolor="#f7f7f7",
        legend=dict(font=dict(color="black"), title_font=dict(color="black"))
    )
    fig.update_xaxes(
        title_font=dict(color="black"),
        tickfont=dict(color="black"),
        showline=True, linecolor="black", gridcolor="lightgrey"
    )
    fig.update_yaxes(
        title_font=dict(color="black"),
        tickfont=dict(color="black"),
        showline=True, linecolor="black", gridcolor="lightgrey"
    )
    return fig


# ----------------------
# Visualizations
# ----------------------
if selected:
    career_plot = career_df[career_df['player'].isin(selected)]
    season_fg_plot = df_season_fg[df_season_fg['player'].isin(selected)]
    season_split_plot = df_season_split[df_season_split['player'].isin(selected)]
    season_ft_plot = df_season_ft[df_season_ft['player'].isin(selected)]

    # Grafici in coppia
    def two_cols_plot(fig1, fig2):
        col1, col2 = st.columns(2)
        with col1: st.plotly_chart(fig1, use_container_width=True)
        with col2: st.plotly_chart(fig2, use_container_width=True)

    two_cols_plot(
        update_layout(px.bar(career_plot, x='player', y='FG%', color='player'), 'Career Overall FG% Comparison'),
        update_layout(px.line(season_fg_plot, x='season', y='FG%', color='player', markers=True), 'Seasonal Overall FG% Trend')
    )
    two_cols_plot(
        update_layout(px.bar(career_plot.melt(id_vars='player', value_vars=['2P%']), x='player', y='value', color='player'), 'Career 2P% Comparison'),
        update_layout(px.line(season_split_plot, x='season', y='2P%', color='player', markers=True), 'Seasonal 2P% Trend')
    )
    two_cols_plot(
        update_layout(px.bar(career_plot.melt(id_vars='player', value_vars=['3P%']), x='player', y='value', color='player'), 'Career 3P% Comparison'),
        update_layout(px.line(season_split_plot, x='season', y='3P%', color='player', markers=True), 'Seasonal 3P% Trend')
    )
    two_cols_plot(
        update_layout(px.bar(career_plot.melt(id_vars='player', value_vars=['FT%']), x='player', y='value', color='player'), 'Career FT% Comparison'),
        update_layout(px.line(season_ft_plot, x='season', y='FT%', color='player', markers=True), 'Seasonal FT% Trend')
    )

else:
    st.markdown("<p style='color:black;'>Select players to display visualizations.</p>", unsafe_allow_html=True)


import streamlit as st
import pandas as pd
import plotly.express as px

# ——————————————————————————————
# FONT Orbitron solo per titoli
# ——————————————————————————————
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@600&display=swap" rel="stylesheet">
    <style>
        .custom-title {
            font-family: 'Orbitron', sans-serif;
            color: #f45208;
            font-size: 1.8rem;
            margin-top: 1.5rem;
        }
        .stApp {
            background-color: #f7f7f7;
        }
    </style>
""", unsafe_allow_html=True)

# ——————————————————————————————
# 📊 EFFICIENCY EXPLANATION
# ——————————————————————————————
st.markdown("<div class='custom-title'>Efficiency Comparison</div>", unsafe_allow_html=True)
st.markdown("""
<div style='color: black; font-size: 1rem;'>
The <strong>EFF</strong> is a synthetic index to estimate a player's overall contribution to the team.<br><br>
<strong>Formula (per season):</strong><br>
EFF = (PTS + TRB + AST + STL + BLK − (FGA − FG) − (FTA − FT) − TOV) / G<br><br>
<ul>
  <li><strong>PTS</strong>: Points</li>
  <li><strong>TRB</strong>: Total Rebounds</li>
  <li><strong>AST</strong>: Assists</li>
  <li><strong>STL</strong>: Steals</li>
  <li><strong>BLK</strong>: Blocks</li>
  <li><strong>FGA − FG</strong>: Missed Field Goals</li>
  <li><strong>FTA − FT</strong>: Missed Free Throws</li>
  <li><strong>TOV</strong>: Turnovers</li>
  <li><strong>G</strong>: Games Played</li>
</ul>
</div>
""", unsafe_allow_html=True)

# ——————————————————————————————
# 📊 CALCOLO EFFICIENZA
# ——————————————————————————————
df_eff = raw_df.copy()
df_eff['miss_fg'] = df_eff['fga'] - df_eff['fg']
df_eff['miss_ft'] = df_eff['fta'] - df_eff['ft']

df_season_eff = (
    df_eff.groupby(['player_x','season'], as_index=False)
    .agg({
        'pts':'sum', 'trb':'sum', 'ast':'sum', 'stl':'sum', 'blk':'sum',
        'miss_fg':'sum', 'miss_ft':'sum', 'tov':'sum', 'g':'sum'
    })
)
df_season_eff['EFF'] = (
    df_season_eff['pts'] + df_season_eff['trb'] + df_season_eff['ast'] +
    df_season_eff['stl'] + df_season_eff['blk'] -
    df_season_eff['miss_fg'] - df_season_eff['miss_ft'] - df_season_eff['tov']
) / df_season_eff['g']
df_season_eff.rename(columns={'player_x': 'player'}, inplace=True)

season_eff_plot = df_season_eff[df_season_eff['player'].isin(selected)]

fig_season_eff = px.line(
    season_eff_plot,
    x='season', y='EFF', color='player', markers=True,
    labels={'EFF':'Efficiency', 'season':'Season', 'player':'Player'}
)
fig_season_eff.update_yaxes(tickformat='.1f')
fig_season_eff.update_layout(
    title=dict(text="Seasonal Player Efficiency (EFF)", x=0,
            xanchor='left',
               font=dict(family="Orbitron, sans-serif", size=20, color="black")),
    font=dict(color="black"),
    paper_bgcolor="#f7f7f7",
    plot_bgcolor="#f7f7f7",
    xaxis=dict(
        title_font=dict(color="black"),
        tickfont=dict(color="black"),
        showline=True,
        linecolor="black",
        gridcolor="lightgray"
    ),
    yaxis=dict(
        title_font=dict(color="black"),
        tickfont=dict(color="black"),
        showline=True,
        linecolor="black",
        gridcolor="lightgray"
    ),
    legend=dict(font=dict(color="black"))
)
st.plotly_chart(fig_season_eff, use_container_width=True)

# ——————————————————————————————
# 📈 OER EXPLANATION
# ——————————————————————————————
st.markdown("<div class='custom-title'>Seasonal Offensive Efficiency Rating (OER) Comparison</div>", unsafe_allow_html=True)
st.markdown("""
<div style='color: black; font-size: 1rem;'>
<strong>OER</strong> estimates how many points a player produces per 100 possessions.<br><br>
<strong>Formula:</strong><br>
OER = (PTS / Possessions) × 100<br><br>
<strong>Where:</strong><br>
Possessions = FGA + 0.44 × FTA + TOV − ORB<br><br>
<ul>
  <li><strong>FGA</strong>: Field Goal Attempts</li>
  <li><strong>FTA</strong>: Free Throw Attempts</li>
  <li><strong>TOV</strong>: Turnovers</li>
  <li><strong>ORB</strong>: Offensive Rebounds</li>
  <li><strong>PTS</strong>: Points</li>
</ul>
</div>
""", unsafe_allow_html=True)

# ——————————————————————————————
# 📈 CALCOLO OER
# ——————————————————————————————
df_oer = (
    raw_df.groupby(['player_x', 'season'], as_index=False)
    .agg({'pts': 'sum', 'fga': 'sum', 'fta': 'sum', 'tov': 'sum', 'orb': 'sum'})
)
df_oer['Possessions'] = df_oer['fga'] + 0.44 * df_oer['fta'] + df_oer['tov'] - df_oer['orb']
df_oer['OER'] = df_oer['pts'] / df_oer['Possessions'] * 100
df_oer.rename(columns={'player_x': 'player'}, inplace=True)

season_oer_plot = df_oer[df_oer['player'].isin(selected)]

fig_oer = px.line(
    season_oer_plot,
    x='season', y='OER', color='player', markers=True,
    labels={'OER': 'OER', 'season': 'Season', 'player': 'Player'}
)
fig_oer.update_yaxes(tickformat='.1f')
fig_oer.update_layout(
    title=dict(text="Seasonal Offensive Efficiency Rating (OER)", x=0,
            xanchor='left',
               font=dict(family="Orbitron, sans-serif", size=20, color="black")),
    font=dict(color="black"),
    paper_bgcolor="#f7f7f7",
    plot_bgcolor="#f7f7f7",
    xaxis=dict(
        title_font=dict(color="black"),
        tickfont=dict(color="black"),
        showline=True,
        linecolor="black",
        gridcolor="lightgray"
    ),
    yaxis=dict(
        title_font=dict(color="black"),
        tickfont=dict(color="black"),
        showline=True,
        linecolor="black",
        gridcolor="lightgray"
    ),
    legend=dict(font=dict(color="black"))
)
st.plotly_chart(fig_oer, use_container_width=True)
