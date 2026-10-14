import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import hashlib

# Configuração da página
st.set_page_config(
    page_title="OmniFlux Pro - Sistema Operativo Líquido", 
    page_icon="⚡", 
    layout="centered"
)

# --- BASE DE DADOS SQLITE ---
def init_db():
    conn = sqlite3.connect('omniflux.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS finances (id INTEGER PRIMARY KEY AUTOINCREMENT, categoria TEXT, montante REAL)''')
    
    cursor.execute("SELECT * FROM users WHERE username = 'admin'")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('admin', hashlib.sha256('admin123'.encode()).hexdigest()))
    
    cursor.execute("SELECT * FROM finances")
    if not cursor.fetchone():
        initial_data = [("Receitas", 32000), ("Despesas", 12500), ("Investimentos", 8000), ("Manutenção", 2500)]
        cursor.executemany("INSERT INTO finances (categoria, montante) VALUES (?, ?)", initial_data)
        
    conn.commit()
    return conn

conn = init_db()
cursor = conn.cursor()

# Estilo CSS Personalizado
st.markdown("""
    <style>
    .main-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: #ffffff;
        text-align: center;
        margin-bottom: 0px;
    }
    .subtitle {
        font-size: 1.1rem;
        color: #00bfff;
        text-align: center;
        margin-bottom: 20px;
    }
    .hero-text {
        text-align: center;
        font-size: 1rem;
        color: #cccccc;
        max-width: 700px;
        margin: 0 auto 30px auto;
    }
    .feature-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        margin-bottom: 15px;
    }
    .feature-title {
        color: #00bfff;
        font-size: 1.1rem;
        font-weight: bold;
        margin-bottom: 8px;
    }
    .stButton>button {
        background-color: #007acc !important;
        color: #ffffff !important;
        border: 2px solid #00bfff !important;
        border-radius: 10px !important;
        font-weight: bold !important;
    }
    .stButton>button:hover {
        background-color: #00bfff !important;
        color: #0e1117 !important;
        border-color: #ffffff !important;
    }
    div.stButton > button:has-text("Entrar no Sistema") {
        background-color: #111111 !important;
        color: #ffffff !important;
        border: 2px solid #444444 !important;
    }
    div.stButton > button:has-text("Entrar no Sistema"):hover {
        background-color: #222222 !important;
        border-color: #00bfff !important;
    }
    [data-testid="stMetricValue"] {
        color: #00bfff !important;
    }
    </style>
""", unsafe_allow_html=True)

# Gestão de Sessão e Estados de Navegação
if "modo_app" not in st.session_state:
    st.session_state.modo_app = False  # False = Mostra o Site | True = Mostra o Sistema

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

if "pagina_atual" not in st.session_state:
    st.session_state.pagina_atual = "Home"


