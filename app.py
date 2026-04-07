import streamlit as st
from fpdf import FPDF

# --- CONFIGURATION ---
st.set_page_config(page_title="Carbon-Pulse Pro", layout="wide")

# --- SYSTÈME DE TRADUCTION ET CONVERSION ---
with st.sidebar:
    st.markdown("## ⚙️ Paramètres")
    lang_choice = st.selectbox("Langue", ["Français", "English"])
    
    currencies = {
        "USD ($)": {"rate": 1.0, "sym": "$"},
        "EUR (€)": {"rate": 0.92, "sym": "EUR"}, 
        "FCFA (CFA)": {"rate": 605.0, "sym": "FCFA"},
        "MAD (DH)": {"rate": 10.0, "sym": "DH"}
    }
    
    monnaie_choice = st.selectbox("Monnaie", list(currencies.keys()))
    taux = currencies[monnaie_choice]["rate"]
    sym = currencies[monnaie_choice]["sym"]

dic = {
    "English": {
        "titre_h1": "Global Carbon Compliance Audit",
        "data_entry": "Data Entry",
        "energy_label": "Energy Consumption (kWh/year)",
        "country_label": "Operating Country",
        "btn_audit": "RUN OFFICIAL AUDIT",
        "premium_title": "Premium Certification",
        "unlock_btn": "UNLOCK PDF REPORT & PRICING",
        "select_plan": "Select Plan:",
        "org_label": "🏢 Organization Name (Client)",
        "company_label": "🏗️ Enterprise Name (For Header)",
        "biz_info": "ℹ️ Business Plan: Header will be 'AUDIT REPORT'",
        "pay_btn": "PAY & DOWNLOAD",
        "pdf_header_gen": "AUDIT REPORT",
        "pdf_expert": "Carbon-Pulse Expert",
        "ai_title": "AI STRATEGIC ADVISORY",
        "source_text": "Source: expert-carbon-pulse-pro.streamlit.app"
    },
    "Français": {
        "titre_h1": "Audit de Conformité Carbone Mondial",
        "data_entry": "Saisie des Données",
        "energy_label": "Consommation Énergétique (kWh/an)",
        "country_label": "Pays d'Opération",
        "btn_audit": "LANCER L'AUDIT OFFICIEL",
        "premium_title": "Certification Premium",
        "unlock_btn": "DÉBLOQUER LE RAPPORT PDF & TARIFS",
        "select_plan": "Choisir un Plan :",
        "org_label": "🏢 Nom de l'Organisation (Client)",
        "company_label": "🏗️ Nom de l'Entreprise (Pour l'en-tête)",
        "biz_info": "ℹ️ Plan Business : L'en-tête sera 'RAPPORT D'AUDIT'",
        "pay_btn": "PAYER & TÉLÉCHARGER",
        "pdf_header_gen": "RAPPORT D'AUDIT",
        "pdf_expert": "Expert Carbon-Pulse",
        "ai_title": "CONSEILS STRATÉGIQUES IA",
        "source_text": "Source : expert-carbon-pulse-pro.streamlit.app"
    }
}

t = dic[lang_choice]

# --- DESIGN CSS ---
st.markdown("""
<style>
 #MainMenu, footer, header {visibility: hidden;}
 .stButton>button { background: #1e3a8a; color: white; border-radius: 6px; font-weight: bold; width: 100%; height: 3.5em; }
 .res-card { background: #f8fafc; padding: 20px; border-radius: 15px; border: 1px solid #e2e8f0; text-align: center; margin-bottom: 20px;}
 .premium-box { background: #1e3a8a; color: white; padding: 25px; border-radius: 15px; text-align: center;}
</style>
""", unsafe_allow_html=True)

