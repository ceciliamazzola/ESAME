import streamlit as st

st.set_page_config(
    page_title="Glossary",
    layout="wide"
)

# 🌐 Tema chiaro e font Orbitron
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@600&display=swap" rel="stylesheet">
    <style>
        /* Sfondo generale */
        .stApp {
            background-color: #2f6974 !important;
        }

        /* Campo input */
        input {
            color: #ffffff !important;
            background-color: #2f6974!important;
            border: 1px solid #ffffff !important;
        }

        label, .stTextInput label {
            color: #ffffff !important;
            font-weight: 600 !important;
        }

        /* Titolo expander (abbreviazioni) */
        .streamlit-expanderHeader {
            color: #ffffff !important;
            font-weight: 700 !important;
            background-color: #2f6974 !important;
        }

        .streamlit-expanderHeader > div {
            color: #ffffff !important;
        }

        .streamlit-expanderHeader:hover,
        .streamlit-expanderHeader:focus,
        .streamlit-expanderHeader:active {
            color: #ffffff !important;
        }

        /* Casella expander */
        .st-expander {
            background-color: #2f6974 !important;
            border: 1px solid #ffffff !important;
            border-radius: 6px !important;
            color: #ffffff !important;
        }

        /* Testo dentro l’expander */
        .stMarkdown, .stMarkdown p {
            color: #ffffff !important;
        }

        

        /* Linea orizzontale */
        .css-1d391kg hr {
            border-color: #999 !important;
        }
    </style>
""", unsafe_allow_html=True)


# Titolo
st.markdown("""
    <div style='font-family: Orbitron, sans-serif; font-size: 2.5rem; font-weight: 700; color: #f45208; text-align: center; margin-bottom: 0.5rem;'>
        GLOSSARY
    </div>
""", unsafe_allow_html=True)

# Sottotitolo
st.markdown("""
    <div style='font-family: Orbitron, sans-serif; font-size: 1.1rem; color: #white; text-align: center; margin-bottom: 1.5rem;'>
        Search and explore key NBA stats and abbreviations with quick definitions
    </div>
""", unsafe_allow_html=True)

# Bottone indietro
# Bottone indietro
st.markdown("""
    <form action="/" method="get">
        <button type="submit" style="
            padding: 10px 20px;
            background-color: #2f6974;
            color: white;
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