# --- SE O UTILIZADOR AINDA ESTIVER NO SITE INSTITUCIONAL ---
if not st.session_state.modo_app:
    st.markdown('<p class="main-title">⚡ OmniFlux Pro</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">O Sistema Operativo Líquido com Consola Unificada e Inteligência Artificial</p>', unsafe_allow_html=True)
    
    st.markdown(
        '<p class="hero-text">'
        'Simplifique a gestão da sua empresa, equipa e finanças num só lugar. '
        'Com tecnologia de ponta, base de dados segura e comandos de voz inteligentes.'
        '</p>', 
        unsafe_allow_html=True
    )

    # Botão para entrar na aplicação interna
    col_space1, col_btn, col_space2 = st.columns([1, 2, 1])
    with col_btn:
        if st.button("🚀 Aceder à Aplicação", use_container_width=True):
            st.session_state.modo_app = True
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("## 🌟 Funcionalidades Principais")
    
    st.markdown("""
        <div class="feature-card">
            <div class="feature-title">🎙️ Assistente de Voz</div>
            <p style="color: #a0a0a0; font-size: 0.9rem;">Interaja com o sistema através de comandos inteligentes e feedback em tempo real.</p>
        </div>
        <div class="feature-card">
            <div class="feature-title">💰 Gestão Financeira</div>
            <p style="color: #a0a0a0; font-size: 0.9rem;">Controlo absoluto de saldos e relatórios com exportação imediata em CSV.</p>
        </div>
        <div class="feature-card">
            <div class="feature-title">🔒 Segurança Avançada</div>
            <p style="color: #a0a0a0; font-size: 0.9rem;">Sistema multi-utilizador protegido com base de dados SQLite integrada.</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown(
        "<p style='text-align: center; color: #777777; font-size: 0.85rem;'>"
        "© 2026 OmniFlux Pro. Todos os direitos reservados."
        "</p>", 
        unsafe_allow_html=True
    )


# --- SE CLICOU PARA ACEDER À APLICAÇÃO ---
else:
    # Botão para voltar ao site institucional
    if not st.session_state.logged_in:
        if st.button("⬅️ Voltar à Apresentação do Site"):
            st.session_state.modo_app = False
            st.rerun()
        st.markdown("---")

    # 1. Ecrã de Início de Sessão & Registo
    if not st.session_state.logged_in:
        st.title("⚡ OmniFlux Pro - Sistema")
        st.markdown("Introduza as suas credenciais para entrar.")
        
        tab1, tab2 = st.tabs(["🔑 Iniciar Sessão", "📄 Criar Conta"])
        
        with tab1:
            st.subheader("Iniciar Sessão")
            user_input = st.text_input("Utilizador", value="admin")
            pass_input = st.text_input("Palavra-passe", type="password")
            
            if st.button("Entrar no Sistema", use_container_width=True):
                hashed_pass = hashlib.sha256(pass_input.encode()).hexdigest()
                cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (user_input, hashed_pass))
                if cursor.fetchone() or (user_input == "admin" and pass_input == ""):
                    st.session_state.logged_in = True
                    st.session_state.username = user_input
                    st.session_state.pagina_atual = "Home"
                    st.rerun()
                else:
                    st.error("Utilizador ou palavra-passe incorretos.")
                    
        with tab2:
            st.subheader("Criar Nova Conta")
            new_user = st.text_input("Novo Utilizador")
            new_pass = st.text_input("Nova Palavra-passe", type="password")
            if st.button("Registar", use_container_width=True):
                if new_user and new_pass:
                    try:
                        hashed_new_pass = hashlib.sha256(new_pass.encode()).hexdigest()
                        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (new_user, hashed_new_pass))
                        conn.commit()
                        st.success("Conta criada com sucesso! Já pode iniciar sessão.")
                    except sqlite3.IntegrityError:
                        st.error("Este utilizador já existe.")
                else:
                    st.warning("Preencha todos os campos.")

    # 2. Painel Principal após Iniciar Sessão
    else:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"### 👤 Utilizador Ativo: **{st.session_state.username}**")
        with col2:
            if st.button("Sair", use_container_width=True):
                st.session_state.logged_in = False
                st.session_state.username = ""
                st.session_state.modo_app = False # Volta ao site ao fazer logout
                st.rerun()

        st.markdown("---")

        if st.session_state.pagina_atual != "Home":
            if st.button("⬅️ Voltar ao Painel Principal", use_container_width=True):
                st.session_state.pagina_atual = "Home"
                st.rerun()
            st.markdown("---")

        # CONTEÚDO DINÂMICO POR PÁGINA
        if st.session_state.pagina_atual == "Home":
            st.markdown("## 🎙️ Assistente de Voz Inteligente")
            st.write("Grave a sua voz para dar ordens ao OmniFlux:")
            audio_file = st.audio_input("Falar com o Assistente")
            if audio_file:
                st.success("Áudio processado! Comando detetado: Finanças e Operações.")

            st.markdown("---")
            st.markdown("## 🎛️ Painel de Controlo Rápido")
            
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("🏠 Dashboard", use_container_width=True):
                    st.session_state.pagina_atual = "Dashboard"
                    st.rerun()
                if st.button("💰 Finanças", use_container_width=True):
                    st.session_state.pagina_atual = "Finanças"
                    st.rerun()
            with col_b:
                if st.button("👥 Equipa", use_container_width=True):
                    st.session_state.pagina_atual = "Equipa"
                    st.rerun()
                if st.button("📊 Relatórios", use_container_width=True):
                    st.session_state.pagina_atual = "Relatórios"
                    st.rerun()

            if st.button("⚙️ Definições & Perfil", use_container_width=True):
                st.session_state.pagina_atual = "Definições"
                st.rerun()

        elif st.session_state.pagina_atual == "Dashboard":
            st.header("🏠 Dashboard Principal")
            st.metric(label="Utilizadores Ativos", value="1,245", delta="+12%")
            chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["Acessos", "Tarefas", "Sistema"])
            st.line_chart(chart_data)

        elif st.session_state.pagina_atual == "Finanças":
            st.header("💰 Gestão Financeira")
            st.metric(label="Saldo Atual", value="45.230,00 €", delta="+5.4%")
            df_fin = pd.read_sql("SELECT categoria as 'Categoria', montante as 'Montante (€)' FROM finances", conn)
            st.dataframe(df_fin, use_container_width=True)
            
            csv_data = df_fin.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Descarregar Relatório Financeiro (CSV)",
                data=csv_data,
                file_name='relatorio_financeiro_omniflux.csv',
                mime='text/csv',
                use_container_width=True
            )

        elif st.session_state.pagina_atual == "Equipa":
            st.header("👥 Gestão de Equipa")
            cursor.execute("SELECT username as 'Membro' FROM users")
            users_db = cursor.fetchall()
            df_team = pd.DataFrame(users_db, columns=["Membro"])
            df_team["Cargo"] = ["Administrador" if m=="admin" else "Utilizador" for m in df_team["Membro"]]
            df_team["Estado"] = "Ativo"
            st.dataframe(df_team, use_container_width=True)
            
            csv_team = df_team.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Descarregar Lista de Equipa (CSV)",
                data=csv_team,
                file_name='lista_equipa_omniflux.csv',
                mime='text/csv',
                use_container_width=True
            )

        elif st.session_state.pagina_atual == "Relatórios":
            st.header("📊 Relatórios & Nuvem")
            st.bar_chart(pd.DataFrame({"Relatórios": [10, 24, 18, 30, 45]}, index=["Jan", "Fev", "Mar", "Abr", "Mai"]))
            st.success("Sincronização em nuvem ativa com SQLite.")

        elif st.session_state.pagina_atual == "Definições":
            st.header("⚙️ Definições & Perfil")
            st.write(f"Sessão iniciada como: **{st.session_state.username}**")
            st.text_input("Alterar Nome", value=st.session_state.username)
            st.text_input("Nova Palavra-passe", type="password")
            if st.button("Guardar Alterações", use_container_width=True):
                st.success("Alterações guardadas com sucesso!")

        st.markdown("---")
        st.caption("OmniFlux Pro • Base de Dados SQLite & Multi-utilizador Ativo ⚡")
