import sqlite3
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Configuração da página do Streamlit
st.set_page_config(page_title="Vanguarda Engenharia & Obras S.A.", layout="wide")

# Estilo visual moderno/executivo
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

# --- SISTEMA DE AUTENTICAÇÃO (LOGIN) ---
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

if not st.session_state["autenticado"]:
    st.title("🔐 Vanguarda ERP - Autenticação Segura")
    st.markdown("Insira as credenciais de acesso executivo para entrar no sistema.")
    
    with st.form("form_login"):
        user = st.text_input("Utilizador", value="admin")
        password = st.text_input("Palavra-passe", type="password", value="vanguarda2026")
        btn_login = st.form_submit_button("Entrar no Sistema")
        
        if btn_login:
            if user == "admin" and password == "vanguarda2026":
                st.session_state["autenticado"] = True
                st.success("Acesso autorizado! A carregar dashboard...")
                st.rerun()
            else:
                st.error("Credenciais inválidas. Utilize: Utilizador 'admin' e Palavra-passe 'vanguarda2026'.")
    st.stop()

# --- 1. INICIALIZAÇÃO DA BASE DE DADOS SQLITE (Versão 3 Limpa) ---
DB_NAME = 'vanguarda_erp_v3.db'

def inicializar_bd():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Tabelas
    cursor.execute('''CREATE TABLE IF NOT EXISTS fluxo_caixa (id INTEGER PRIMARY KEY AUTOINCREMENT, mes TEXT, entradas REAL, saidas REAL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS mao_obra (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, idade INTEGER, cargo TEXT, quantidade INTEGER, custo_diario REAL, dias INTEGER, custo_mensal REAL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS stock_materiais (id INTEGER PRIMARY KEY AUTOINCREMENT, material TEXT, quantidade INTEGER, unidade TEXT, preco_unitario REAL, custo_total REAL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS projetos (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, status TEXT, valor REAL, imagem TEXT)''')
    
    # Dados de Exemplo - Fluxo de Caixa
    cursor.execute("SELECT COUNT(*) FROM fluxo_caixa")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("INSERT INTO fluxo_caixa (mes, entradas, saidas) VALUES (?, ?, ?)", [
            ('Maio', 45000, 38000), ('Junho', 62000, 50000), ('Julho', 58000, 48000),
            ('Agosto', 70000, 60000), ('Setembro', 75000, 65000), ('Outubro', 80000, 70000)
        ])
        conn.commit()

    # Dados de Exemplo - Projetos com Fotos Únicas e Sem Repetições
    cursor.execute("SELECT COUNT(*) FROM projetos")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("INSERT INTO projetos (nome, status, valor, imagem) VALUES (?, ?, ?, ?)", [
            ("Projeto 205 - Infraestrutura Rodoviária", "Em Curso", 1800000.0, "https://images.unsplash.com/photo-1545677317-eb61803459eb"),
            ("Projeto 206 - Residencial Vista Verde", "Concluído", 2200000.0, "https://images.unsplash.com/photo-1512917774080-9991f1c4c750"),
            ("Projeto 207 - Edifício Corporate Center", "Em Curso", 3900000.0, "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab"),
            ("Projeto 208 - Remodelação Hospitalar", "Em Curso", 2700000.0, "https://images.unsplash.com/photo-1587351021759-3e566b6af7cc")
        ])
        conn.commit()

    # Dados de Exemplo - Mão de Obra
    cursor.execute("SELECT COUNT(*) FROM mao_obra")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("INSERT INTO mao_obra (nome, idade, cargo, quantidade, custo_diario, dias, custo_mensal) VALUES (?, ?, ?, ?, ?, ?, ?)", [
            ("Carlos Silva", 35, "Eletricista", 2, 80.0, 22, 3520.0),
            ("António Santos", 42, "Encarregado", 1, 110.0, 22, 2420.0),
            ("Manuel Ribeiro", 28, "Técnico", 3, 75.0, 22, 4950.0)
        ])
        conn.commit()

    # Dados de Exemplo - Stock
    cursor.execute("SELECT COUNT(*) FROM stock_materiais")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("INSERT INTO stock_materiais (material, quantidade, unidade, preco_unitario, custo_total) VALUES (?, ?, ?, ?, ?)", [
            ("Cabo de Cobre 16mm", 150, "Metros", 6.50, 975.0),
            ("Tubagem PVC 50mm", 80, "Un", 12.00, 960.0),
            ("Sacos de Cimento 50kg", 200, "Sacos", 5.50, 1100.0)
        ])
        conn.commit()
        
    conn.close()

