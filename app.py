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

# 2. Função para carregar os dados diretamente da Base de Dados Persistente
@st.cache_data
def carregar_dados_erp():
    conexao = sqlite3.connect('vanguarda_erp.db')
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
