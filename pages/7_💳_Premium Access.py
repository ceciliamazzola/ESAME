import streamlit as st

# CONFIGURAZIONE DELLA PAGINA
st.set_page_config(page_title="Premium Access", page_icon="💳")

# CSS globale
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&display=swap" rel="stylesheet">
    <style>
        html, body, .stApp {
            background-color: #2f6974 !important;
        }
        h1, h2, h3, h4, h5, h6, p, li {
            color: white !important;
        }
        .plan-card {
            border: 2px solid #f45208;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            background-color: white;
            color: #333;
            margin: 10px;
        }
        .plan-card .features li {
            color: #000 !important;
        }
        .highlight {
            border: 4px solid #f45208;
        }
        .plan-title {
            font-size: 24px;
            font-weight: bold;
        }
        .price {
            font-size: 32px;
            color: #f45208;
            margin: 10px 0;
        }
        .features {
            font-size: 16px;
            margin-top: 10px;
            color: #000 !important;
        }
        .title-font {
            font-family: 'Orbitron', sans-serif;
            font-size: 46px;
            color: #f45208;
            font-weight: 700;
            text-align: center;
            margin-bottom: 30px;
            text-shadow: -1px -1px 0 #fff, 1px -1px 0 #fff, -1px 1px 0 #fff, 1px 1px 0 #fff;
        }

        /* Bottone personalizzato su st.button */
        button[kind="secondary"] {
            background-color: #f45208 !important;
            color: white !important;
            border: none !important;
            border-radius: 5px !important;
            font-family: 'Orbitron', sans-serif !important;
            font-weight: bold !important;
        }
        button[kind="secondary"]:hover {
            background-color: #ff7633 !important;
        }
    </style>
""", unsafe_allow_html=True)

# Inizializza il piano selezionato
if "selected_plan" not in st.session_state:
    st.session_state.selected_plan = None

# TITOLO
st.markdown("<div class='title-font'>Unlock Premium Analytics</div>", unsafe_allow_html=True)

# SOTTOTITOLO
st.markdown("""
<div style="text-align: center; font-size: 1.1rem; font-family: 'Orbitron', sans-serif;">
    Get exclusive access to advanced metrics, draft insights, and real-time analytics to have a competitive edge
</div>
""", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)  # Una riga vuota


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

# LISTA DEI PIANI
plans = [
    {
        "name": "Starter",
        "price": "$19/month",
        "desc": "Perfect for individual users",
        "features": ["Basic player statistics", "Weekly reports", "Email support", "Limited data exports"]
    },
    {
        "name": "Pro",
        "price": "$49/month",
        "desc": "Best for professional scouts and analysts",
        "features": ["Advanced analytics", "Player comparisons", "Real-time updates", "Priority support", "Unlimited exports", "Custom reports"],
        "popular": True
    },
    {
        "name": "Enterprise",
        "price": "$79/month",
        "desc": "Complete solution for organizations",
        "features": ["Full analytics suite", "Custom reports", "API access", "Dedicated support", "Team collaboration", "White-label options"]
    }
]

# RENDERING PIANI
cols = st.columns(3)
for idx, plan in enumerate(plans):
    with cols[idx]:
        extra_class = " highlight" if plan.get("popular") else ""
        st.markdown(f"""
            <div class='plan-card{extra_class}'>
                <div class='plan-title'>{plan['name']}</div>
                <div class='price'>{plan['price']}</div>
                <div>{plan['desc']}</div>
                <ul class='features'>
                    {''.join([f"<li>{f}</li>" for f in plan['features']])}
                </ul>
            </div>
        """, unsafe_allow_html=True)
        if st.button(f"Choose {plan['name']}", key=f"btn_{idx}"):
            st.session_state.selected_plan = plan["name"]

# SEZIONE PAGAMENTO
if st.session_state.selected_plan:
    st.markdown("---")
    st.subheader("Start Your Trial")
    st.markdown(f"**Selected Plan:** `{st.session_state.selected_plan}`")

    with st.form("payment_form"):
        email = st.text_input("Email Address")
        payment_method = st.radio("Payment Method", ["Credit Card"])
        if payment_method == "Credit Card":
            cc_number = st.text_input("Card Number")
            cc_expiry = st.text_input("MM/YY")
            cc_cvc = st.text_input("CVC")
        st.markdown(f"**{st.session_state.selected_plan} Plan (Monthly)**\n\n7-day free trial\n\nThen pricing as listed above.")
        submitted = st.form_submit_button("Start Free Trial")
        if submitted:
            st.success(f"✅ Subscription to {st.session_state.selected_plan} plan started for {email}!")
