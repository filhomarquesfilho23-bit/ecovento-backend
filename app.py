import streamlit as st
import pandas as pd
from supabase import create_client, Client

# Configuração da página do Streamlit
st.set_page_config(page_title="Vanguarda ERP - Cloud Enterprise System", page_icon="🚀", layout="wide")

# Estilo visual moderno/executivo dark
st.markdown("""
    <style>
    .metric-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        padding: 20px;
        border-radius: 10px;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# --- CONEXÃO AO SUPABASE COM TRATAMENTO DE ERROS ---
@st.cache_resource
def init_connection():
    try:
        url = st.secrets["supabase"]["url"]
        key = st.secrets["supabase"]["key"]
        return create_client(url, key)
    except Exception as e:
        return None

supabase = init_connection()

if not supabase:
    st.error("⚠️ **Erro de Configuração:** Não foi possível estabelecer ligação ao Supabase.")
    st.markdown("Certifica-te de que guardaste as **Secrets** corretamente no painel do Streamlit Cloud com este formato:")
    st.code('''[supabase]
url = "https://ufgmuayietkuwsobjszx.supabase.co"
key = "sb_publishable_jpN4HMUb5OcuvL_EgzKLUW_uRf5B1t_"''', language="toml")
    st.stop()

# --- SISTEMA DE AUTENTICAÇÃO COM NÍVEIS DE ACESSO (RBAC) ---
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False
    st.session_state["utilizador"] = ""
    st.session_state["role"] = ""

if not st.session_state["autenticado"]:
    st.title("🔐 Vanguarda ERP - Portal de Autenticação na Nuvem")
    st.markdown("Insira as suas credenciais para aceder ao sistema de gestão centralizado.")

    with st.form("form_login"):
        user_input = st.text_input("Utilizador", value="admin")
        pass_input = st.text_input("Palavra-passe", type="password", value="")
        btn_login = st.form_submit_button("Entrar no Sistema")

        if btn_login:
            if user_input == "admin" and pass_input == "vanguarda2026":
                st.session_state["autenticado"] = True
                st.session_state["utilizador"] = "Administrador Geral"
                st.session_state["role"] = "Admin"
                st.success("Acesso autorizado como Administrador!")
                st.rerun()
            else:
                st.error("Credenciais inválidas.")
    st.stop()

# --- APLICAÇÃO PRINCIPAL (APÓS LOGIN) ---
st.title("🚀 Vanguarda ERP - Cloud Enterprise System")

# Barra de navegação simples
menu = st.sidebar.selectbox("Navegação", ["Dashboard & Projetos", "Mão de Obra", "Stock e Materiais"])

if menu == "Dashboard & Projetos":
    st.header("Painel Executivo e Obras em Curso (Supabase Cloud)")
    
    # Formulário para adicionar novo projeto
    with st.expander("✨ Adicionar Novo Projeto à Base de Dados"):
        with st.form("form_novo_projeto"):
            nome_projeto = st.text_input("Nome do Projeto / Obra")
            descricao_projeto = st.text_area("Descrição / Detalhes")
            btn_guardar = st.form_submit_button("Guardar no Supabase")
            
            if btn_guardar:
                if nome_projeto.strip() != "":
                    try:
                        dados = {
                            "name": nome_projeto,
                            "description": descricao_projeto
                        }
                        supabase.table("projects").insert(dados).execute()
                        st.success("Projeto guardado com sucesso!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erro ao inserir dados: {e}")
                else:
                    st.warning("O nome do projeto não pode estar vazio.")

    st.divider()

    # Listagem de projetos do Supabase
    st.subheader("📋 Lista de Projetos Registados")
    try:
        resposta = supabase.table("projects").select("*").order("id", desc=True).execute()
        projetos = resposta.data

        if projetos:
            for p in projetos:
                with st.container():
                    st.markdown(f"### 📌 {p.get('name')}")
                    st.write(f"**Descrição:** {p.get('description') if p.get('description') else 'Sem descrição'}")
                    st.caption(f"ID: {p.get('id')} | Criado em: {p.get('created_at')}")
                    st.markdown("---")
        else:
            st.info("Ainda não existem projetos registados na base de dados do Supabase.")
    except Exception as e:
        st.error(f"Erro ao carregar projetos: {e}")

elif menu == "Mão de Obra":
    st.header("Gestão de Mão de Obra e Equipas")
    st.info("Módulo em desenvolvimento.")

elif menu == "Stock e Materiais":
    st.header("Gestão de Stock e Materiais de Construção")
    st.info("Módulo em desenvolvimento.")
