import streamlit as st

# --- CONFIGURATION PRO & THÈME SOMBRE ---
st.set_page_config(page_title="Carbon-Pulse AI - Audit Premium", page_icon="🌍", layout="wide")

# CSS PERSONNALISÉ POUR DESIGN "TECH/DATA" (MODERN DARK MODE)
st.markdown("""
<style>
    /* Global Styles */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', sans-serif;
        background-color: #111111;
        color: #f5f5f7;
    }
    
    /* Headers */
    h1 {
        font-weight: 700;
        color: #f5f5f7;
    }
    h2, h3 {
        color: #A1A1A6;
        font-weight: 600;
    }

    /* Cards/Sections */
    [data-testid="stBlock"] {
        background-color: #1A1A1A;
        border-radius: 16px;
        padding: 2.5rem;
        border: 1px solid #333333;
        transition: all 0.3s ease-in-out;
    }
    [data-testid="stBlock"]:hover {
        border-color: #0071e3;
        box-shadow: 0 4px 20px rgba(0, 113, 227, 0.2);
    }

    /* Metric */
    [data-testid="stMetricValue"] {
        color: #f5f5f7;
        font-weight: 700;
        font-size: 3rem;
    }
    [data-testid="stMetricLabel"] {
        color: #A1A1A6;
    }

    /* Buttons */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.5em;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.2s;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    /* Primary Action Button (Audit) */
    .element-container:nth-of-type(3) button {
        background: linear-gradient(135deg, #0071e3 0%, #00a0f0 100%);
        color: white;
        border: none;
    }
    .element-container:nth-of-type(3) button:hover {
        background: linear-gradient(135deg, #005bb5 0%, #008cd4 100%);
        transform: translateY(-2px);
    }
    
    /* Upgrade Button */
    .element-container:nth-of-type(5) button {
        background-color: transparent;
        border: 2px solid #333333;
        color: #f5f5f7;
    }
    .element-container:nth-of-type(5) button:hover {
        border-color: #f5f5f7;
        background-color: #333333;
    }

    /* Input & Selectboxes */
    input, .stSelectbox > div {
        background-color: #1A1A1A !important;
        border: 1px solid #333333 !important;
        color: #f5f5f7 !important;
        border-radius: 8px !important;
    }
</style>
""", unsafe_allow_html=True)

# --- TRADUCTIONS ET SYMBOLES ---
TEXTS = {
    "English": {
        "title": "GLOBAL CARBON AUDIT",
        "subtitle": "Trusted Enterprise ESG Certification Platform",
        "input_hdr": "🚀 Data Collection",
        "label_energy": "Total Grid Energy Consumption (kWh/year)",
        "label_country": "Primary Operating Country",
        "btn_audit": "EXECUTE COMPLIANCE AUDIT",
        "result_hdr": "📊 Audit Results",
        "premium_hdr": "💎 Unlocked: Certification & Reporting",
        "premium_status": "PRO Status: 3-Day Enterprise Trial Active",
        "plan_biz": "Business Plan ($500/mo)",
        "plan_pro": "Enterprise Pro ($1000/mo)",
        "premium_btn": "GENERATE PREMIUM ESG REPORT (PDF)"
    },
    "Français": {
        "title": "AUDIT CARBONE GLOBAL",
        "subtitle": "Plateforme d'Audit ESG et Certification d'Entreprise",
        "input_hdr": "🚀 Collecte des Données",
        "label_energy": "Consommation Électrique Totale (kWh/an)",
        "label_country": "Pays d'Opération Principal",
        "btn_audit": "EXÉCUTER L'AUDIT DE CONFORMITÉ",
        "result_hdr": "📊 Résultats de l'Audit",
        "premium_hdr": "💎 Débloqué : Certification & Reporting",
        "premium_status": "Statut PRO : Essai Entreprise de 3 jours Activé",
        "plan_biz": "Plan Business (500€/mois)",
        "plan_pro": "Expert Pro (1000€/mois)",
        "premium_btn": "GÉNÉRER LE RAPPORT ESG PREMIUM (PDF)"
    }
}

# --- BARRE LATÉRALE (PARAMÈTRES PRO) ---
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    lang = st.selectbox("Language / Langue", ["English", "Français"])
    currency = st.selectbox("Currency / Monnaie", ["USD ($)", "EUR (€)", "MAD (DH)", "XAF (FCFA)"])
    st.write("---")
    st.caption(f"App Version: 1.1")
    st.caption(f"Powered by: Carbon-Pulse AI")