glossary = {
        "2P": "2-Point Field Goals",
        "2P%": "2-Point Field Goal Percentage, calculated as 2P / 2PA.",
        "2PA": "2-Point Field Goal Attempts",
        "3P": "3-Point Field Goals (available since the 1979-80 NBA season)",
        "3P%": "3-Point Field Goal Percentage, calculated as 3P / 3PA (available since the 1979-80 NBA season).",
        "3PA": "3-Point Field Goal Attempts (available since the 1979-80 NBA season)",
        "Age": "Player's age on February 1 of the given season.",
        "AST": "Assists",
        "AST%": "Assist Percentage, an estimate of the percentage of teammate field goals a player assisted while on the floor (available since the 1964-65 NBA season).",
        "Award Share": "Calculated as (award points) / (maximum number of award points).",
        "BLK": "Blocks (available since the 1973-74 NBA season)",
        "BLK%": "Block Percentage, an estimate of the percentage of opponent two-point field goal attempts blocked by the player while on the floor (available since the 1973-74 NBA season).",
        "BPM": "Box Plus/Minus, a box score estimate of points contributed above a league-average player per 100 possessions (available since the 1973-74 NBA season).",
        "DPOY": "Defensive Player of the Year",
        "DRB": "Defensive Rebounds (available since the 1973-74 NBA season)",
        "DRB%": "Defensive Rebound Percentage, an estimate of the percentage of available defensive rebounds a player grabbed while on the floor (available since the 1970-71 NBA season).",
        "DRtg": "Defensive Rating, points allowed per 100 possessions for players and teams (available since the 1973-74 NBA season).",
        "DWS": "Defensive Win Shares.",
        "eFG%": "Effective Field Goal Percentage, which adjusts for the fact that a 3-point field goal is worth more than a 2-point field goal.",
        "FG": "Field Goals (includes both 2-point and 3-point field goals)",
        "FG%": "Field Goal Percentage, calculated as FG / FGA.",
        "FGA": "Field Goal Attempts (includes both 2-point and 3-point field goal attempts)",
        "FT": "Free Throws",
        "FT%": "Free Throw Percentage, calculated as FT / FTA.",
        "FTA": "Free Throw Attempts",
        "Four Factors": "Dean Oliver's \"Four Factors of Basketball Success.\"",
        "G": "Games",
        "GB": "Games Behind.",
        "GmSc": "Game Score, a measure of a player's productivity for a single game.",
        "GS": "Games Started (available since the 1982 season)",
        "L": "Losses",
        "L Pyth": "Pythagorean Losses.",
        "Lg": "League",
        "MVP": "Most Valuable Player",
        "MP": "Minutes Played (available since the 1951-52 season)",
        "MOV": "Margin of Victory, calculated as PTS - Opp PTS.",
        "ORtg": "Offensive Rating, points produced per 100 possessions for players and points scored per 100 possessions for teams (available since the 1977-78 NBA season).",
        "Opp": "Opponent",
        "ORB": "Offensive Rebounds (available since the 1973-74 NBA season)",
        "ORB%": "Offensive Rebound Percentage, an estimate of the percentage of available offensive rebounds a player grabbed while on the floor (available since the 1970-71 NBA season).",
        "OWS": "Offensive Win Shares.",
        "Pace": "Pace Factor, an estimate of the number of possessions per 48 minutes by a team (available since the 1973-74 NBA season).",
        "PER": "Player Efficiency Rating, a per-minute rating of a player's performance (available since the 1951-52 season).",
        "Per 36 Minutes": "A statistic divided by minutes played, multiplied by 36.",
        "Per Game": "A statistic divided by games.",
        "PF": "Personal Fouls",
        "Poss": "Possessions (available since the 1973-74 NBA season).",
        "PProd": "Points Produced, Dean Oliver's measure of offensive points produced.",
        "PTS": "Points",
        "ROY": "Rookie of the Year",
        "SMOY": "Sixth Man of the Year",
        "SOS": "Strength of Schedule, a rating denominated in points above/below average.",
        "SRS": "Simple Rating System, a rating that considers average point differential and strength of schedule.",
        "STL": "Steals (available since the 1973-74 NBA season)",
        "STL%": "Steal Percentage, an estimate of the percentage of opponent possessions that end with a steal by the player while on the floor (available since the 1973-74 NBA season).",
        "Stops": "Dean Oliver's measure of individual defensive stops.",
        "Tm": "Team",
        "TOV": "Turnovers (available since the 1977-78 NBA season)",
        "TOV%": "Turnover Percentage, an estimate of turnovers per 100 plays (available since the 1977-78 NBA season).",
        "TRB": "Total Rebounds (available since the 1950-51 season)",
        "TRB%": "Total Rebound Percentage, an estimate of the percentage of available rebounds a player grabbed while on the floor (available since the 1970-71 NBA season).",
        "TS%": "True Shooting Percentage, a measure of shooting efficiency.",
        "TSA": "True Shooting Attempts.",
        "Usg%": "Usage Percentage, an estimate of the percentage of team plays used by a player while on the floor (available since the 1977-78 NBA season).",
        "VORP": "Value Over Replacement Player, a box score estimate of points contributed above a replacement-level player (available since the 1973-74 NBA season).",
        "W": "Wins",
        "W Pyth": "Pythagorean Wins.",
        "W-L%": "Won-Lost Percentage, calculated as W / (W + L).",
        "WS": "Win Shares, an estimate of the number of wins contributed by a player.",
        "WS/48": "Win Shares Per 48 Minutes, an estimate of wins contributed by the player per 48 minutes (available since the 1951-52 NBA season).",
        "Win Probability": "The estimated probability that Team A will defeat Team B in a given matchup.",
        "Year": "The last calendar year for a given NBA season (e.g., 2000 for the 1999-00 season)."
}

# Ordina i termini alfabeticamente
sorted_terms = sorted(glossary.keys())

# Barra di ricerca
query = st.text_input("Search for a term (e.g., FG%, PER, AST)").strip().lower()

# Filtra i termini in base alla query
filtered_terms = [term for term in sorted_terms if query in term.lower() or query in glossary[term].lower()]

# Mostra i risultati filtrati
if filtered_terms:
    for term in filtered_terms:
        definition = glossary[term]
        with st.expander(f"**{term}**"):
            st.write(definition)
else:
    if query:
        st.warning("No matching terms found.")
    else:
        for term in sorted_terms:
            definition = glossary[term]
            with st.expander(f"**{term}**"):
                st.write(definition)