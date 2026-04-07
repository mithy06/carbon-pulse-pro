import streamlit as st
from fpdf import FPDF
import time

# --- CONFIGURATION PRO ---
st.set_page_config(page_title="Carbon-Pulse Pro", layout="wide")

st.markdown("""
<style>
    #MainMenu, footer, header, [data-testid="stStatusWidget"] {visibility: hidden;}
    .main { background-color: #ffffff; }
    .stButton>button { background: #1e3a8a; color: white; border-radius: 6px; border: none; height: 3.5em; width: 100%; font-weight: 600; }
    .res-card { background: #f8fafc; padding: 30px; border-radius: 12px; border: 1px solid #e2e8f0; text-align: center; }
</style>
""", unsafe_allow_html=True)

# --- FONCTION QUI CREE LE RAPPORT ---
def generer_pdf(pays, energie, score):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "RAPPORT D'AUDIT CARBONE OFFICIEL", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", '', 12)
    pdf.cell(200, 10, f"Pays : {pays}", ln=True)
    pdf.cell(200, 10, f"Consommation : {energie} kWh", ln=True)
    pdf.cell(200, 10, f"Resultat : {score:.2f} tCO2e", ln=True)
    pdf.ln(10)
    pdf.multi_cell(0, 10, "Ce document certifie la conformite de votre bilan carbone selon les standards Carbon-Pulse Pro.")
    return pdf.output(dest='S').encode('latin-1')

# --- INTERFACE ---
st.markdown("<h1 style='text-align: center; color: #1e3a8a;'>Carbon-Pulse Pro</h1>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📊 Calculateur")
    energie = st.number_input("Consommation (kWh)", min_value=1, value=120000)
    pays = st.selectbox("Pays", ["Maroc", "Gabon", "Senegal", "France"])
    
    f = {"Maroc": 0.7, "Gabon": 0.35, "Senegal": 0.58, "France": 0.05}
    score = (energie * f[pays]) / 1000
    
    if st.button("CALCULER"):
        st.markdown(f"<div class='res-card'><h2>{score:.2f} tCO2e</h2><p>Audit Termine</p></div>", unsafe_allow_html=True)

with col2:
    st.subheader("💎 Rapport Premium")
    st.write("Prix : 500.00 USD")
    
    # CE BOUTON GENERE ET TELECHARGE DIRECTEMENT
    pdf_final = generer_pdf(pays, energie, score)
    
    st.download_button(
        label="📥 TELECHARGER LE RAPPORT (PDF)",
        data=pdf_final,
        file_name=f"Audit_{pays}.pdf",
        mime="application/pdf"
    )
