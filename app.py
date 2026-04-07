import streamlit as st
from fpdf import FPDF

# --- CONFIGURATION ---
st.set_page_config(page_title="Carbon-Pulse Pro", layout="wide")

# --- SYSTÈME DE TRADUCTION ET CONVERSION ---
with st.sidebar:
    st.markdown("## ⚙️ Settings")
    lang_choice = st.selectbox("Language / Langue", ["English", "Français"])
    
    # Dictionnaire des monnaies (Taux indicatifs basés sur 1 USD)
    currencies = {
        "USD ($)": {"rate": 1.0, "sym": "$"},
        "EUR (€)": {"rate": 0.92, "sym": "EUR"}, 
        "FCFA (CFA)": {"rate": 605.0, "sym": "FCFA"},
        "MAD (DH)": {"rate": 10.0, "sym": "DH"}
    }
    
    monnaie_choice = st.selectbox("Currency / Monnaie", list(currencies.keys()))
    taux = currencies[monnaie_choice]["rate"]
    sym = currencies[monnaie_choice]["sym"]

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
        "org_label": "🏢 Client Organization Name (Signature)",
        "company_label": "🏗️ Report Header Name (Enterprise)",
        "biz_info": "ℹ️ Business Plan: Report Header will be 'AUDIT REPORT'",
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
        "res_card": "EMPREINTE ESTIMÉE",
        "premium_title": "Certification Premium",
        "unlock_btn": "DÉBLOQUER LE RAPPORT PDF & TARIFS",
        "select_plan": "Choisir un Plan :",
        "org_label": "🏢 Nom de l'Organisation (Signature)",
        "company_label": "🏗️ Nom de l'Entreprise (Pour l'en-tête du rapport)",
        "biz_info": "ℹ️ Plan Business : L'en-tête du rapport sera 'RAPPORT D'AUDIT'",
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
 #MainMenu, footer, header, [data-testid="stStatusWidget"] {visibility: hidden;}
 section[data-testid="stSidebar"] { background-color: #f1f5f9; border-right: 1px solid #e2e8f0; }
 .stButton>button { background: #1e3a8a; color: white; border-radius: 6px; font-weight: bold; width: 100%; height: 3.5em; }
 .res-card { background: #f8fafc; padding: 30px; border-radius: 15px; border: 1px solid #e2e8f0; text-align: center; }
 .premium-box { background: #1e3a8a; color: white; padding: 25px; border-radius: 15px; }
</style>
""", unsafe_allow_html=True)

# --- GÉNÉRATEUR PDF ---
def generate_pro_pdf(country, energy, result, plan, sym, lang, org_name="", ent_name="", final_price=0):
    pdf = FPDF()
    pdf.add_page()
    texts = dic[lang]

    # 1. EN-TÊTE DYNAMIQUE (Modification demandée : Entreprise en en-tête pour 1000)
    pdf.set_font("Arial", 'B', 20)
    pdf.set_text_color(30, 58, 138)
    
    if "1000" in plan and ent_name:
        pdf.cell(0, 15, ent_name.upper(), ln=True, align='C')
    else:
        pdf.cell(0, 15, texts["pdf_header_gen"], ln=True, align='C')
        
    pdf.set_draw_color(30, 58, 138)
    pdf.line(10, 30, 200, 30)
    
    # 2. SOURCE BIEN VISIBLE (Uniquement pour formule 500)
    if "500" in plan:
        pdf.ln(5)
        pdf.set_font("Arial", 'B', 12)
        pdf.set_text_color(200, 0, 0)
        pdf.cell(0, 10, texts["source_text"], ln=True, align='C')
        pdf.ln(5)
    else:
        pdf.ln(10)
    
    # 3. DÉTAILS DU RAPPORT
    pdf.set_font("Arial", 'B', 12); pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, f"Plan: {plan} ({final_price:,.0f} {sym})", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.cell(0, 8, f"Region: {country} | Energy: {energy:,} kWh", ln=True)
    pdf.ln(5)
    
    # 4. RÉSULTAT
    pdf.set_fill_color(248, 250, 252); pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 12, "TOTAL CERTIFIED EMISSIONS", ln=True, fill=True, align='C')
    pdf.set_font("Arial", 'B', 24); pdf.set_text_color(16, 185, 129)
    pdf.cell(0, 20, f"{result:,.2f} Tonnes CO2e", ln=True, align='C')
    
    # 5. CONSEILS IA (Uniquement sur la formule de 1000)
    if "1000" in plan:
        pdf.ln(5); pdf.set_font("Arial", 'B', 12); pdf.set_text_color(30, 58, 138)
        pdf.cell(0, 10, texts["ai_title"], ln=True)
        pdf.set_font("Arial", '', 10); pdf.set_text_color(50, 50, 50)
        reco = f"Strategic Analysis: Decarbonization roadmap recommended for local operations in {country}."
        pdf.multi_cell(0, 8, reco)

    # 6. SIGNATURES (Marge pour le nom de l'organisation)
    pdf.ln(30); pdf.set_font("Arial", 'B', 10); pdf.set_text_color(0, 0, 0)
    pdf.cell(95, 10, texts["pdf_expert"], ln=0)
    pdf.cell(95, 10, f"{org_name if org_name else 'Client Organization'}", ln=1)
    pdf.line(10, pdf.get_y()+10, 80, pdf.get_y()+10)
    pdf.line(110, pdf.get_y()+10, 190, pdf.get_y()+10)

    # Encodage sécurisé pour éviter l'erreur Unicode
    return pdf.output(dest='S').encode('cp1252', 'replace')

# --- INTERFACE ---
st.markdown(f"<h1>🚀 {t['titre_h1']}</h1>", unsafe_allow_html=True)

if 'calculated' not in st.session_state: st.session_state.calculated = False
if 'show_pricing' not in st.session_state: st.session_state.show_pricing = False

col1, col2 = st.columns([1.2, 1], gap="large")

with col1:
    st.markdown(f"### 📥 {t['data_entry']}")
    energy = st.number_input(t["energy_label"], min_value=0, value=120000)
    country = st.selectbox(t["country_label"], ["USA", "France", "Morocco", "Gabon", "Senegal", "Ivory Coast"])
    resultat = (energy * 0.45) / 1000

    if st.button(t["btn_audit"]):
        st.session_state.calculated = True
        st.markdown(f"""<div class="res-card"><h1>{resultat:,.2f} tCO2e</h1></div>""", unsafe_allow_html=True)

with col2:
    if st.session_state.calculated:
        st.markdown(f"### 💎 {t['premium_title']}")
        if st.button(t["unlock_btn"]): st.session_state.show_pricing = True
        
        if st.session_state.show_pricing:
            st.write("---")
            plan = st.radio(t["select_plan"], ["Business ($500)", "Enterprise ($1000)"])
            
            # Calcul du prix converti
            base_price = 500 if "500" in plan else 1000
            final_price = base_price * taux
            
            # Marge sur le site pour l'organisation (disponible pour les deux plans)
            org_name = st.text_input(t["org_label"], placeholder="Nom du client de l'entreprise...")
            
            # Marge sur le site pour l'entreprise en-tête (uniquement pour 1000)
            ent_name = ""
            if "1000" in plan:
                ent_name = st.text_input(t["company_label"], placeholder="Nom qui figurera en en-tête...")
            else:
                st.info(t["biz_info"])

            # Affichage du prix dynamique
            st.markdown(f"""<div class="premium-box"><h2 style="color:white; margin:0;">{final_price:,.0f} {sym}</h2></div>""", unsafe_allow_html=True)
            
            # Génération et téléchargement
            pdf_data = generate_pro_pdf(country, energy, resultat, plan, sym, lang_choice, org_name, ent_name, final_price)
            
            st.download_button(
                label=f"{t['pay_btn']} ({final_price:,.0f} {sym})",
                data=pdf_data,
                file_name=f"Audit_Report_{base_price}.pdf",
                mime="application/pdf"
            )
