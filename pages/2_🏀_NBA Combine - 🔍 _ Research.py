import streamlit as st
import pandas as pd

# Load unified dataset (corretto con separatore e engine)
df = pd.read_csv("combine_with_draft_info_fixed.csv", sep=';', engine='python')

# Debug temporaneo: mostra le colonne disponibili
# st.write(df.columns.tolist())  # Puoi decommentare per controllo

# Page configuration
st.set_page_config(page_title="Research - Next Gen Draft")

# Style aggiornato
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@600&display=swap" rel="stylesheet">
<style>
    html, body, .stApp {
        background-color: #f7f7f7 !important;
        color: #333 !important;
    }
    .title-custom {
        font-family: 'Orbitron', sans-serif;
        font-size: 2.5rem;
        font-weight: 700;
        color: #f45208;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .subtitle-custom {
        font-family: 'Orbitron', sans-serif;
        font-size: 1.1rem;
        color: #333;
        text-align: center;
        margin-bottom: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Titolo + sottotitolo
st.markdown("<div class='title-custom'>RESEARCH</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle-custom'>Advanced search to identify draft prospects matching ideal profile</div>", unsafe_allow_html=True)

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

# Prepara liste per i filtri
if 'POS' in df.columns:
    positions = df['POS'].dropna().unique().tolist()
    colleges = df['College'].dropna().unique().tolist()
    years = sorted(df['YEAR'].dropna().unique().tolist())

    # Sidebar filters
    with st.sidebar:
        st.title("Filter Players")

        # Valori iniziali predefiniti
        initial_values = {
            "selected_years": years,
            "selected_pos": [],
            "selected_college": [],
            "height_range": (int(df['HGT'].min()), int(df['HGT'].max())),
            "bmi_range": (float(df['BMI'].min()), float(df['BMI'].max())),
            "wingspan_range": (float(df['WNGSPN'].min()), float(df['WNGSPN'].max())),
            "stndrch_range": (float(df['STNDRCH'].min()), float(df['STNDRCH'].max())),
            "vert_range": (float(df['LPVERT'].min()), float(df['LPVERT'].max())),
            "sprint_range": (float(df['SPRINT'].min()), float(df['SPRINT'].max())),
            "first_pick_only": False
        }

        if st.button("Clear Filters"):
            for key, value in initial_values.items():
                st.session_state[key] = value
            st.rerun()

        selected_years = st.multiselect("Draft Year", years, default=years, key="selected_years")
        selected_pos = st.multiselect("Position", positions, key="selected_pos")
        selected_college = st.multiselect("College", colleges, key="selected_college")

        height_range = st.slider("Height (inches)", int(df['HGT'].min()), int(df['HGT'].max()),
                                 (int(df['HGT'].min()), int(df['HGT'].max())), key="height_range")
        bmi_range = st.slider("BMI", float(df['BMI'].min()), float(df['BMI'].max()),
                              (float(df['BMI'].min()), float(df['BMI'].max())), key="bmi_range")
        wingspan_range = st.slider("Wingspan (inches)", float(df['WNGSPN'].min()), float(df['WNGSPN'].max()),
                                   (float(df['WNGSPN'].min()), float(df['WNGSPN'].max())), key="wingspan_range")
        stndrch_range = st.slider("Standing Reach (inches)", float(df['STNDRCH'].min()), float(df['STNDRCH'].max()),
                                  (float(df['STNDRCH'].min()), float(df['STNDRCH'].max())), key="stndrch_range")
        vert_range = st.slider("Max Vertical Jump (inches)", float(df['LPVERT'].min()), float(df['LPVERT'].max()),
                               (float(df['LPVERT'].min()), float(df['LPVERT'].max())), key="vert_range")
        sprint_range = st.slider("Sprint Time (seconds)", float(df['SPRINT'].min()), float(df['SPRINT'].max()),
                                 (float(df['SPRINT'].min()), float(df['SPRINT'].max())), key="sprint_range")
        first_pick_only = st.checkbox("1st Pick Only", key="first_pick_only")

    # Applica i filtri
    filtered = df.copy()
    filtered = filtered[filtered['YEAR'].isin(st.session_state.selected_years)]
    if st.session_state.selected_pos:
        filtered = filtered[filtered['POS'].isin(st.session_state.selected_pos)]
    if st.session_state.selected_college:
        filtered = filtered[filtered['College'].isin(st.session_state.selected_college)]
    filtered = filtered[(filtered['HGT'] >= st.session_state.height_range[0]) & (filtered['HGT'] <= st.session_state.height_range[1])]
    filtered = filtered[(filtered['BMI'] >= st.session_state.bmi_range[0]) & (filtered['BMI'] <= st.session_state.bmi_range[1])]
    filtered = filtered[(filtered['WNGSPN'] >= st.session_state.wingspan_range[0]) & (filtered['WNGSPN'] <= st.session_state.wingspan_range[1])]
    filtered = filtered[(filtered['STNDRCH'] >= st.session_state.stndrch_range[0]) & (filtered['STNDRCH'] <= st.session_state.stndrch_range[1])]
    filtered = filtered[(filtered['LPVERT'] >= st.session_state.vert_range[0]) & (filtered['LPVERT'] <= st.session_state.vert_range[1])]
    filtered = filtered[(filtered['SPRINT'] >= st.session_state.sprint_range[0]) & (filtered['SPRINT'] <= st.session_state.sprint_range[1])]
    if st.session_state.first_pick_only:
        filtered = filtered[filtered['Pk'] == 1]


        if st.button("Clear Filters"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

        selected_years = st.multiselect("Draft Year", years, default=years, key="selected_years")
        selected_pos = st.multiselect("Position", positions, key="selected_pos")
        selected_college = st.multiselect("College", colleges, key="selected_college")

        height_range = st.slider("Height (inches)", int(df['HGT'].min()), int(df['HGT'].max()),
                                 (int(df['HGT'].min()), int(df['HGT'].max())), key="height_range")
        bmi_range = st.slider("BMI", float(df['BMI'].min()), float(df['BMI'].max()),
                              (float(df['BMI'].min()), float(df['BMI'].max())), key="bmi_range")
        wingspan_range = st.slider("Wingspan (inches)", float(df['WNGSPN'].min()), float(df['WNGSPN'].max()),
                                   (float(df['WNGSPN'].min()), float(df['WNGSPN'].max())), key="wingspan_range")
        stndrch_range = st.slider("Standing Reach (inches)", float(df['STNDRCH'].min()), float(df['STNDRCH'].max()),
                                  (float(df['STNDRCH'].min()), float(df['STNDRCH'].max())), key="stndrch_range")
        vert_range = st.slider("Max Vertical Jump (inches)", float(df['LPVERT'].min()), float(df['LPVERT'].max()),
                               (float(df['LPVERT'].min()), float(df['LPVERT'].max())), key="vert_range")
        sprint_range = st.slider("Sprint Time (seconds)", float(df['SPRINT'].min()), float(df['SPRINT'].max()),
                                 (float(df['SPRINT'].min()), float(df['SPRINT'].max())), key="sprint_range")
        first_pick_only = st.checkbox("1st Pick Only", key="first_pick_only")

    # Applica i filtri
    filtered = df.copy()
    filtered = filtered[filtered['YEAR'].isin(st.session_state.selected_years)]
    if st.session_state.selected_pos:
        filtered = filtered[filtered['POS'].isin(st.session_state.selected_pos)]
    if st.session_state.selected_college:
        filtered = filtered[filtered['College'].isin(st.session_state.selected_college)]
    filtered = filtered[(filtered['HGT'] >= st.session_state.height_range[0]) & (filtered['HGT'] <= st.session_state.height_range[1])]
    filtered = filtered[(filtered['BMI'] >= st.session_state.bmi_range[0]) & (filtered['BMI'] <= st.session_state.bmi_range[1])]
    filtered = filtered[(filtered['WNGSPN'] >= st.session_state.wingspan_range[0]) & (filtered['WNGSPN'] <= st.session_state.wingspan_range[1])]
    filtered = filtered[(filtered['STNDRCH'] >= st.session_state.stndrch_range[0]) & (filtered['STNDRCH'] <= st.session_state.stndrch_range[1])]
    filtered = filtered[(filtered['LPVERT'] >= st.session_state.vert_range[0]) & (filtered['LPVERT'] <= st.session_state.vert_range[1])]
    filtered = filtered[(filtered['SPRINT'] >= st.session_state.sprint_range[0]) & (filtered['SPRINT'] <= st.session_state.sprint_range[1])]
    if st.session_state.first_pick_only:
        filtered = filtered[filtered['Pk'] == 1]

>>>>>>> 57037df (Research)
    # Mostra i risultati
    st.header("Filtered Players")
    if filtered.empty:
        st.markdown("""
            <p style='color: #000; font-size: 1.1rem; text-align: center; margin-top: 1rem;'>
                No players found with selected criteria.
            </p>
        """, unsafe_allow_html=True)
    else:
        for year in sorted(filtered['YEAR'].unique(), reverse=True):
            st.subheader(f"Draft Year: {year}")
            year_df = filtered[filtered['YEAR'] == year][[
                'PLAYER', 'POS', 'HGT', 'WGT', 'BMI', 'WNGSPN',
                'STNDRCH', 'LPVERT', 'SPRINT', 'College', 'Pk', 'Tm'
            ]]
            st.dataframe(year_df.reset_index(drop=True))
else:
    st.error("❌ Errore: la colonna 'POS' non esiste nel file. Verifica che il file CSV sia nel formato corretto e che usi il separatore ';'.")
