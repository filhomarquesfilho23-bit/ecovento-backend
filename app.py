import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import base64
from supabase import create_client, Client

# Configuração da página do Streamlit
st.set_page_config(page_title="Vanguarda Engenharia & Obras S.A.", layout="wide", page_icon="🏗️")

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

# --- CONEXÃO AO SUPABASE ---
@st.cache_resource
def init_connection():
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)

supabase: Client = init_connection()

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
        pass_input = st.text_input("Palavra-passe", type="password", value="vanguarda2026")
        btn_login = st.form_submit_button("Entrar no Sistema")
        
        if btn_login:
            if user_input == "admin" and pass_input == "vanguarda2026":
                st.session_state["autenticado"] = True
                st.session_state["utilizador"] = "Administrador Geral"
                st.session_state["role"] = "Admin"
                st.success("Acesso autorizado como Administrador!")
                st.rerun()
            elif user_input == "diretor" and pass_input == "obra2026":
                st.session_state["autenticado"] = True
                st.session_state["utilizador"] = "Diretor de Obra"
                st.session_state["role"] = "Diretor"
                st.success("Acesso autorizado como Diretor de Obra!")
                st.rerun()
            elif user_input == "cliente" and pass_input == "cliente2026":
                st.session_state["autenticado"] = True
                st.session_state["utilizador"] = "Cliente / Consultor"
                st.session_state["role"] = "Cliente"
                st.success("Acesso autorizado em modo de Consulta!")
                st.rerun()
            else:
                st.error("Credenciais inválidas.")
    st.stop()

st.title("🚀 Vanguarda ERP - Cloud Enterprise System")

# --- BARRA LATERAL COM PERFIL E FILTROS ---
with st.sidebar:
    st.write(f"👤 **Utilizador:** {st.session_state['utilizador']}")
    st.write(f"🛡️ **Perfil:** {st.session_state['role']}")
    st.divider()
    
    st.markdown("### 🔍 Filtros Avançados")
    filtro_status = st.selectbox("Filtrar Projetos por Estado", ["Todos", "Em Curso", "Concluído", "Planeamento"])
    
    st.divider()
    if st.button("Terminar Sessão", type="secondary"):
        st.session_state["autenticado"] = False
        st.rerun()

# --- NAVEGAÇÃO POR ABAS ---
tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard & Projetos", "👥 Mão de Obra", "📦 Stock e Materiais", "💰 Financeiro"])

# ================= TAB 1: DASHBOARD & PROJETOS =================
with tab1:
    st.subheader("Painel Executivo e Obras em Curso (Supabase Cloud)")
    
    response_proj = supabase.table("projetos").select("*").execute()
    df_proj = pd.DataFrame(response_proj.data)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Estado da Empresa", "Operacional", "Nuvem Sincronizada")
    with c2:
        total_p = len(df_proj) if not df_proj.empty else 0
        st.metric("Obras / Projetos Ativos", f"{total_p} Projetos", "Tempo real")
    with c3:
        st.metric("Eficiência Global", "96.4%", "+1.2% este mês")
        
    st.divider()

    if not df_proj.empty:
        if filtro_status != "Todos":
            df_proj_filtrado = df_proj[df_proj['status'] == filtro_status]
        else:
            df_proj_filtrado = df_proj

        if not df_proj_filtrado.empty:
            st.markdown(f"### 📈 Gráfico: Contratos de Obras ({filtro_status})")
            fig_proj, ax_proj = plt.subplots(figsize=(10, 4))
            ax_proj.barh(df_proj_filtrado['nome'], df_proj_filtrado['valor'] / 1000000, color='#3498db')
            ax_proj.set_xlabel('Valor do Contrato (Milhões de EUR)')
            ax_proj.set_title('Comparativo de Contratos na Nuvem')
            ax_proj.grid(axis='x', linestyle='--', alpha=0.7)
            plt.tight_layout()
            st.pyplot(fig_proj)
            st.divider()

    if st.session_state["role"] in ["Admin", "Diretor"]:
        st.markdown("### 🏗️ Gestão e Registo de Novos Projetos")
        with st.expander("➕ Registar Novo Projeto na Nuvem"):
            with st.form("form_novo_proj", clear_on_submit=True):
                f_nome = st.text_input("Nome/Código do Projeto", value="Projeto 209 - Centro Logístico")
                f_status = st.selectbox("Estado", ["Em Curso", "Concluído", "Planeamento"])
                f_valor = st.number_input("Valor do Contrato (EUR)", min_value=10000.0, value=1500000.0, step=50000.0)
                f_img = st.text_input("URL da Nova Fotografia", value="https://images.unsplash.com/photo-1503387762-592deb58ef4e")
                
                if st.form_submit_button("Guardar Projeto no Supabase"):
                    if not f_nome.strip():
                        st.warning("Insira um nome válido.")
                    else:
                        supabase.table("projetos").insert({
                            "nome": f_nome,
                            "status": f_status,
                            "valor": f_valor,
                            "imagem": f_img
                        }).execute()
                        st.success("Projeto guardado na nuvem com sucesso!")
                        st.rerun()

    if not df_proj.empty:
        g_cols = st.columns(2)
        for idx, row in df_proj.iterrows():
            with g_cols[idx % 2]:
                st.image(row['imagem'], caption=f"{row['nome']} ({row['status']})", use_container_width=True)
                st.markdown(f"**Valor do Contrato:** €{row['valor']:,.2f}")
                st.write("---")
        
        csv_proj = df_proj.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Descarregar Relatório de Projetos (CSV)", csv_proj, "projetos_vanguarda.csv", "text/csv")

