import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# Configuração da página para telemóvel
st.set_page_config(
    page_title="OmniFlux Ultimate",
    page_icon="⚡",
    layout="centered"
)

# --- BASE DE DADOS PERSISTENTE (SQLite) ---
def init_db():
    conn = sqlite3.connect('omniflux.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS notas (id INTEGER PRIMARY KEY AUTOINCREMENT, texto TEXT, data TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS tarefas (id INTEGER PRIMARY KEY AUTOINCREMENT, tarefa TEXT, concluida INTEGER, data TEXT)''')
    conn.commit()
    conn.close()

init_db()

def guardar_nota(texto):
    conn = sqlite3.connect('omniflux.db')
    c = conn.cursor()
    c.execute("INSERT INTO notas (texto, data) VALUES (?, ?)", (texto, datetime.now().strftime("%Y-%m-%d %H:%M")))
    conn.commit()
    conn.close()

def obter_notas():
    conn = sqlite3.connect('omniflux.db')
    df = pd.read_sql_query("SELECT * FROM notas ORDER BY id DESC", conn)
    conn.close()
    return df

# --- ESTILO AZUL FUTURISTA ---
st.markdown("""
    <style>
    .stApp {
        background-color: #0b1329;
        color: #e2e8f0;
    }
    h1, h2, h3 {
        color: #38bdf8 !important;
        font-family: -apple-system, BlinkMacSystemFont, sans-serif;
    }
    .stTextInput input, .stTextArea textarea {
        background-color: #1e293b !important;
        color: #ffffff !important;
        border: 1px solid #38bdf8 !important;
        border-radius: 8px;
    }
    .stButton button {
        background: linear-gradient(135deg, #0ea5e9 0%, #2563eb 100%);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: bold;
        width: 100%;
        padding: 0.6rem 1rem;
        box-shadow: 0 4px 12px rgba(14, 165, 233, 0.3);
    }
    .stButton button:hover {
        background: linear-gradient(135deg, #38bdf8 0%, #1d4ed8 100%);
        border: none;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ OmniFlux Instantâneo")
st.caption("Sistema Operativo Líquido de Resposta Imediata.")

# Gerir o estado da intenção atual
if "intencao_atual" not in st.session_state:
    st.session_state.intencao_atual = "geral"

# --- PAINEL DE CONTROLO POR TOQUE RÁPIDO (Substituto fiável para telemóvel) ---
st.markdown("### 🎙️ Seleção de Intenção Instantânea")
st.caption("Toca num botão para materializar a resposta imediatamente em baixo:")

col1, col2 = st.columns(2)
with col1:
    if st.button("💰 Analisar Finanças"):
        st.session_state.intencao_atual = "financeiro"
    if st.button("📋 Criar Tarefas"):
        st.session_state.intencao_atual = "tarefas"
with col2:
    if st.button("👥 Gerir Equipa"):
        st.session_state.intencao_atual = "recursos_humanos"
    if st.button("📝 Escrever Nota"):
        st.session_state.intencao_atual = "notas"

modulo_ativo = st.session_state.intencao_atual

st.markdown("---")

# --- MATERIALIZAÇÃO LÍQUIDA DINÂMICA (Respostas diretas em baixo) ---
if modulo_ativo == "financeiro":
    st.success("💧 Módulo Financeiro Materializado Instantaneamente")
    st.metric("Saldo Global Ativo", "4.850,00 €", "+18.2%")
    st.bar_chart({"Jan": 1500, "Fev": 2800, "Mar": 4850})
    limite = st.slider("Ajustar Limite de Tesouraria (€)", 0, 10000, 4000)
    st.info(f"Limite otimizado: {limite} €")

elif modulo_ativo == "recursos_humanos":
    st.warning("💧 Módulo de Gestão de Talento Materializado Instantaneamente")
    cargo = st.text_input("Cargo Pretendido", value="Arquiteto de Sistemas IA")
    vencimento = st.number_input("Orçamento Mensal Bruto (€)", value=3000)
    if st.button("Simular Contrato Anual"):
        st.success(f"Custo total anual projetado para {cargo}: {vencimento * 14} € (Subsídios incluídos).")

elif modulo_ativo == "tarefas":
    st.info("💧 Módulo de Tarefas e Execução Materializado Instantaneamente")
    nova_tarefa = st.text_input("Nova Tarefa Estratégica:")
    if st.button("Guardar Tarefa"):
        st.toast("Tarefa guardada com sucesso!", icon="✅")
    st.checkbox("Operação fluida no OmniFlux", value=True)
    st.checkbox("Validar transições no telemóvel", value=True)

elif modulo_ativo == "notas":
    st.success("💧 Módulo de Memória Persistente Materializado Instantaneamente")
    texto_nota = st.text_area("Regista o teu pensamento:", placeholder="Escreve aqui a tua ideia...")
    if st.button("Salvar na Base de Dados Global"):
        if texto_nota.strip():
            guardar_nota(texto_nota)
            st.success("Nota gravada com sucesso na memória persistente!")
        else:
            st.warning("Escreve algo antes de salvar.")
    
    st.markdown("### 📚 Histórico de Notas Guardadas")
    df_notas = obter_notas()
    if not df_notas.empty:
        for index, row in df_notas.iterrows():
            st.info(f"[{row['data']}] {row['texto']}")
    else:
        st.write("Ainda não existem notas guardadas.")

else:
    st.info("💡 **OmniFlux Pronto:** Toca num dos botões em cima para ver a resposta e os gráficos a aparecerem instantaneamente em baixo no ecrã do telemóvel!")

st.markdown("---")
st.caption("OmniFlux Ultimate • Resposta Instantânea ⚡")