inicializar_bd()

st.title("🚀 Vanguarda ERP - Gestão Integrada & Dashboard Executivo")

with st.sidebar:
    st.write("👤 **Sessão Ativa:** Administrador")
    if st.button("Terminar Sessão"):
        st.session_state["autenticado"] = False
        st.rerun()

# --- 2. NAVEGAÇÃO POR ABAS ---
tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard & Projetos", "👥 Mão de Obra", "📦 Stock e Materiais", "💰 Financeiro"])

# ================= TAB 1: DASHBOARD & PROJETOS =================
with tab1:
    st.subheader("Painel Executivo e Obras em Curso")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Estado da Empresa", "Operacional", "100% Ativo")
    with c2:
        conn = sqlite3.connect(DB_NAME)
        total_p = pd.read_sql("SELECT COUNT(*) as t FROM projetos", conn).iloc[0]['t']
        conn.close()
        st.metric("Obras / Projetos Ativos", f"{total_p} Projetos", "Monitorização em tempo real")
    with c3:
        st.metric("Eficiência Global", "96.4%", "+1.2% este mês")
        
    st.divider()

    # Gráfico de Valores dos Projetos
    conn = sqlite3.connect(DB_NAME)
    df_proj = pd.read_sql("SELECT * FROM projetos", conn)
    conn.close()

    if not df_proj.empty:
        st.markdown("### 📈 Gráfico: Distribuição de Valores por Contrato de Obra")
        fig_proj, ax_proj = plt.subplots(figsize=(10, 4))
        ax_proj.barh(df_proj['nome'], df_proj['valor'] / 1000000, color='#3498db')
        ax_proj.set_xlabel('Valor do Contrato (Milhões de EUR)')
        ax_proj.set_title('Comparativo de Contratos de Engenharia')
        ax_proj.grid(axis='x', linestyle='--', alpha=0.7)
        plt.tight_layout()
        st.pyplot(fig_proj)
        st.divider()

    # Layout Duplo: Código do lado esquerdo, Projeto do lado direito
    st.markdown("### 💻 Visualização Dupla (Lógica SQLite vs Projeto Renderizado)")
    col_codigo, col_projeto = st.columns(2)
    
    with col_codigo:
        st.markdown("**Código Fonte de Gestão (SQLite Backend):**")
        st.code("""
def guardar_projeto_db(nome, status, valor, img):
    conn = sqlite3.connect('vanguarda_erp_v3.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO projetos (nome, status, valor, imagem) VALUES (?, ?, ?, ?)",
        (nome, status, valor, img)
    )
    conn.commit()
    conn.close()
        """, language="python")
        st.caption("O código acima gere a persistência dos dados diretamente na base de dados SQLite.")
        
    with col_projeto:
        st.markdown("**Projeto em Destaque (Frontend Streamlit):**")
        st.image("https://images.unsplash.com/photo-1545677317-eb61803459eb", caption="Projeto Principal - Infraestrutura Rodoviária", use_container_width=True)
        st.markdown("**Estado:** Em Curso | **Contrato:** €1.800.000")

    st.divider()
    st.markdown("### 🏗️ Gestão e Registo de Novos Projetos")
    
    with st.expander("➕ Registar Novo Projeto"):
        with st.form("form_novo_proj", clear_on_submit=True):
            f_nome = st.text_input("Nome/Código do Projeto", value="Projeto 209 - Centro Logístico")
            f_status = st.selectbox("Estado", ["Em Curso", "Concluído", "Planeamento"])
            f_valor = st.number_input("Valor do Contrato (EUR)", min_value=10000.0, value=1500000.0, step=50000.0)
            f_img = st.text_input("URL da Nova Fotografia", value="https://images.unsplash.com/photo-1503387762-592deb58ef4e")
            
            if st.form_submit_button("Guardar Projeto na Base de Dados"):
                if not f_nome.strip():
                    st.warning("Insira um nome válido.")
                else:
                    conn = sqlite3.connect(DB_NAME)
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO projetos (nome, status, valor, imagem) VALUES (?, ?, ?, ?)", (f_nome, f_status, f_valor, f_img))
                    conn.commit()
                    conn.close()
                    st.success("Projeto guardado com sucesso!")
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
    
    conn = sqlite3.connect(DB_NAME)
    df_mo = pd.read_sql("SELECT * FROM mao_obra", conn)
    conn.close()

    if not df_mo.empty:
        st.markdown("### 📈 Gráfico: Custo Mensal por Trabalhador")
        fig_mo, ax_mo = plt.subplots(figsize=(10, 4))
        # Corrigido para evitar erro de coluna
        labels_mo = df_mo['nome'].astype(str) + " - " + df_mo['cargo'].astype(str)
        ax_mo.bar(labels_mo, df_mo['custo_mensal'], color='#e67e22')
        ax_mo.set_ylabel('Custo Mensal (EUR)')
        ax_mo.set_title('Despesa com Mão de Obra')
        plt.xticks(rotation=15, ha='right')
        ax_mo.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        st.pyplot(fig_mo)
        st.divider()

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
                conn = sqlite3.connect(DB_NAME)
                c = conn.cursor()
                c.execute("INSERT INTO mao_obra (nome, idade, cargo, quantidade, custo_diario, dias, custo_mensal) VALUES (?, ?, ?, ?, ?, ?, ?)",
                          (nome, idade, cargo, qtd, custo_d, dias, custo_m))
                conn.commit()
                conn.close()
                st.success("Trabalhador registado!")
                st.rerun()
                
    st.dataframe(df_mo, use_container_width=True)
    
    if not df_mo.empty:
        csv_mo = df_mo.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Descarregar Relatório de Mão de Obra (CSV)", csv_mo, "mao_de_obra_vanguarda.csv", "text/csv")

