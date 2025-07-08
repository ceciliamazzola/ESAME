import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from PIL import Image
import base64
from io import BytesIO
import os

# Percorsi portabili
current_dir = Path(__file__).parent
df_path = current_dir.parent / "draft_history_fin.csv"
logo_folder = current_dir.parent / "logos"
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

    st.subheader(f"<h3 style='color: black;'>Draft {year} - Round {round_selected}</h3>", unsafe_allow_html=True)


    def find_logo(abbrev):
        for ext in [".png", ".jpg", ".jpeg", ".svg"]:
            path = logo_folder / f"{abbrev}{ext}"
            if path.exists():
                return path
        return None

    for _, r in filtered.iterrows():
        col1, col2, col3 = st.columns([1, 4, 2])

        col1.markdown(f"<div style='text-align:center; font-size:24px; font-weight:bold; color:#333;'>{r['Overall Pick']}</div>", unsafe_allow_html=True)

        col2.markdown(f"""
            <div style="padding: 4px 8px;">
                <div style="font-size:18px; font-weight:bold; color: #222;">{r['Player']}</div>
                <div style="font-size:14px; color: #555;">{int(r['Round Number'])}° Round, Pick {int(r['Round Pick'])}</div>
            </div>
        """, unsafe_allow_html=True)

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

fig = px.bar(
    top_affiliations,
    x='Players',
    y='Affiliation',
    orientation='h',
    text='Players',
    color='Players',
    color_continuous_scale='Blues',
    # Set the category order for the y-axis based on the sorted DataFrame
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
