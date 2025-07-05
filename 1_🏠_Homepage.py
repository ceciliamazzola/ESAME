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
