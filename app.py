import streamlit as st
import pandas as pd
import numpy as np

# Configuração da página
st.set_page_config(page_title="OmniFlux Pro", page_icon="⚡", layout="centered")

# Estilo CSS Personalizado: Botão de Login Preto e restantes botões/elementos em Azul
st.markdown("""
    <style>
    /* Estilo padrão para os botões do painel (Azul) */
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
    
    /* Forçar especificamente o botão "Entrar no Sistema" a ficar Preto */
    div.stButton > button:has-text("Entrar no Sistema") {
        background-color: #111111 !important;
        color: #ffffff !important;
        border: 2px solid #444444 !important;
    }
    div.stButton > button:has-text("Entrar no Sistema"):hover {
        background-color: #222222 !important;
        border-color: #00bfff !important;
    }

    /* Cor para as métricas */
    [data-testid="stMetricValue"] {
        color: #00bfff !important;
    }
    </style>
""", unsafe_allow_html=True)

# Inicializar o estado da sessão
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

if "pagina_atual" not in st.session_state:
    st.session_state.pagina_atual = "Home"

# 1. Ecrã de Início de Sessão (Login)
if not st.session_state.logged_in:
    st.title("⚡ OmniFlux Pro")
    st.markdown("Sistema Operativo Líquido • Segurança & Controlo Multi-utilizador.")
    
    tab1, tab2 = st.tabs(["🔑 Iniciar Sessão", "📄 Criar Conta"])
    
    with tab1:
        st.subheader("Iniciar Sessão")
        user_input = st.text_input("Utilizador", value="admin")
        pass_input = st.text_input("Palavra-passe", type="password")
        
        if st.button("Entrar no Sistema", use_container_width=True):
            if user_input == "admin":
                st.session_state.logged_in = True
                st.session_state.username = user_input
                st.session_state.pagina_atual = "Home"
                st.rerun()
            else:
                st.error("Utilizador ou palavra-passe incorretos.")
                
    with tab2:
        st.subheader("Criar Nova Conta")
        st.text_input("Novo Utilizador")
        st.text_input("Nova Palavra-passe", type="password")
        st.button("Registar", use_container_width=True)

# 2. Painel Principal após Iniciar Sessão
else:
    # Cabeçalho e Botão Sair
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"### 👤 Utilizador Ativo: **{st.session_state.username}**")
    with col2:
        if st.button("Sair", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.pagina_atual = "Home"
            st.rerun()

    st.markdown("---")

    # Botão para voltar ao menu principal se estiver numa subpágina
    if st.session_state.pagina_atual != "Home":
        if st.button("⬅️ Voltar ao Painel Principal", use_container_width=True):
            st.session_state.pagina_atual = "Home"
            st.rerun()
        st.markdown("---")

    # CONTEÚDO DINÂMICO CONSOANTE A PÁGINA ATIVA
    if st.session_state.pagina_atual == "Home":
        
        # Secção: Assistente de Voz Inteligente
        st.markdown("## 🎙️ Assistente de Voz Inteligente")
        if st.button("🎤 Tocar para Falar com o OmniFlux", use_container_width=True):
            st.success("Comando detetado: Finanças e equipe")
        st.caption("Diga um comando (ex: finanças, equipa, tarefas, relatórios)...")

        st.markdown("---")

        # Secção: Painel de Controlo Rápido
        st.markdown("## 🎛️ Painel de Controlo Rápido")
        
        if st.button("🏠 Dashboard", use_container_width=True):
            st.session_state.pagina_atual = "Dashboard"
            st.rerun()
            
        if st.button("💰 Finanças", use_container_width=True):
            st.session_state.pagina_atual = "Finanças"
            st.rerun()
            
        if st.button("👥 Equipa", use_container_width=True):
            st.session_state.pagina_atual = "Equipa"
            st.rerun()
            
        if st.button("📊 Relatórios & Nuvem", use_container_width=True):
            st.session_state.pagina_atual = "Relatórios"
            st.rerun()

    elif st.session_state.pagina_atual == "Dashboard":
        st.header("🏠 Dashboard Principal")
        st.write("Métricas de desempenho em tempo real e evolução do sistema.")
        st.metric(label="Utilizadores Ativos", value="1,245", delta="+12%")
        
        # Gráfico dinâmico de exemplo
        chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["Acessos", "Tarefas", "Sistema"])
        st.line_chart(chart_data)

    elif st.session_state.pagina_atual == "Finanças":
        st.header("💰 Gestão Financeira")
        st.write("Consulte os saldos, faturas recentes, receitas e despesas da empresa.")
        st.metric(label="Saldo Atual", value="45.230,00 €", delta="+5.4%")
        
        # Tabela financeira detalhada
        df_fin = pd.DataFrame({
            "Categoria": ["Receitas", "Despesas", "Investimentos", "Manutenção"],
            "Montante (€)": [32000, 12500, 8000, 2500]
        })
        st.dataframe(df_fin, use_container_width=True)

    elif st.session_state.pagina_atual == "Equipa":
        st.header("👥 Gestão de Equipa")
        st.write("Lista de membros e permissões de acesso ativas.")
        
        df_team = pd.DataFrame({
            "Membro": ["Admin Principal", "João Silva", "Ana Souza", "Carlos Mendes"],
            "Cargo": ["Administrador", "Gestor de Contas", "Suporte Técnico", "Desenvolvedor"],
            "Estado": ["Ativo", "Ativo", "Ausente", "Ativo"]
        })
        st.dataframe(df_team, use_container_width=True)

    elif st.session_state.pagina_atual == "Relatórios":
        st.header("📊 Relatórios & Nuvem")
        st.write("Aceda aos relatórios gerados automaticamente e aos ficheiros sincronizados na nuvem.")
        
        st.bar_chart(pd.DataFrame({"Relatórios Gerados": [10, 24, 18, 30, 45]}, index=["Jan", "Fev", "Mar", "Abr", "Mai"]))
        st.success("Sincronização com a nuvem concluída com sucesso.")

    st.markdown("---")
    st.caption("OmniFlux Pro • Multi-utilizador Ativo ⚡")