# ================= TAB 2: MÃO DE OBRA =================
with tab2:
    st.subheader("👥 Gestão de Mão de Obra e Equipa")
    
    response_mo = supabase.table("mao_obra").select("*").execute()
    df_mo = pd.DataFrame(response_mo.data)

    if not df_mo.empty:
        st.markdown("### 📈 Gráfico: Custo Mensal por Trabalhador")
        fig_mo, ax_mo = plt.subplots(figsize=(10, 4))
        labels_mo = df_mo['nome'].astype(str) + " - " + df_mo['cargo'].astype(str)
        ax_mo.bar(labels_mo, df_mo['custo_mensal'], color='#e67e22')
        ax_mo.set_ylabel('Custo Mensal (EUR)')
        ax_mo.set_title('Despesa com Mão de Obra')
        plt.xticks(rotation=15, ha='right')
        ax_mo.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        st.pyplot(fig_mo)
        st.divider()

    if st.session_state["role"] in ["Admin", "Diretor"]:
        with st.expander("➕ Registar Novo Trabalhador"):
            with st.form("form_trabalhador", clear_on_submit=True):
                c1, c2 = st.columns(2)
                with c1:
                    nome = st.text_input("Nome", value="Manuel Ribeiro")
                    idade = st.number_input("Idade", min_value=18, max_value=70, value=32)
                    cargo = st.text_input("Cargo", value="Engenheiro Civil")
                with c2:
                    qtd = st.number_input("Quantidade", value=1)
                    custo_d = st.number_input("Custo Diário (EUR)", value=90.0)
                    dias = st.number_input("Dias Mensais", value=22)
                    
                if st.form_submit_button("Guardar Trabalhador"):
                    custo_m = qtd * custo_d * dias
                    supabase.table("mao_obra").insert({
                        "nome": nome, "idade": idade, "cargo": cargo,
                        "quantidade": qtd, "custo_diario": custo_d,
                        "dias": dias, "custo_mensal": custo_m
                    }).execute()
                    st.success("Trabalhador registado na nuvem!")
                    st.rerun()
                
    st.dataframe(df_mo, use_container_width=True)
    
    if not df_mo.empty:
        csv_mo = df_mo.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Descarregar Relatório de Mão de Obra (CSV)", csv_mo, "mao_de_obra_vanguarda.csv", "text/csv")

