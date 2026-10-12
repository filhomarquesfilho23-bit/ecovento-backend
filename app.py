import sqlite3
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Configuração da página do Streamlit (Layout largo e tema escuro simulado)
st.set_page_config(page_title="Vanguarda Engenharia & Obras S.A.", layout="wide")

# Estilo CSS personalizado para dar o aspeto executivo/dark
st.markdown("""
    <style>
    .main {
        background-color: #0d1117;
    }
    .metric-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        padding: 20px;
        border-radius: 10px;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Cabeçalho da Empresa
st.markdown("### 🟡 Vanguarda Engenharia & Obras S.A.")
st.caption("DASHBOARD EXECUTIVO & ANALYTICS")

# Linha de Métricas Principais (3 Colunas)
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div class="metric-card">
            <p style="color: #8b949e; margin-bottom: 5px; font-size: 14px;">Estado da Empresa</p>
            <h2 style="color: #58a6ff; margin-top: 0;">Operacional</h2>
            <p style="color: #2ea043; font-size: 12px; margin: 0;">● Todos os sistemas ativos</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="metric-card">
            <p style="color: #8b949e; margin-bottom: 5px; font-size: 14px;">Obras / Projetos Ativos</p>
            <h2 style="color: #d29922; margin-top: 0;">4 Projetos</h2>
            <p style="color: #8b949e; font-size: 12px; margin: 0;">Monitorização em tempo real</p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="metric-card">
            <p style="color: #8b949e; margin-bottom: 5px; font-size: 14px;">Eficiência Global</p>
            <h2 style="color: #3fb950; margin-top: 0;">96.4%</h2>
            <p style="color: #8b949e; font-size: 12px; margin: 0;">Performance operacional excelente</p>
        </div>
    """, unsafe_allow_html=True)

st.write("")
st.markdown("### 🏗️ Projetos e Parques em Execução")

# Grelha de Projetos (2 colunas x 2 linhas)
p_col1, p_col2 = st.columns(2)

with p_col1:
    st.image("https://images.unsplash.com/photo-1541888946425-d0fbb18f504d", caption="PROJETO 205 - Infraestrutura Viária Sul (Em Curso)", use_container_width=True)
    st.markdown("**Valor do Contrato:** €1.800.000")
    
    st.write("---")
    
    st.image("https://images.unsplash.com/photo-1503387762-592deb58ef4e", caption="PROJETO 207 - Edifício Corporate Center (Em Curso)", use_container_width=True)
    st.markdown("**Valor do Contrato:** €3.900.000")

with p_col2:
    st.image("https://images.unsplash.com/photo-1513694203232-719a280e022f", caption="PROJETO 206 - Residencial Vista Verde (Concluído)", use_container_width=True)
    st.markdown("**Valor do Contrato:** €2.200.000")
    
    st.write("---")
    
    st.image("https://images.unsplash.com/photo-1486406146926-c627a92ad1ab", caption="PROJETO 208 - Remodelação Hospitalar (Em Curso)", use_container_width=True)
    st.markdown("**Valor do Contrato:** €2.700.000")

st.write("")

# Botão de Sincronização Operacional
if st.button("✨ Sincronizar Estado Operacional", type="primary", use_container_width=True):
    st.success("Estado operacional sincronizado com sucesso com a base de dados central!")
