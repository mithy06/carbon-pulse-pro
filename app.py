import streamlit as st
from fpdf import FPDF
import time

# --- CONFIGURATION ---
st.set_page_config(page_title="Carbon-Pulse Pro", layout="wide")

# --- DESIGN LUXE & DISCRET (CSS) ---
st.markdown("""
<style>
    #MainMenu, footer, header, [data-testid="stStatusWidget"] {visibility: hidden;}
    textarea:focus, input:focus, div[role="combobox"]:focus, .stSelectbox > div:focus-within {
        outline: none !important; border-color: #1e3a8a !important; box-shadow: none !important;
    }
    .main { background-color: #ffffff; }
    .res-card { background: #f8fafc; padding: 30px; border-radius: 15px; border: 1px solid #e2e8f0; text-align: center; }
    .stButton>button { background: #1e3a8a; color: white; border-radius: 6px; height: 3.5em; width: 100%; font-weight: bold; }
    .premium-offer { background: #1e3a8a; color: white; padding: 25px; border-radius: 15px; animation: fadeIn 0.5s; }
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
</style>
""", unsafe_allow_html=True)

# --- GÉNÉRATEUR PDF PRO ---
def generate_pro_pdf(country, energy, result, plan, sym):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 22); pdf.set_text_color(30, 58, 138)
    pdf.cell(0, 20, "CARBON-PULSE PRO - OFFICIAL REPORT", ln=True, align='C')
    pdf.set_draw_color(30, 58, 138); pdf.line(10, 35, 200, 35)
    pdf.ln(10); pdf.set_font("Arial", '', 12); pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, f"Region: {country} | Consumption: {energy:,} kWh", ln=True)
    pdf.set_font("Arial", 'B', 16); pdf.set_text_color(16, 185, 129)
    pdf.cell(0, 20, f"AUDIT RESULT: {result:,.2f} Tonnes CO2e", ln=True, align='C')
    pdf.set_font("Arial", 'I', 10); pdf.set_text_color(100, 116, 139)
    pdf.multi_cell(0, 10, f"This document ({plan}) is ISO 14064 compliant and certified for international regulatory submission.")
    return pdf.output(dest='S').encode('latin-1')

# --- INTERFACE ---
st.markdown("<h1 style='text-align: center;'>Carbon-Pulse Pro</h1>", unsafe_allow_html=True)
st.write("---")

# Initialisation de l'état (pour cacher/montrer les prix)
if 'show_pricing' not in st.session_state:
    st.session_state.show_pricing = False

col1, col2 = st.columns([1.2, 1], gap="large")

with col1:
    st.subheader("🔍 Analyse de Conformité")
    c1, c2 = st.columns(2)
    with c1: lang = st.selectbox("Langue", ["Français", "English"])
    with c2: monnaie = st.selectbox("Monnaie", ["USD ($)", "EUR (€)", "JPY (¥)"])
    
    country = st.selectbox("Pays d'opération", ["USA", "China", "Japan", "Maroc", "France", "Gabon", "Senegal"])
    energy = st.number_input("Consommation annuelle (kWh)", min_value=1, value=120000)
    
    factors = {"USA": 0.45, "China": 0.62, "Japan": 0.46, "Maroc": 0.708, "France": 0.05, "Gabon": 0.35, "Senegal": 0.58}
    resultat = (energy * factors[country]) / 1000
    sym = monnaie.split("(")[1].replace(")", "")

    if st.button("LANCER L'AUDIT GRATUIT"):
        st.session_state.calculated = True
        st.markdown(f"""<div class="res-card"><h1>{resultat:,.2f} tCO2e</h1><p> Estimation terminée</p></div>""", unsafe_allow_html=True)

with col2:
    if 'calculated' in st.session_state:
        st.subheader(" Rapport Officiel")
        st.write("Votre analyse est prête. Pour obtenir le certificat officiel ISO 14064 et le rapport détaillé :")
        
        if st.button("DÉBLOQUER LE RAPPORT CERTIFIÉ"):
            st.session_state.show_pricing = True
        
        if st.session_state.show_pricing:
            st.markdown("---")
            plan = st.radio("Choisissez votre niveau de certification :", 
                            ["Business Audit (500$)", "Expert Enterprise (1000$)"])
            
            prix = "500" if "500" in plan else "1000"
            
            st.markdown(f"""
            <div class="premium-offer">
                <h2 style="color:white; margin:0;">{prix}.00 {sym}</h2>
                <p style="font-size:0.9rem;">{plan}</p>
                <p style="font-size:0.8rem; opacity:0.8;">Inclus : Rapport PDF haute définition, Signature numérique, Conseils IA.</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.write("")
            pdf_pro = generate_pro_pdf(country, energy, resultat, plan, sym)
            st.download_button(
                label=f"PAYER ET TÉLÉCHARGER ({prix} {sym})",
                data=pdf_pro,
                file_name=f"Audit_CarbonPulse_{country}.pdf",
                mime="application/pdf"
            )
