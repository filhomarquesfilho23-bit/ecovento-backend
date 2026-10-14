import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# Configuração da página para telemóvel
st.set_page_config(
    page_title="OmniFlux Pro - Passo 1",
    page_icon="⚡",
    layout="centered"
)

# --- BASE DE DADOS PERSISTENTE (SQLite Avançada) ---
def init_db():
    conn = sqlite3.connect('omniflux_pro.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS notas (id INTEGER PRIMARY KEY AUTOINCREMENT, texto TEXT, data TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS tarefas (id INTEGER PRIMARY KEY AUTOINCREMENT, tarefa TEXT, concluida INTEGER, data TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS transacoes (id INTEGER PRIMARY KEY AUTOINCREMENT, tipo TEXT, valor REAL, descricao TEXT, data TEXT)''')
    conn.commit()
    conn.close()

init_db()

# Funções de Notas
def guardar_nota(texto):
    conn = sqlite3.connect('omniflux_pro.db')
    c = conn.cursor()
    c.execute("INSERT INTO notas (texto, data) VALUES (?, ?)", (texto, datetime.now().strftime("%Y-%m-%d %H:%M")))
    conn.commit()
    conn.close()

def obter_notas():
    conn = sqlite3.connect('omniflux_pro.db')
    df = pd.read_sql_query("SELECT * FROM notas ORDER BY id DESC", conn)
    conn.close()
    return df

# Funções de Tarefas
def guardar_tarefa(tarefa):
    conn = sqlite3.connect('omniflux_pro.db')
    c = conn.cursor()
    c.execute("INSERT INTO tarefas (tarefa, concluida, data) VALUES (?, 0, ?)", (tarefa, datetime.now().strftime("%Y-%m-%d")))
    conn.commit()
    conn.close()

def obter_tarefas():
    conn = sqlite3.connect('omniflux_pro.db')
    df = pd.read_sql_query("SELECT * FROM tarefas ORDER BY id DESC", conn)
    conn.close()
    return df

def atualizar_estado_tarefa(tarefa_id, concluida):
    conn = sqlite3.connect('omniflux_pro.db')
    c = conn.cursor()
    c.execute("UPDATE tarefas SET concluida = ? WHERE id = ?", (1 if concluida else 0, tarefa_id))
    conn.commit()
    conn.close()

# Funções Financeiras
def guardar_transacao(tipo, valor, descricao):
    conn = sqlite3.connect('omniflux_pro.db')
    c = conn.cursor()
    c.execute("INSERT INTO transacoes (tipo, valor, descricao, data) VALUES (?, ?, ?, ?)", 
              (tipo, valor, descricao, datetime.now().strftime("%Y-%m-%d")))
    conn.commit()
    conn.close()

def obter_transacoes():
    conn = sqlite3.connect('omniflux_pro.db')
    df = pd.read_sql_query("SELECT * FROM transacoes ORDER BY id DESC", conn)
    conn.close()
    return df