# ================= TAB 3: STOCK E MATERIAIS =================
with tab3:
    st.subheader("📦 Gestão de Stock e Armazém")
    
    response_st = supabase.table("stock_materiais").select("*").execute()
    df_st = pd.DataFrame(response_st.data)

    if not df_st.empty:
        st.markdown("### 📈 Gráfico: Custo Total por Material em Stock")
        fig_st, ax_st = plt.subplots(figsize=(10, 4))
        ax_st.bar(df_st['material'], df_st['custo_total'], color='#9b59b6')
        ax_st.set_ylabel('Custo Total (EUR)')
        ax_st.set_title('Investimento em Materiais de Armazém')
        ax_st.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        st.pyplot(fig_st)
        st.divider()

    if st.session_state["role"] in ["Admin", "Diretor"]:
        with st.expander("➕ Registar Material"):
            with st.form("form_stock", clear_on_submit=True):
                mat = st.text_input("Material", value="Cabo de Cobre 16mm")
                q_mat = st.number_input("Quantidade", value=100)
                uni = st.text_input("Unidade", value="Metros")
                p_uni = st.number_input("Preço Unitário (EUR)", value=6.50)
                
                if st.form_submit_button("Guardar Material"):
                    c_tot = q_mat * p_uni
                    supabase.table("stock_materiais").insert({
                        "material": mat, "quantidade": q_mat,
                        "unidade": uni, "preco_unitario": p_uni,
                        "custo_total": c_tot
                    }).execute()
                    st.success("Material adicionado ao stock na nuvem!")
                    st.rerun()
                
    st.dataframe(df_st, use_container_width=True)
    
    if not df_st.empty:
        csv_st = df_st.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Descarregar Relatório de Stock (CSV)", csv_st, "stock_vanguarda.csv", "text/csv")

# ================= TAB 4: FINANCEIRO =================
with tab4:
    st.subheader("📊 Painel Financeiro & Fluxo de Caixa")
    
    response_fl = supabase.table("fluxo_caixa").select("*").execute()
    df_fl = pd.DataFrame(response_fl.data)

    if not df_fl.empty:
        st.markdown("### 📈 Gráfico: Evolução Mensal de Entradas vs Saídas")
        fig, ax = plt.subplots(figsize=(10, 4))
        meses = df_fl['mes'].tolist()
        entradas = df_fl['entradas'].tolist()
        saidas = df_fl['saidas'].tolist()
        
        x = np.arange(len(meses))
        width = 0.35

        ax.bar(x - width/2, entradas, width, label='Entradas', color='#2ecc71')
        ax.bar(x + width/2, saidas, width, label='Saídas', color='#e74c3c')

        ax.set_xticks(x)
        ax.set_xticklabels(meses)
        ax.set_title('Fluxo de Caixa Consolidado (Supabase)')
        ax.legend(fontsize=8)
        ax.grid(axis='y', linestyle='--', alpha=0.7)

        plt.tight_layout()
        st.pyplot(fig)
        
        csv_fl = df_fl.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Descarregar Relatório Financeiro (CSV)", csv_fl, "financeiro_vanguarda.csv", "text/csv")

    st.divider()
    st.markdown("### 📄 Geração de Relatório Executivo Consolidado")
    
    if st.button("Gerar Relatório HTML Consolidado"):
        html_report = f"""
        <html>
        <head><title>Relatório Vanguarda ERP</title></head>
        <body style="font-family: Arial; background-color: #0d1117; color: white; padding: 20px;">
            <h1>Vanguarda Engenharia & Obras S.A.</h1>
            <h3>Relatório Executivo Cloud - Gerado por {st.session_state['utilizador']}</h3>
            <hr>
            <h4>Resumo Operacional</h4>
            <p>Estado da Empresa: <b>Operacional (Sincronizado na Nuvem)</b></p>
            <p>Eficiência Global: <b>96.4%</b></p>
            <hr>
            <h4>Projetos Ativos no Supabase</h4>
            {df_proj.to_html(index=False) if not df_proj.empty else "Sem dados"}
        </body>
        </html>
        """
        b64 = base64.b64encode(html_report.encode()).decode()
        href = f'<a href="data:text/html;base64,{b64}" download="Relatorio_Cloud_Vanguarda.html" target="_blank">📥 Clique aqui para descarregar o Relatório em HTML</a>'
        st.markdown(href, unsafe_allow_html=True)