# ================= TAB 3: STOCK E MATERIAIS =================
with tab3:
    st.subheader("📦 Gestão de Stock e Armazém")
    
    conn = sqlite3.connect(DB_NAME)
    df_st = pd.read_sql("SELECT * FROM stock_materiais", conn)
    conn.close()

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

    with st.expander("➕ Registar Material"):
        with st.form("form_stock", clear_on_submit=True):
            mat = st.text_input("Material", value="Cabo de Cobre 16mm")
            q_mat = st.number_input("Quantidade", value=100)
            uni = st.text_input("Unidade", value="Metros")
            p_uni = st.number_input("Preço Unitário (EUR)", value=6.50)
            
            if st.form_submit_button("Guardar Material"):
                c_tot = q_mat * p_uni
                conn = sqlite3.connect(DB_NAME)
                c = conn.cursor()
                c.execute("INSERT INTO stock_materiais (material, quantidade, unidade, preco_unitario, custo_total) VALUES (?, ?, ?, ?, ?)",
                          (mat, q_mat, uni, p_uni, c_tot))
                conn.commit()
                conn.close()
                st.success("Material adicionado ao stock!")
                st.rerun()
                
    st.dataframe(df_st, use_container_width=True)
    
    if not df_st.empty:
        csv_st = df_st.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Descarregar Relatório de Stock (CSV)", csv_st, "stock_vanguarda.csv", "text/csv")

# ================= TAB 4: FINANCEIRO =================
with tab4:
    st.subheader("📊 Painel Financeiro & Fluxo de Caixa")
    conn = sqlite3.connect(DB_NAME)
    df_fl = pd.read_sql("SELECT mes, entradas, saidas FROM fluxo_caixa", conn)
    conn.close()

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
        ax.set_title('Fluxo de Caixa Consolidado')
        ax.legend(fontsize=8)
        ax.grid(axis='y', linestyle='--', alpha=0.7)

        plt.tight_layout()
        st.pyplot(fig)
        
        csv_fl = df_fl.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Descarregar Relatório Financeiro (CSV)", csv_fl, "financeiro_vanguarda.csv", "text/csv")
