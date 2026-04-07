import streamlit as st
from fpdf import FPDF

# --- CONFIGURATION ---
st.set_page_config(page_title="Carbon-Pulse Pro", layout="wide")

# --- SYSTÈME DE TRADUCTION ---
with st.sidebar:
    st.markdown("## ⚙️ Settings")
    lang_choice = st.selectbox("Language / Langue", ["English", "Français"])
    monnaie = st.selectbox("Currency / Monnaie", ["USD ($)", "EUR (€)", "MAD (DH)"])
    sym = monnaie.split("(")[1].replace(")", "")

# Dictionnaire des textes de l'interface
dic = {
    "English": {
        "titre_h1": "Global Carbon Compliance Audit",
        "data_entry": "Data Entry",
        "energy_label": "Energy Consumption (kWh/year)",
        "country_label": "Operating Country",
        "btn_audit": "RUN OFFICIAL AUDIT",
        "res_card": "ESTIMATED FOOTPRINT",
        "premium_title": "Premium Certification",
        "unlock_btn": "UNLOCK PDF REPORT & PRICING",
        "select_plan": "Select Plan:",
        "company_label": "🏢 Company Name (Required for Enterprise Report)",
        "biz_info": "ℹ️ Business Plan: Standard Audit Report (Generic Header)",
        "pay_btn": "PAY & DOWNLOAD",
        "pdf_header_gen": "AUDIT REPORT",
        "pdf_expert": "Carbon-Pulse Expert",
        "pdf_client": "Authorized Signature",
        "ai_title": "AI STRATEGIC ADVISORY",
        "url_text": "Official Portal: expert-carbon-pulse-pro.streamlit.app"
    },
    "Français": {
        "titre_h1": "Audit de Conformité Carbone Mondial",
        "data_entry": "Saisie des Données",
        "energy_label": "Consommation Énergétique (kWh/an)",
        "country_label": "Pays d'Opération",
        "btn_audit": "LANCER L'AUDIT OFFICIEL",
        "res_card": "EMPREINTE ESTIMÉE",
        "premium_title": "Certification Premium",
        "unlock_btn": "DÉBLOQUER LE RAPPORT PDF & TARIFS",
        "select_plan": "Choisir un Plan :",
        "company_label": "🏢 Nom de l'Entreprise (Requis pour le rapport Enterprise)",
        "biz_info": "ℹ️ Plan Business : Rapport d'audit standard (En-tête générique)",
        "pay_btn": "PAYER & TÉLÉCHARGER",
        "pdf_header_gen": "RAPPORT D'AUDIT",
        "pdf_expert": "Expert Carbon-Pulse",
        "pdf_client": "Signature Autorisée",
        "ai_title": "CONSEILS STRATÉGIQUES IA",
        "url_text": "Portail Officiel : expert-carbon-pulse-pro.streamlit.app"
    }
}

t = dic[lang_choice]

# --- DESIGN CSS ---
st.markdown("""
<style>
 #MainMenu, footer, header, [data-testid="stStatusWidget"] {visibility: hidden;}
 section[data-testid="stSidebar"] { background-color: #f1f5f9; border-right: 1px solid #e2e8f0; }
 .main { background-color: #ffffff; }
 .stButton>button { background: #1e3a8a; color: white; border-radius: 6px; font-weight: bold; width: 100%; height: 3.5em; }
 .res-card { background: #f8fafc; padding: 30px; border-radius: 15px; border: 1px solid #e2e8f0; text-align: center; }
 .premium-box { background: #1e3a8a; color: white; padding: 25px; border-radius: 15px; }
 .company-input { margin-bottom: 20px; }
</style>
""", unsafe_allow_html=True)