# --- ESTILO AZUL FUTURISTA TOTALMENTE PREENCHIDO (CUSTOM CSS) ---
st.markdown("""
    <style>
    .stApp {
        background-color: #0b1329;
        color: #ffffff;
    }
    h1, h2, h3 {
        color: #38bdf8 !important;
        font-family: -apple-system, BlinkMacSystemFont, sans-serif;
    }
    .stTextInput input, .stTextArea textarea, .stNumberInput input, .stSelectbox select {
        background-color: #1e293b !important;
        color: #ffffff !important;
        border: 1px solid #38bdf8 !important;
        border-radius: 8px;
    }
    .stButton button, div.stFormSubmitButton > button {
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%) !important;
        color: #ffffff !important;
        border: 1px solid #38bdf8 !important;
        border-radius: 8px;
        font-weight: bold;
        width: 100%;
        padding: 0.6rem 1rem;
        box-shadow: 0 4px 12px rgba(14, 165, 233, 0.4);
    }
    .stButton button:hover, div.stFormSubmitButton > button:hover {
        background: linear-gradient(135deg, #38bdf8 0%, #0284c7 100%) !important;
        color: #ffffff !important;
    }
    .stSuccess, .stInfo, .stWarning {
        background-color: #1e293b !important;
        border: 1px solid #38bdf8 !important;
        color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ OmniFlux Pro")
st.caption("Sistema Operativo Líquido • Passo 1: Dashboard Dinâmico.")

# --- GESTÃO DE ESTADO E NAVEGAÇÃO LÍQUIDA ---
if "intencao_atual" not in st.session_state:
    st.session_state.intencao_atual = "dashboard"

st.markdown("### 🎙️ Painel de Controlo Rápido")
col1, col2 = st.columns(2)
with col1:
    if st.button("🏠 Dashboard"):
        st.session_state.intencao_atual = "dashboard"
    if st.button("💰 Finanças"):
        st.session_state.intencao_atual = "financeiro"
with col2:
    if st.button("📋 Tarefas"):
        st.session_state.intencao_atual = "tarefas"
    if st.button("📝 Notas & Exportar"):
        st.session_state.intencao_atual = "notas"

modulo_ativo = st.session_state.intencao_atual
st.markdown("---")

# --- 1. DASHBOARD COM GRÁFICOS DINÂMICOS REAIS ---
if modulo_ativo == "dashboard":
    st.success("💧 Dashboard Dinâmico em Tempo Real")
    
    # Obter dados reais das tabelas
    df_t = obter_tarefas()
    total_tarefas = len(df_t) if not df_t.empty else 0
    pendentes = len(df_t[df_t['concluida'] == 0]) if not df_t.empty else 0
    concluidas = total_tarefas - pendentes
    
    df_n = obter_notas()
    total_notas = len(df_n) if not df_n.empty else 0
    
    df_fin = obter_transacoes()
    total_receitas = df_fin[df_fin['tipo'] == 'Receita']['valor'].sum() if not df_fin.empty else 0.0
    total_despesas = df_fin[df_fin['tipo'] == 'Despesa']['valor'].sum() if not df_fin.empty else 0.0
    saldo_liquido = 4850.0 + total_receitas - total_despesas

    # Métricas de topo
    c1, c2 = st.columns(2)
    with c1:
        st.metric("Saldo Líquido", f"{saldo_liquido:,.2f} €")
    with c2:
        st.metric("Tarefas Pendentes", f"{pendentes}")

    st.markdown("### 📊 Gráficos de Atividade do Sistema")
    
    if not df_fin.empty or total_tarefas > 0:
        # Gráfico dinâmico de finanças reais
        st.markdown("**Resumo Financeiro (Receitas vs Despesas):**")
        df_chart_fin = pd.DataFrame({
            "Fluxo": ["Receitas", "Despesas"],
            "Montante (€)": [total_receitas, total_despesas]
        }).set_index("Fluxo")
        st.bar_chart(df_chart_fin)
        
        # Gráfico dinâmico de tarefas reais
        st.markdown("**Progresso de Tarefas:**")
        df_chart_t = pd.DataFrame({
            "Estado": ["Concluídas", "Pendentes"],
            "Quantidade": [concluidas, pendentes]
        }).set_index("Estado")
        st.bar_chart(df_chart_t)
    else:
        st.info("💡 Regista algumas transações no módulo de Finanças ou cria tarefas para veres os gráficos dinâmicos a preencherem-se automaticamente aqui!")

# --- 2. MÓDULO FINANCEIRO INTERATIVO ---
elif modulo_ativo == "financeiro":
    st.success("💧 Módulo Financeiro Interativo Materializado")
    
    with st.form("form_financas"):
        st.markdown("**Registar Movimento Financeiro:**")
        tipo_mov = st.selectbox("Tipo", ["Receita", "Despesa"])
        valor_mov = st.number_input("Valor (€)", min_value=0.0, value=100.0)
        desc_mov = st.text_input("Descrição", placeholder="Ex: Venda de serviço, Assinatura...")
        btn_registar = st.form_submit_button("Adicionar ao Sistema")
        
        if btn_registar:
            guardar_transacao(tipo_mov, valor_mov, desc_mov)
            st.success("Movimento financeiro registado com sucesso!")
            st.rerun()

    df_fin = obter_transacoes()
    st.markdown("### 📊 Histórico de Transações")
    if not df_fin.empty:
        st.dataframe(df_fin[['data', 'tipo', 'descricao', 'valor']], use_container_width=True)
    else:
        st.write("Ainda sem transações registadas.")

# --- 3. MÓDULO DE TAREFAS PERSISTENTES ---
elif modulo_ativo == "tarefas":
    st.info("💧 Módulo de Tarefas Estratégicas Materializado")
    
    nova_t = st.text_input("Adicionar nova prioridade:")
    if st.button("Registar Tarefa"):
        if nova_t.strip():
            guardar_tarefa(nova_t)
            st.success("Tarefa guardada na base de dados!")
            st.rerun()
        else:
            st.warning("Escreve uma tarefa válida.")
            
    st.markdown("### 📋 Lista de Tarefas Ativas")
    df_t = obter_tarefas()
    if not df_t.empty:
        for index, row in df_t.iterrows():
            concluida_atual = bool(row['concluida'])
            novo_estado = st.checkbox(f"[{row['data']}] {row['tarefa']}", value=concluida_atual, key=f"t_{row['id']}")
            if novo_estado != concluida_atual:
                atualizar_estado_tarefa(row['id'], novo_estado)
                st.rerun()
    else:
        st.write("Sem tarefas criadas.")

# --- 4. MÓDULO DE NOTAS & EXPORTAÇÃO ---
elif modulo_ativo == "notas":
    st.success("💧 Módulo de Memória & Exportação Materializado")
    
    texto_nota = st.text_area("Regista o teu pensamento:", placeholder="Escreve aqui a tua ideia...")
    if st.button("Salvar na Base de Dados Global"):
        if texto_nota.strip():
            guardar_nota(texto_nota)
            st.success("Nota gravada com sucesso!")
            st.rerun()
        else:
            st.warning("Escreve algo antes de salvar.")
            
    st.markdown("### 📚 Histórico de Notas")
    df_notas = obter_notas()
    if not df_notas.empty:
        for index, row in df_notas.iterrows():
            st.info(f"[{row['data']}] {row['texto']}")
            
        csv_data = df_notas.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Descarregar Notas em formato CSV",
            data=csv_data,
            file_name="omniflux_notas.csv",
            mime="text/csv",
        )
    else:
        st.write("Ainda não existem notas guardadas.")

st.markdown("---")
st.caption("OmniFlux Pro • Passo 1 Concluído ⚡")
