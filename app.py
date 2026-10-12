import sqlite3
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Configuração da página do Streamlit
st.set_page_config(page_title="Vanguarda ERP", layout="wide")

st.title("🚀 Vanguarda ERP - Gestão e Painel Financeiro")

# 1. Função para inicializar a Base de Dados SQLite
def inicializar_bd():
    conn = sqlite3.connect('vanguarda_erp.db')
    cursor = conn.cursor()
    
    # Tabela de Fluxo de Caixa
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fluxo_caixa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mes TEXT,
            entradas REAL,
            saidas REAL
        )
    ''')
    
    # Tabela de Mão de Obra
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mao_obra (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cargo TEXT,
            quantidade INTEGER,
            custo_diario REAL,
            dias INTEGER,
            custo_mensal REAL
        )
    ''')
    
    # Inserir dados de exemplo no fluxo de caixa se estiver vazio
    cursor.execute("SELECT COUNT(*) FROM fluxo_caixa")
    if cursor.fetchone()[0] == 0:
        dados_iniciais = [
            ('Maio', 45000, 38000),
            ('Junho', 62000, 50000),
            ('Julho', 58000, 48000),
            ('Agosto', 70000, 60000),
            ('Setembro', 75000, 65000),
            ('Outubro', 80000, 70000)
        ]
        cursor.executemany("INSERT INTO fluxo_caixa (mes, entradas, saidas) VALUES (?, ?, ?)", dados_iniciais)
        conn.commit()
        
    conn.close()

# Executar a inicialização
inicializar_bd()

# --- SECÇÃO 1: FORMULÁRIO PARA REGISTAR NOVO TRABALHADOR ---
with st.expander("➕ Registar Novo Trabalhador / Cargo"):
    with st.form("form_novo_trabalhador", clear_on_submit=True):
        st.write("Insira os dados do novo elemento da equipa:")
        
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            novo_cargo = st.text_input("Cargo ou Função")
            nova_qtd = st.number_input("Quantidade", min_value=1, value=1, step=1)
            novo_custo_diario = st.number_input("Custo Diário (EUR)", min_value=0.0, value=75.0, step=5.0)
            
        with col_f2:
            novos_dias = st.number_input("Dias de Trabalho Mensal", min_value=1, value=22, step=1)
            
        submit_button = st.form_submit_button(label="Guardar na Base de Dados")
        
        if submit_button:
            if not novo_cargo.strip():
                st.warning("Por favor, escreve um cargo válido.")
            else:
                custo_mensal = nova_qtd * novo_custo_diario * novos_dias
                
                conexao = sqlite3.connect('vanguarda_erp.db')
                cursor = conexao.cursor()
                cursor.execute(
                    "INSERT INTO mao_obra (cargo, quantidade, custo_diario, dias, custo_mensal) VALUES (?, ?, ?, ?, ?)",
                    (novo_cargo, nova_qtd, novo_custo_diario, novos_dias, custo_mensal)
                )
                conexao.commit()
                conexao.close()
                
                st.success(f"Trabalhador '{novo_cargo}' adicionado com sucesso!")
                st.rerun()

st.divider()

# --- SECÇÃO 2: PAINEL DE FLUXO DE CAIXA ---
st.subheader("📊 Painel de Fluxo de Caixa Mensal")

conn = sqlite3.connect('vanguarda_erp.db')
df_fluxo = pd.read_sql("SELECT mes, entradas, saidas FROM fluxo_caixa", conn)
conn.close()

if not df_fluxo.empty:
    fig, ax = plt.subplots(figsize=(8, 4))
    meses = df_fluxo['mes'].tolist()
    entradas = df_fluxo['entradas'].tolist()
    saidas = df_fluxo['saidas'].tolist()
    
    x = np.arange(len(meses))
    width = 0.35

    ax.bar(x - width/2, entradas, width, label='Entradas', color='#2ecc71')
    ax.bar(x + width/2, saidas, width, label='Saídas', color='#e74c3c')

    ax.set_xticks(x)
    ax.set_xticklabels(meses)
    ax.set_title('Evolução do Fluxo de Caixa')
    ax.legend(fontsize=8)
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    st.pyplot(fig)

# --- SECÇÃO 3: TABELA DE REGISTOS DE MÃO DE OBRA ---
with st.expander("📋 Ver Trabalhadores Registados na Base de Dados"):
    conn = sqlite3.connect('vanguarda_erp.db')
    df_mao = pd.read_sql("SELECT * FROM mao_obra", conn)
    conn.close()
    if not df_mao.empty:
        st.dataframe(df_mao)
    else:
        st.info("Ainda não existem trabalhadores registados.")
