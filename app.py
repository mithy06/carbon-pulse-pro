import streamlit as st

# --- DESIGN PROFESSIONNEL ---
st.set_page_config(page_title="Carbon-Pulse Pro", layout="wide")
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #007BFF; color: white; border: none; font-weight: bold; }
    .stButton>button:hover { background-color: #0056b3; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- TRADUCTIONS ---
TEXTS = {
    "English": {
        "title": "Global Carbon Compliance Audit",
        "label_energy": "Energy Consumption (kWh)",
        "label_country": "Operating Country",
        "btn_audit": "RUN OFFICIAL AUDIT",
        "plan_biz": "Business Plan ($500/mo)",
        "plan_pro": "Enterprise Pro ($1000/mo)",
        "trial": "3-Day Trial Active"
    },
    "Français": {
        "title": "Audit de Conformité Carbone Global",
        "label_energy": "Consommation Énergie (kWh)",
        "label_country": "Pays d'Opération",
        "btn_audit": "LANCER L'AUDIT OFFICIEL",
        "plan_biz": "Plan Business (500€/mois)",
        "plan_pro": "Expert Pro (1000€/mois)",
        "trial": "Essai de 3 jours Activé"
    }
}

# --- BARRE LATÉRALE (PARAMÈTRES) ---
with st.sidebar:
    st.title("⚙️ Settings")
    lang = st.selectbox("Language / Langue", ["English", "Français"])
    currency = st.selectbox("Currency / Monnaie", ["USD ($)", "EUR (€)", "MAD (DH)", "XAF (FCFA)"])
    st.write("---")
    st.success(TEXTS[lang]["trial"])

# --- CONTENU PRINCIPAL ---
t = TEXTS[lang]
st.title(f"🚀 {t['title']}")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📥 Data Entry")
    energy = st.number_input(t["label_energy"], min_value=0)
    country = st.selectbox(t["label_country"], ["Maroc", "Gabon", "France", "USA"])
    
    if st.button(t["btn_audit"]):
        # Calcul simple basé sur le pays choisi
        factor = 0.708 if country == "Maroc" else 0.350 if country == "Gabon" else 0.1
        st.metric("Total Footprint", f"{(energy * factor) / 1000:.2f} tCO2e")

with col2:
    st.subheader("💎 Premium Plans")
    st.info(f"**{t['plan_biz']}**\n\nStandard reporting & Certification")
    st.warning(f"**{t['plan_pro']}**\n\nFull ESG Audit & Multi-site")
    st.button("Upgrade to Unlock PDF Report")
