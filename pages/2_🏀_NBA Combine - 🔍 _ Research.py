import streamlit as st
import pandas as pd

# Caricamento dataset
df = pd.read_csv("combine_with_draft_info_fixed.csv", sep=';', engine='python')

# Configurazione pagina
st.set_page_config(page_title="Research - Next Gen Draft")

# Stile CSS personalizzato
st.markdown(
    """
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
    """, unsafe_allow_html=True
)

# Titoli
st.markdown("<div class='title-custom'>RESEARCH</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='subtitle-custom'>Advanced search to identify draft prospects matching ideal profile</div>",
    unsafe_allow_html=True
)

# Bottone "Back to menu"
st.markdown(
    """
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
    """, unsafe_allow_html=True
)
st.markdown("<br>", unsafe_allow_html=True)

# Verifica colonne prima di procedere
if 'POS' not in df.columns:
    st.error("❌ Errore: la colonna 'POS' non esiste nel file. Verifica il formato e il separatore del CSV.")
else:
    # Valori disponibili
    years = sorted(df['YEAR'].dropna().unique().tolist())
    positions = df['POS'].dropna().unique().tolist()
    colleges = df['College'].dropna().unique().tolist()

    # Form per l'applicazione dei filtri
    with st.form(key='filter_form'):
        st.header("Filter Players")
        st.caption("Imposta qui i parametri di ricerca e poi clicca 'Apply Filters'.")

        col1, col2 = st.columns(2)
        with col1:
            selected_years = st.multiselect(
                "Draft Year", years, default=years)
            selected_pos = st.multiselect(
                "Position", positions, default=None)
            selected_college = st.multiselect(
                "College", colleges, default=None)
        with col2:
            height_range = st.slider(
                "Height (inches)",
                int(df['HGT'].min()), int(df['HGT'].max()),
                value=(int(df['HGT'].min()), int(df['HGT'].max())))
            bmi_range = st.slider(
                "BMI",
                float(df['BMI'].min()), float(df['BMI'].max()),
                value=(float(df['BMI'].min()), float(df['BMI'].max())))
            wingspan_range = st.slider(
                "Wingspan (inches)",
                float(df['WNGSPN'].min()), float(df['WNGSPN'].max()),
                value=(float(df['WNGSPN'].min()), float(df['WNGSPN'].max())))
            stndrch_range = st.slider(
                "Standing Reach (inches)",
                float(df['STNDRCH'].min()), float(df['STNDRCH'].max()),
                value=(float(df['STNDRCH'].min()), float(df['STNDRCH'].max())))
            vert_range = st.slider(
                "Max Vertical Jump (inches)",
                float(df['LPVERT'].min()), float(df['LPVERT'].max()),
                value=(float(df['LPVERT'].min()), float(df['LPVERT'].max())))
            sprint_range = st.slider(
                "Sprint Time (seconds)",
                float(df['SPRINT'].min()), float(df['SPRINT'].max()),
                value=(float(df['SPRINT'].min()), float(df['SPRINT'].max())))
            first_pick_only = st.checkbox("1st Pick Only")

        # Bottone di submit
        submitted = st.form_submit_button("Apply Filters")

    # Dopo il submit, applica i filtri
    if submitted:
        filtered = df[
            (df['YEAR'].isin(selected_years)) &
            (df['HGT'].between(*height_range)) &
            (df['BMI'].between(*bmi_range)) &
            (df['WNGSPN'].between(*wingspan_range)) &
            (df['STNDRCH'].between(*stndrch_range)) &
            (df['LPVERT'].between(*vert_range)) &
            (df['SPRINT'].between(*sprint_range))
        ]
        if selected_pos:
            filtered = filtered[filtered['POS'].isin(selected_pos)]
        if selected_college:
            filtered = filtered[filtered['College'].isin(selected_college)]
        if first_pick_only:
            filtered = filtered[filtered['Pk'] == 1]

        st.header("Filtered Players")
        if filtered.empty:
            st.markdown(
                """
                <p style='color: #000; font-size: 1.1rem; text-align: center; margin-top: 1rem;'>
                    No players found with selected criteria.
                </p>
                """, unsafe_allow_html=True
            )
        else:
            for year in sorted(filtered['YEAR'].unique(), reverse=True):
                st.subheader(f"Draft Year: {year}")
                year_df = filtered[filtered['YEAR'] == year][[
                    'PLAYER', 'POS', 'HGT', 'WGT', 'BMI', 'WNGSPN',
                    'STNDRCH', 'LPVERT', 'SPRINT', 'College', 'Pk', 'Tm'
                ]]
                st.dataframe(year_df.reset_index(drop=True))
    else:
        st.info("⏳ Imposta i filtri e clicca 'Apply Filters' per vedere i risultati.")
