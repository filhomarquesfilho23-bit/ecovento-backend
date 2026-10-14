import streamlit as st

# Configuração da página para o Site Institucional
st.set_page_config(
    page_title="OmniFlux Pro - Sistema Operativo Líquido", 
    page_icon="⚡", 
    layout="wide"
)

# Estilo CSS Personalizado para a Landing Page
st.markdown("""
    <style>
    .main-title {
        font-size: 3rem;
        font-weight: 800;
        color: #ffffff;
        text-align: center;
        margin-bottom: 0px;
    }
    .subtitle {
        font-size: 1.2rem;
        color: #00bfff;
        text-align: center;
        margin-bottom: 30px;
    }
    .hero-text {
        text-align: center;
        font-size: 1.1rem;
        color: #cccccc;
        max-width: 700px;
        margin: 0 auto 40px auto;
    }
    .feature-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 25px;
        text-align: center;
        height: 100%;
    }
    .feature-title {
        color: #00bfff;
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .stButton>button {
        background-color: #007acc !important;
        color: #ffffff !important;
        border: 2px solid #00bfff !important;
        border-radius: 10px !important;
        font-weight: bold !important;
        padding: 10px 24px;
    }
    .stButton>button:hover {
        background-color: #00bfff !important;
        color: #0e1117 !important;
        border-color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- CABEÇALHO / HERO SECTION ---
st.markdown('<p class="main-title">⚡ OmniFlux Pro</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">O Sistema Operativo Líquido com Consola Unificada e Inteligência Artificial</p>', unsafe_allow_html=True)

st.markdown(
    '<p class="hero-text">'
    'Simplifique a gestão da sua empresa, equipa e finanças num só lugar. '
    'Com tecnologia de ponta, base de dados segura e comandos de voz inteligentes.'
    '</p>', 
    unsafe_allow_html=True
)

# Botão de Ação Direta para a Aplicação
col_space1, col_btn, col_space2 = st.columns([2, 2, 2])
with col_btn:
    # Substitua o link abaixo pelo link real da sua app no Streamlit Cloud quando tiver
    link_app = "https://seu-link-do-streamlit.app" 
    st.markdown(f'<a href="{link_app}" target="_blank"><button style="width: 100%; background-color: #007acc; color: white; border: 2px solid #00bfff; border-radius: 10px; padding: 12px; font-weight: bold; cursor: pointer;">🚀 Aceder à Aplicação</button></a>', unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# --- SECÇÃO DE FUNCIONALIDADES (Grelha) ---
st.markdown("## 🌟 Funcionalidades Principais")
st.markdown("Descubra o que torna o OmniFlux Pro a ferramenta ideal para o seu negócio:")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div class="feature-card">
            <div class="feature-title">🎙️ Assistente de Voz</div>
            <p style="color: #a0a0a0;">Interaja com o sistema através de comandos de voz inteligentes e feedback em tempo real.</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="feature-card">
            <div class="feature-title">💰 Gestão Financeira</div>
            <p style="color: #a0a0a0;">Controlo absoluto de saldos, faturas e relatórios com exportação imediata em CSV.</p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="feature-card">
            <div class="feature-title">🔒 Segurança Avançada</div>
            <p style="color: #a0a0a0;">Sistema multi-utilizador protegido com base de dados SQLite integrada e encriptada.</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# --- SECÇÃO SOBRE / ESTATÍSTICAS ---
st.markdown("## 📊 O OmniFlux em Números")
m1, m2, m3 = st.columns(3)
m1.metric("Disponibilidade", "99.9%", "Cloud Ready")
m2.metric("Velocidade de Processamento", "< 0.2s", "Otimizado")
m3.metric("Satisfação de Utilizadores", "100%", "+5.4%")

# --- RODAPÉ DO SITE ---
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #777777; font-size: 0.9rem;'>"
    "© 2026 OmniFlux Pro. Todos os direitos reservados. Desenvolvido com Streamlit & Python."
    "</p>", 
    unsafe_allow_html=True
)