# --- CONTENU PRINCIPAL ---
t = TEXTS[lang]
symbol = currency.split(" ")[1].replace("(", "").replace(")", "")

# Entête de page Pro
st.title(f"{t['title']}")
st.markdown(f"<p style='color: #A1A1A6; font-size: 1.2rem; margin-top: -15px;'>{t['subtitle']}</p>", unsafe_allow_html=True)
st.write("---")

# Structure principale en deux colonnes
col1, col2 = st.columns([2, 1.3], gap="large")

with col1:
    st.subheader(t['input_hdr'])
    # Champ de saisie pro avec min et max réalistes
    energy = st.number_input(t["label_energy"], min_value=1, max_value=10000000, value=120000)
    country = st.selectbox(t["label_country"], ["Gabon", "Maroc", "France", "USA", "Autres pays d'Afrique subsaharienne"])
    st.write("") # Espace
    
    # Le bouton pour lancer l'audit (avec effet de chargement)
    if st.button(t["btn_audit"]):
        with st.spinner('Calculating footprint with real-time grid factors...'):
            # Facteurs d'émission (simplifiés pour l'exemple, mais crédibles)
            factors = {
                "Gabon": 0.350, # Moyenne indicative
                "Maroc": 0.708, # Source ONEE indicative
                "France": 0.050, # Très bas (nucléaire/renouvelable)
                "USA": 0.380,    # Moyenne
                "Autres pays d'Afrique subsaharienne": 0.550 # Moyenne large
            }
            factor = factors[country]
            
            # Calcul et conversion en tonnes (kg / 1000)
            footprint_tco2e = (energy * factor) / 1000
            
            st.write("---")
            st.subheader(t['result_hdr'])
            # Affichage Metric Ultra Pro
            st.metric("Total Emissions", f"{footprint_tco2e:.2f} tCO2e", f"{footprint_tco2e:.1f} tCO2e / MWh")
            st.success(f"Audit completed. Factor used: {factor:.3f} kgCO2e/kWh ({country})")
            st.balloons()

with col2:
    st.subheader(t['premium_hdr'])
    # Zone de confiance (Trust Badge)
    st.markdown(f"""
        <div style="background-color: rgba(0, 113, 227, 0.1); border: 1px solid #0071e3; border-radius: 12px; padding: 1.5rem; margin-bottom: 2rem;">
            <p style="color: #0071e3; font-weight: 600; font-size: 1.1rem; text-align: center; margin: 0;">{t['premium_status']}</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Affichage des plans avec prix fixes et monnaie choisie
    # (Les prix sont fixes pour l'exemple, on les automatisera plus tard)
    p1 = "500" if "USD" in currency or "EUR" in currency else "5000" if "MAD" in currency else "320,000"
    p2 = "1000" if "USD" in currency or "EUR" in currency else "10000" if "MAD" in currency else "640,000"

    # Plan Business
    st.markdown(f"<p style='color: #f5f5f7; font-weight: 600; font-size: 1.1rem;'>✅ {t['plan_biz']}</p>", unsafe_allow_html=True)
    st.code(f"{p1} {symbol} / month")
    st.caption("- Includes Certification & Report PDF")
    st.write("")
    
    # Plan Enterprise Pro
    st.markdown(f"<p style='color: #f5f5f7; font-weight: 600; font-size: 1.1rem;'>🔥 {t['plan_pro']}</p>", unsafe_allow_html=True)
    st.code(f"{p2} {symbol} / month")
    st.caption("- Full ESG Audit, Multi-site, Custom Factors")
    
    st.write("---")
    
    # LE BOUTON DE DEVIS / RAPPORT
    # C'est ici que se fait le rapport. Plus tard, ce bouton débloquera le vrai PDF.
    if st.button(t['premium_btn']):
        st.info("Generating professional audit summary...")
        # Simule le temps de génération
        import time
        time.sleep(2)
        
        # Exemple d'intégration d'un fichier PDF (on le fera plus tard)
        # Mais on va inclure un document PDF de test
        with open("rapport_exemple.pdf", "rb") as file:
            btn = st.download_button(
                    label="⬇️ Download Your Official Audit Report",
                    data=file,
                    file_name="Carbon-Pulse_Pro_Audit.pdf",
                    mime="application/pdf"
                  )
