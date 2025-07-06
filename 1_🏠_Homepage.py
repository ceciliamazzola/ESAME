import streamlit as st
import base64
import os

def get_base64_image(image_path):
    with open(image_path, "rb") as img:
        return f"data:image/png;base64,{base64.b64encode(img.read()).decode()}"

# Carica immagine di sfondo
# Ottieni il percorso assoluto del file corrente
current_dir = os.path.dirname(__file__)
image_path = os.path.join(current_dir, "bandiere", "prova4.png")
image_base64 = get_base64_image(image_path)

# Configura la pagina
st.set_page_config(page_title="Home - DRAFT TO DINASTY", page_icon="")

# HTML layout
st.markdown("""
    <div class="left-block">
        <div class="title-left">
            DRAFT<br>TO DINASTY
        </div>
        <div class="subtitle-effect subtitle-left">
            Where talent meets destiny<br>
            and every pick could shape <br>
            the future of the game
        </div>
        <div class="menu-labels">
            <div class="menu-item">NBA Combine</div>
            <div class="menu-item">NBA Stats</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# CSS completo con Orbitron e scritte invece dei bottoni
st.markdown(f"""
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@800&display=swap" rel="stylesheet">
    <style>
        .stApp {{
            background-image: url('{image_base64}');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            overflow: hidden;
        }}
        .left-block {{
            position: fixed;
            top: 50px;
            left: 50%;
            transform: translateX(-77%); /* Sposta il blocco più verso il centro */
            width: 600px;
            height: 800px;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
            align-items: flex-start;
            z-index: 10;
        }}
        .title-left {{
            font-family: 'Orbitron', sans-serif;
            font-weight: 800;
            font-size: 80px;
            color: #f45208;
            -webkit-text-stroke: 3px white;
            text-shadow: 5px 5px 10px rgba(0,0,0,0.3);
            line-height: 1.1;
            margin-bottom: 40px;
            text-align: left;
        }}
        .subtitle-effect {{
            font-family: 'Orbitron', sans-serif;
            font-size: 24px;
            color: white;
            animation: fadeIn 2s ease-in-out;
            transition: transform 0.3s ease, color 0.3s ease, text-shadow 0.3s ease;
        }}
        .subtitle-effect:hover {{
            transform: scale(1.08);
            color: #f45208;
            text-shadow: 0 0 10px rgba(244,82,8,0.7);
        }}
        .subtitle-left {{
            text-align: left;
            line-height: 36px;
            max-width: 550px;
            margin-top: 60px;
            margin-left: 10px;
        }}
        .menu-labels {{
            margin-top: 80px;
            display: flex;
            gap: 30px;
            margin-left: 10px;
        }}
        .menu-item {{
            font-family: 'Orbitron', sans-serif;
            font-size: 20px;
            color: white;
            background-color: rgba(0, 0, 0, 0.4);
            padding: 10px 20px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.3);
        }}
        @keyframes fadeIn {{
            0% {{ opacity: 0; transform: translateY(10px); }}
            100% {{ opacity: 1; transform: translateY(0); }}
        }}
    </style>
