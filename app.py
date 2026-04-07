import streamlit as st
from fpdf import FPDF

# --- CONFIGURATION ---
st.set_page_config(page_title="Carbon-Pulse Pro", layout="wide")

# --- DESIGN SIDEBAR & INTERFACE ---
st.markdown("""
<style>
    #MainMenu, footer, header, [data-testid="stStatusWidget"] {visibility: hidden;}
    section[data-testid="stSidebar"] { background-color: #f1f5f9; border-right: 1px solid #e2e8f0; }
    .main { background-color: #ffffff; }
    .stButton>button { background: #1e3a8a; color: white; border-radius: 6px; font-weight: bold; width: 100%; }
    .res-card { background: #f8fafc; padding: 30px; border-radius: 15px; border: 1px solid #e2e8f0; text-align: center; }
    .premium-box { background: #1e3a8a; color: white; padding: 25px; border-radius: 15px; }
    /* Marge pour le champ de saisie */
    .company-input { margin-bottom: 20px; }
</style>
""", unsafe_allow_html=True)

# --- GÉNÉRATEUR PDF CONDITIONNEL ---
def generate_pro_pdf(country, energy, result, plan, sym, lang, company_name=""):
    pdf = FPDF()
    pdf.add_page()
    
    # Textes selon la langue
    txt = {
        "Français": {"titre": "RAPPORT D'AUDIT", "expert": "Expert Carbon-Pulse", "client": "Signature Client"},
        "English": {"titre": "AUDIT REPORT", "expert": "Carbon-Pulse Expert", "client": "Client Signature"}
    }
    t = txt.get(lang, txt["English"])

    # 1. EN-TÊTE DYNAMIQUE
    pdf.set_font("Arial", 'B', 20)
    pdf.set_text_color(30, 58, 138)
    
    if "1000" in plan and company_name:
        # Affichage du nom de l'entreprise pour le plan 1000$
        pdf.cell(0, 15, company_name.upper(), ln=True, align='C')
    else:
        # En-tête générique pour le plan 500$
        pdf.cell(0, 15, t["titre"], ln=True, align='C')
        
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
        pdf.cell(0, 10, "AI STRATEGIC ADVISORY", ln=True)
        pdf.set_font("Arial", '', 10); pdf.set_text_color(50, 50, 50)
        reco = f"Strategic Analysis for {company_name if company_name else country}: Energy optimization recommended."
        pdf.multi_cell(0, 8, reco)

    # 5. SIGNATURES
    pdf.ln(30)
    pdf.set_font("Arial", 'B', 10); pdf.set_text_color(0, 0, 0)
    pdf.cell(95, 10, t["expert"], ln=0)
    pdf.cell(95, 10, f"{t['client']} ({company_name if company_name else ''})", ln=1)
    pdf.line(10, pdf.get_y()+10, 80, pdf.get_y()+10)
    pdf.line(110, pdf.get_y()+10, 190, pdf.get_y()+10)

    # 6. PIED DE PAGE & URL (URL uniquement pour 500$)
    pdf.set_y(-30)
    pdf.set_font("Arial", 'I', 8); pdf.set_text_color(150, 150, 150)
    if "500" in plan:
        pdf.cell(0, 10, "Official Portal: expert-carbon-pulse-pro.streamlit.app", align='C', ln=True)
    pdf.cell(0, 5, f"Audit ID: CP-{country[:2].upper()}-2026", align='C')

    return pdf.output(dest='S').encode('latin-1')

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("## ⚙️ Settings")
    lang_choice = st.selectbox("Language / Langue", ["English", "Français"])
    monnaie = st.selectbox("Currency / Monnaie", ["USD ($)", "EUR (€)", "MAD (DH)"])
    sym = monnaie.split("(")[1].replace(")", "")

# --- CENTRE ---
st.markdown(f"<h1>🚀 Carbon-Pulse Pro | {lang_choice}</h1>", unsafe_allow_html=True)

if 'show_pricing' not in st.session_state: st.session_state.show_pricing = False

col1, col2 = st.columns([1.2, 1], gap="large")

with col1:
    st.markdown("### 📥 Data Entry")
    energy = st.number_input("Energy Consumption (kWh/year)", min_value=0, value=120000)
    country = st.selectbox("Operating Country", ["USA", "France", "Morocco", "Gabon", "Senegal", "China"])
    
    factors = {"USA": 0.45, "France": 0.05, "Morocco": 0.70, "Gabon": 0.35, "Senegal": 0.58}
    resultat = (energy * factors.get(country, 0.50)) / 1000

    if st.button("RUN OFFICIAL AUDIT"):
        st.session_state.calculated = True
        st.markdown(f"""<div class="res-card"><h1>{resultat:,.2f} tCO2e</h1></div>""", unsafe_allow_html=True)

with col2:
    if 'calculated' in st.session_state:
        st.markdown("### 💎 Premium Certification")
        if st.button("UNLOCK PDF REPORT & PRICING"):
            st.session_state.show_pricing = True
        
        if st.session_state.show_pricing:
            st.write("---")
            plan = st.radio("Select Plan:", ["Business ($500)", "Enterprise ($1000)"])
            
            # LOGIQUE DE MARGE ET SAISIE POUR 1000$
            company_name = ""
            if "1000" in plan:
                st.markdown('<div class="company-input">', unsafe_allow_html=True)
                company_name = st.text_input("🏢 Company Name (Required for Enterprise Report)", placeholder="Your Company Ltd.")
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.info("ℹ️ Business Plan: Standard Audit Report (Generic Header)")

            prix = "500" if "500" in plan else "1000"
            st.markdown(f"""<div class="premium-box"><h2 style="color:white; margin:0;">{prix}.00 {sym}</h2></div>""", unsafe_allow_html=True)
            
            pdf_pro = generate_pro_pdf(country, energy, resultat, plan, sym, lang_choice, company_name)
            st.download_button(
                label=f"PAY & DOWNLOAD ({prix} {sym})",
                data=pdf_pro,
                file_name=f"Audit_Report_{prix}.pdf",
                mime="application/pdf"
            )
