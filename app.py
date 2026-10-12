import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# 1. Configuração da Página e Layout Executivo
st.set_page_config(
    page_title="Vanguarda ERP - Gestão de Obra",
    page_icon="🏗️",
    layout="wide"
)

# Estilização CSS personalizada (Dark Mode Profissional)
st.markdown("""
    <style>
    .main {
        background-color: #0f172a;
        color: #f8fafc;
    }
    .stMetric {
        background-color: #1e293b;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #475569;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🏗️ Vanguarda ERP - Sistema de Gestão de Obra")
st.markdown("Portal Executivo Integrado | Controlo de Mão de Obra e Stock")

# 2. Inicializar e carregar dados da Base de Dados Persistente automaticamente
@st.cache_data
def carregar_dados_erp():
    conexao = sqlite3.connect('vanguarda_erp.db')
    cursor = conexao.cursor()
    
    # Criar tabelas se não existirem
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mao_obra (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cargo TEXT NOT NULL,
            quantidade INTEGER,
            custo_diario REAL,
            dias INTEGER,
            custo_mensal REAL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stock (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            material TEXT NOT NULL,
            quantidade_atual INTEGER,
            stock_minimo INTEGER,
            preco_unit REAL,
            valor_total REAL
        )
    ''')
    
    # Inserir dados padrão se as tabelas estiverem vazias
    cursor.execute("SELECT COUNT(*) FROM mao_obra")
    if cursor.fetchone()[0] == 0:
        equipa = [
            ("Encarregado de Obra", 1, 120.0, 22, 2640.0),
            ("Pedreiro Especializado", 8, 90.0, 22, 15840.0),
            ("Servente / Ajudante", 6, 55.0, 22, 7260.0),
            ("Gruista", 1, 95.0, 22, 2090.0)
        ]
        cursor.executemany("INSERT INTO mao_obra (cargo, quantidade, custo_diario, dias, custo_mensal) VALUES (?, ?, ?, ?, ?)", equipa)

    cursor.execute("SELECT COUNT(*) FROM stock")
    if cursor.fetchone()[0] == 0:
        materiais = [
            ("Cimento Portland", 40, 50, 7.50, 300.0),
            ("Aço A500NR", 15, 30, 1.20, 18.0),
            ("Tijolo Cerâmico", 3200, 1000, 0.45, 1440.0),
            ("Tinta Plástica", 8, 15, 25.00, 200.0),
            ("Areia Grossa", 120, 50, 18.00, 2160.0)
        ]
        cursor.executemany("INSERT INTO stock (material, quantidade_atual, stock_minimo, preco_unit, valor_total) VALUES (?, ?, ?, ?, ?)", materiais)
        
    conexao.commit()

    df_mao = pd.read_sql("SELECT * FROM mao_obra", conexao)
    df_stock = pd.read_sql("SELECT * FROM stock", conexao)
    conexao.close()
    return df_mao, df_stock

df_mao_obra, df_stock = carregar_dados_erp()

# 3. Cálculos de Indicadores Globais
total_mao = df_mao_obra['custo_mensal'].sum()
total_stock = df_stock['valor_total'].sum()
orcamento_global = total_mao + total_stock

# 4. Painel Superior de Métricas (KPIs)
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Orçamento Global", value=f"{orcamento_global:,.2f} EUR")
with col2:
    st.metric(label="Custo Total Mão de Obra", value=f"{total_mao:,.2f} EUR")
with col3:
    st.metric(label="Valor Total em Stock", value=f"{total_stock:,.2f} EUR")

st.divider()

# 5. Abas de Navegação do ERP
aba1, aba2, aba3 = st.tabs(["📊 Dashboard Executivo", "👷 Recursos Humanos", "📦 Inventário de Stock"])

with aba1:
    st.subheader("Análise Visual Consolidada")
    
    col_g1, col_g2 = st.columns(2)
    
    with col_g1:
        st.write("**Custos Mensais de Mão de Obra**")
        fig, ax = plt.subplots(figsize=(6, 4))
        fig.patch.set_facecolor('#0f172a')
        ax.set_facecolor('#1e293b')
        ax.bar(df_mao_obra['cargo'], df_mao_obra['custo_mensal'], color='#ef4444', width=0.6)
        ax.tick_params(axis='x', rotation=20, colors='#e2e8f0', labelsize=8)
        ax.tick_params(axis='y', colors='#e2e8f0')
        for spine in ax.spines.values():
            spine.set_color('#475569')
        st.pyplot(fig)
        
    with col_g2:
        st.write("**Valor Imobilizado por Material**")
        fig, ax = plt.subplots(figsize=(6, 4))
        fig.patch.set_facecolor('#0f172a')
        ax.set_facecolor('#1e293b')
        ax.bar(df_stock['material'], df_stock['valor_total'], color='#10b981', width=0.6)
        ax.tick_params(axis='x', rotation=20, colors='#e2e8f0', labelsize=8)
        ax.tick_params(axis='y', colors='#e2e8f0')
        for spine in ax.spines.values():
            spine.set_color('#475569')
        st.pyplot(fig)

with aba2:
    st.subheader("Tabela Oficial de Mão de Obra")
    st.dataframe(df_mao_obra, use_container_width=True)

with aba3:
    st.subheader("Tabela Oficial de Stock e Materiais")
    st.dataframe(df_stock, use_container_width=True)