# --- GÉNÉRATEUR PDF CONDITIONNEL ---
def generate_pro_pdf(country, energy, result, plan, sym, lang, company_name=""):
    pdf = FPDF()
    pdf.add_page()
    
    # Récupération des textes PDF selon la langue
    texts = dic[lang]

    # 1. EN-TÊTE DYNAMIQUE
    pdf.set_font("Arial", 'B', 20)
    pdf.set_text_color(30, 58, 138)
    
    if "1000" in plan and company_name:
        pdf.cell(0, 15, company_name.upper(), ln=True, align='C')
    else:
        pdf.cell(0, 15, texts["pdf_header_gen"], ln=True, align='C')
        
    pdf.set_draw_color(30, 58, 138)
    pdf.line(10, 30, 200, 30)
    pdf.ln(10)
    
    # 2. DÉTAILS DU RAPPORT
    pdf.set_font("Arial", 'B', 12); pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, f"Plan: {plan}", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.cell(0, 8, f"Region: {country} | Energy: {energy:,} kWh", ln=True)
    pdf.ln(5)
    
    # 3. RÉSULTAT
    pdf.set_fill_color(248, 250, 252)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 12, "TOTAL EMISSIONS", ln=True, fill=True, align='C')
    pdf.set_font("Arial", 'B', 24); pdf.set_text_color(16, 185, 129)
    pdf.cell(0, 20, f"{result:,.2f} Tonnes CO2e", ln=True, align='C')
    
    # 4. CONSEILS IA (UNIQUEMENT 1000$)
    if "1000" in plan:
        pdf.ln(5)
        pdf.set_font("Arial", 'B', 12); pdf.set_text_color(30, 58, 138)
        pdf.cell(0, 10, texts["ai_title"], ln=True)
        pdf.set_font("Arial", '', 10); pdf.set_text_color(50, 50, 50)
        reco = f"Strategic Analysis for {company_name if company_name else country}: Energy optimization recommended based on local grid factors."
        pdf.multi_cell(0, 8, reco)

    # 5. SIGNATURES
    pdf.ln(30)
    pdf.set_font("Arial", 'B', 10); pdf.set_text_color(0, 0, 0)
    pdf.cell(95, 10, texts["pdf_expert"], ln=0)
    pdf.cell(95, 10, f"{texts['pdf_client']} ({company_name if company_name else ''})", ln=1)
    pdf.line(10, pdf.get_y()+10, 80, pdf.get_y()+10)
    pdf.line(110, pdf.get_y()+10, 190, pdf.get_y()+10)

    # 6. PIED DE PAGE & URL (URL uniquement pour 500$)
    pdf.set_y(-30)
    pdf.set_font("Arial", 'I', 8); pdf.set_text_color(150, 150, 150)
    if "500" in plan:
        pdf.cell(0, 10, texts["url_text"], align='C', ln=True)
    pdf.cell(0, 5, f"Audit ID: CP-{country[:2].upper()}-2026", align='C')

    return pdf.output(dest='S').encode('latin-1')

# --- CENTRE ---
st.markdown(f"<h1>🚀 {t['titre_h1']}</h1>", unsafe_allow_html=True)

if 'show_pricing' not in st.session_state: st.session_state.show_pricing = False

col1, col2 = st.columns([1.2, 1], gap="large")

with col1:
    st.markdown(f"### 📥 {t['data_entry']}")
    energy = st.number_input(t["energy_label"], min_value=0, value=120000)
    country = st.selectbox(t["country_label"], ["USA", "France", "Morocco", "Gabon", "Senegal", "China"])
    
    factors = {"USA": 0.45, "France": 0.05, "Morocco": 0.70, "Gabon": 0.35, "Senegal": 0.58}
    resultat = (energy * factors.get(country, 0.50)) / 1000

    if st.button(t["btn_audit"]):
        st.session_state.calculated = True
        st.markdown(f"""<div class="res-card"><p>{t['res_card']}</p><h1>{resultat:,.2f} tCO2e</h1></div>""", unsafe_allow_html=True)

with col2:
    if 'calculated' in st.session_state:
        st.markdown(f"### 💎 {t['premium_title']}")
        if st.button(t["unlock_btn"]):
            st.session_state.show_pricing = True
        
        if st.session_state.show_pricing:
            st.write("---")
            plan = st.radio(t["select_plan"], ["Business ($500)", "Enterprise ($1000)"])
            
            company_name = ""
            if "1000" in plan:
                st.markdown('<div class="company-input">', unsafe_allow_html=True)
                company_name = st.text_input(t["company_label"], placeholder="Ex: Praises Electronics")
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.info(t["biz_info"])

            prix = "500" if "500" in plan else "1000"
            st.markdown(f"""<div class="premium-box"><h2 style="color:white; margin:0;">{prix}.00 {sym}</h2></div>""", unsafe_allow_html=True)
            
            pdf_pro = generate_pro_pdf(country, energy, resultat, plan, sym, lang_choice, company_name)
            st.download_button(
                label=f"{t['pay_btn']} ({prix} {sym})",
                data=pdf_pro,
                file_name=f"Audit_Report_{prix}.pdf",
                mime="application/pdf"
            )