# --- GÉNÉRATEUR PDF ---
def generate_pro_pdf(country, energy, result, plan, sym, lang, org_name, ent_name, final_price):
    pdf = FPDF()
    pdf.add_page()
    texts = dic[lang]
    
    # 1. En-tête
    pdf.set_font("Arial", 'B', 20)
    pdf.set_text_color(30, 58, 138)
    
    header_title = ent_name.upper() if ("1000" in plan and ent_name) else texts["pdf_header_gen"]
    pdf.cell(0, 15, header_title, ln=True, align='C')
    
    pdf.set_draw_color(30, 58, 138)
    pdf.line(10, 30, 200, 30)
    pdf.ln(10)

    # 2. Source (Pour formule 500)
    if "500" in plan:
        pdf.set_font("Arial", 'B', 10)
        pdf.set_text_color(200, 0, 0)
        pdf.cell(0, 10, texts["source_text"], ln=True, align='C')
        pdf.ln(5)

    # 3. Corps du rapport
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, f"Plan: {plan} ({final_price:,.0f} {sym})", ln=True)
    
    pdf.set_font("Arial", '', 11)
    pdf.cell(0, 8, f"Region: {country}", ln=True)
    pdf.cell(0, 8, f"Energy Consumption: {energy:,} kWh/year", ln=True)
    pdf.ln(10)

    # 4. Résultat
    pdf.set_fill_color(240, 240, 240)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 12, "CARBON FOOTPRINT RESULT", ln=True, fill=True, align='C')
    pdf.set_font("Arial", 'B', 24)
    pdf.set_text_color(16, 185, 129)
    pdf.cell(0, 20, f"{result:,.2f} Tonnes CO2e", ln=True, align='C')
    pdf.ln(10)

    # 5. IA Conseils (Uniquement 1000)
    if "1000" in plan:
        pdf.set_text_color(30, 58, 138)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, texts["ai_title"], ln=True)
        pdf.set_font("Arial", '', 10)
        pdf.set_text_color(50, 50, 50)
        advice = f"Based on the data for {country}, we recommend transitioning to 100% renewable energy to reduce emissions."
        pdf.multi_cell(0, 7, advice)
        pdf.ln(10)

    # 6. Signatures
    pdf.set_y(-60)
    pdf.set_font("Arial", 'B', 10)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(95, 10, texts["pdf_expert"], ln=0)
    pdf.cell(95, 10, f"Org: {org_name if org_name else '________________'}", ln=1)
    pdf.line(10, pdf.get_y()+5, 80, pdf.get_y()+5)
    pdf.line(110, pdf.get_y()+5, 190, pdf.get_y()+5)

    return pdf.output(dest='S').encode('cp1252', 'replace')

# --- INTERFACE ---
st.markdown(f"<h1>🚀 {t['titre_h1']}</h1>", unsafe_allow_html=True)

if 'calculated' not in st.session_state: st.session_state.calculated = False
if 'show_pricing' not in st.session_state: st.session_state.show_pricing = False

col1, col2 = st.columns([1.2, 1], gap="large")

with col1:
    st.markdown(f"### 📥 {t['data_entry']}")
    energy = st.number_input(t["energy_label"], min_value=0, value=120000)
    country = st.selectbox("Pays", ["USA", "France", "Maroc", "Gabon", "Sénégal", "Côte d'Ivoire"])
    resultat = (energy * 0.45) / 1000

    if st.button(t["btn_audit"]):
        st.session_state.calculated = True

    if st.session_state.calculated:
        st.markdown(f"""<div class="res-card"><h3>{resultat:,.2f} tCO2e</h3></div>""", unsafe_allow_html=True)

with col2:
    if st.session_state.calculated:
        st.markdown(f"### 💎 {t['premium_title']}")
        if st.button(t["unlock_btn"]): st.session_state.show_pricing = True
        
        if st.session_state.show_pricing:
            st.write("---")
            plan = st.radio(t["select_plan"], ["Business ($500)", "Enterprise ($1000)"])
            
            base_price = 500 if "500" in plan else 1000
            final_price = base_price * taux
            
            org_name = st.text_input(t["org_label"])
            ent_name = ""
            if "1000" in plan:
                ent_name = st.text_input(t["company_label"])
            else:
                st.info(t["biz_info"])

            st.markdown(f"""<div class="premium-box"><h2>{final_price:,.0f} {sym}</h2></div>""", unsafe_allow_html=True)
            st.write("")
            
            # Génération du contenu PDF
            pdf_out = generate_pro_pdf(country, energy, resultat, plan, sym, lang_choice, org_name, ent_name, final_price)
            
            st.download_button(
                label=f"{t['pay_btn']}",
                data=pdf_out,
                file_name=f"Report_{base_price}.pdf",
                mime="application/pdf"
            )