""", unsafe_allow_html=True)









# ----------------------
# Data Loading
# ----------------------
@st.cache_data
def load_data(path: str):
    df = pd.read_csv(path)
    df = df[df['season'] >= 2000].copy()

    # Build career_df with shooting percentages and per-game stats
    df_pct = (
        df.drop_duplicates('player_x')
          .loc[:, ['player_x',
                    'career_x2p_percent','career_x3p_percent','career_ft_percent','career_e_fg_percent',
                    'career_pts_per_g','career_trb_per_g','career_ast_per_g','career_tov_per_g',
                    'career_orb','career_drb',
                    'career_g',
                    'career_fga','career_fg','career_fta','career_ft','career_tov',
                    'career_stl','career_blk'
                   ]]
          .rename(columns={
              'career_x2p_percent':'2P%',
              'career_x3p_percent':'3P%',
              'career_ft_percent':'FT%',
              'career_e_fg_percent':'eFG%',
              'career_pts_per_g':'PTS/G',
              'career_trb_per_g':'TRB/G',
              'career_ast_per_g':'AST/G',
              'career_tov_per_g':'TOV/G',
              'career_orb':'ORB_tot',
              'career_drb':'DRB_tot',
              'career_g':'Games',
          })
    )

    # Calculate efficiency (EFF) and offensive efficiency rating (OER)
    # EFF = (PTS + TRB + AST + STL + BLK - (FGA-FG) - (FTA-FT) - TOV) / Games
    df_pct['EFF'] = (
        df_pct['PTS/G'] * df_pct['Games'] + df_pct['TRB/G'] * df_pct['Games'] + df_pct['AST/G'] * df_pct['Games']
        + df_pct['career_stl'] + df_pct['career_blk']
        - (df_pct['career_fga'] - df_pct['career_fg'])
        - (df_pct['career_fta'] - df_pct['career_ft'])
        - df_pct['career_tov']
    ) / df_pct['Games']

    # OER = PTS / (FGA + 0.44*FTA + TOV - ORB) * 100
    denom = df_pct['career_fga'] + 0.44 * df_pct['career_fta'] + df_pct['career_tov'] - df_pct['ORB_tot']
    df_pct['OER'] = df_pct['PTS/G'] * df_pct['Games'] / denom * 100

    # Merge shooting percentages and per-game stats into one career_df
    career_df = df_pct.drop(columns=['career_stl','career_blk','career_fga','career_fg','career_fta','career_ft','career_tov','ORB_tot','DRB_tot'])
    career_df = career_df.rename(columns={'player_x':'player'})
    return career_df

@st.cache_data
def load_raw(path: str):
    return pd.read_csv(path)

career_df = load_data('Player Final.csv')
raw_df = load_raw('Player Final.csv')
logo_dir = Path(__file__).parent.parent / 'logos'

# ----------------------


# ----------------------
# Season Stats + Career EFF/OER
# ----------------------
st.markdown('---')
avail = raw_df[raw_df['player_x']==selected]['season'].dropna().astype(int).sort_values(ascending=False).unique()
sel_season = st.selectbox('Pick a season:', avail)
row = raw_df[(raw_df['player_x']==selected)&(raw_df['season']==sel_season)].iloc[0]
# Season metrics
display = {
    'Team': row['tm'], 'G': int(row['g']), 'MPG': round(row['mp']/row['g'],1),
    'PPG': round(row['pts']/row['g'],1), 'RPG': round(row['trb']/row['g'],1),
    'APG': round(row['ast']/row['g'],1), 'SPG': round(row['stl']/row['g'],1),
    'BPG': round(row['blk']/row['g'],1), 'TO/G': round(row['tov']/row['g'],1),
    'FG%': round(row['fg_percent']*100,1), '3P%': round(row['x3p_percent']*100,1), 'FT%': round(row['ft_percent']*100,1)
}
# Career metrics
pr = career_df[career_df['player']==selected].iloc[0]
display['Career EFF'] = round(pr['EFF'],1)
display['Career OER'] = round(pr['OER'],1)

cards = '<div class="stats-grid">'
for label, value in display.items():
    cards += '<div class="stat-card">'
    if label == 'Team':
        # team logo
        logo = None
        for ext in ('png','jpg','jpeg'):
            pth = logo_dir / f"{value}.{ext}"
            if pth.is_file(): logo = pth; break
        if logo:
            b = base64.b64encode(open(logo,'rb').read()).decode()
            mime = 'jpeg' if logo.suffix in ('.jpg','.jpeg') else 'png'
            cards += f'<img src="data:image/{mime};base64,{b}" class="team-logo">'
        cards += f'<div class="stat-value">{value}</div><div class="stat-label">Team</div>'
    else:
        cards += f'<div class="stat-value">{value}</div><div class="stat-label">{label}</div>'
    cards += '</div>'
cards += '</div>'
st.markdown(cards, unsafe_allow_html=True)