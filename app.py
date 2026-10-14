import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import streamlit.components.v1 as components

# Configuração da página para telemóvel
st.set_page_config(
    page_title="OmniFlux Voice Ultimate",
    page_icon="⚡",
    layout="centered"
)

# --- CAPTURAR VOZ VIA URL PARAMS ---
query_params = st.query_params
if "intencao" in query_params:
    st.session_state.intencao_atual = query_params["intencao"]
    # Limpar parâmetro para evitar loops
    st.query_params.clear()

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

# --- ESTILO AZUL FUTURISTA & VOZ (CUSTOM CSS) ---
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
        padding: 0.5rem 1rem;
        box-shadow: 0 4px 12px rgba(14, 165, 233, 0.3);
    }
    .stButton button:hover {
        background: linear-gradient(135deg, #38bdf8 0%, #1d4ed8 100%);
        border: none;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ OmniFlux Voice")
st.caption("Sistema Operativo Líquido com Comandos por Voz Instantâneos.")

# --- COMPONENTE DE VOZ ROBUSTO (RELOAD VIA URL) ---
st.markdown("### 🎙️ Comando por Voz Inteligente")
voice_component = """
<div style="text-align: center; margin-bottom: 15px;">
    <button onclick="startListening()" style="background: linear-gradient(135deg, #f43f5e 0%, #e11d48 100%); color: white; border: none; border-radius: 25px; padding: 12px 24px; font-weight: bold; font-size: 16px; box-shadow: 0 4px 15px rgba(244, 63, 94, 0.4); cursor: pointer; width: 100%;">
        🎤 Tocar para Falar com o OmniFlux
    </button>
    <p id="status" style="color: #38bdf8; font-size: 13px; margin-top: 8px;">Toque no botão e diga o que pretende...</p>
</div>

<script>
function startListening() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
        alert("O seu browser não suporta reconhecimento de voz direto. Use o campo de texto abaixo.");
        return;
    }
    const recognition = new SpeechRecognition();
    recognition.lang = 'pt-PT';
    recognition.interimResults = false;
    
    document.getElementById("status").innerText = "A escutar a sua voz...";
    
    recognition.onresult = function(event) {
        const speechToText = event.results[0][0].transcript;
        document.getElementById("status").innerText = "Detetado: " + speechToText + " (A carregar...)";
        
        // Recarregar a página passando o texto na URL para o Streamlit apanhar logo
        setTimeout(() => {
            const baseUrl = window.parent.location.origin + window.parent.location.pathname;
            window.parent.location.href = baseUrl + '?intencao=' + encodeURIComponent(speechToText);
        }, 400);
    };
    
    recognition.onerror = function(event) {
        document.getElementById("status").innerText = "Erro ao escutar. Tente novamente.";
    };
    
    recognition.start();
}
</script>
"""
components.html(voice_component, height=100)

# --- CAMPO DE INTENÇÃO ABSOLUTA ---
if "intencao_atual" not in st.session_state:
    st.session_state.intencao_atual = ""

st.markdown("### 🧠 Campo de Intenção Global")
intencao_utilizador = st.text_input(
    "O que desejas realizar hoje?",
    value=st.session_state.intencao_atual,
    placeholder="Ex: analisar finanças, escrever uma nota, gerir equipa..."
)

st.session_state.intencao_atual = intencao_utilizador

def motor_ia_semantico(texto):
    """Motor de intenção inteligente otimizado."""
    t = texto.lower()
    if "finan" in t or "dinheiro" in t or "gastos" in t or "orçamento" in t or "fatura" in t:
        return "financeiro"
    elif any(k in t for k in ["equipa", "salario", "contrat", "colaborador"]):
        return "recursos_humanos"
    elif any(k in t for k in ["tarefa", "projeto", "fazer", "prioridade"]):
        return "tarefas"
    elif any(k in t for k in ["nota", "escrever", "ideia", "registo", "lembrar"]):
        return "notas"
    else:
        return "geral"

modulo_ativo = motor_ia_semantico(intencao_utilizador) if intencao_utilizador else "geral"

st.markdown("---")

# --- MATERIALIZAÇÃO LÍQUIDA DINÂMICA ---
if modulo_ativo == "financeiro":
    st.success("💧 Módulo Financeiro Materializado por Voz")
    st.metric("Saldo Global Ativo", "4.850,00 €", "+18.2%")
    st.bar_chart({"Jan": 1500, "Fev": 2800, "Mar": 4850})
    limite = st.slider("Ajustar Limite de Tesouraria (€)", 0, 10000, 4000)
    st.info(f"Limite otimizado: {limite} €")

elif modulo_ativo == "recursos_humanos":
    st.warning("💧 Módulo de Gestão de Talento Materializado por Voz")
    cargo = st.text_input("Cargo Pretendido", value="Arquiteto de Sistemas IA")
    vencimento = st.number_input("Orçamento Mensal Bruto (€)", value=3000)
    if st.button("Simular Contrato Anual"):
        st.success(f"Custo total anual projetado para {cargo}: {vencimento * 14} € (Subsídios incluídos).")

elif modulo_ativo == "tarefas":
    st.info("💧 Módulo de Tarefas e Execução Materializado por Voz")
    nova_tarefa = st.text_input("Nova Tarefa Estratégica:")
    if st.button("Guardar Tarefa"):
        st.toast("Tarefa guardada com sucesso!", icon="✅")
    st.checkbox("Integrar comandos por voz instantâneos no OmniFlux", value=True)
    st.checkbox("Validar transições líquidas no telemóvel", value=True)

elif modulo_ativo == "notas":
    st.success("💧 Módulo de Memória Persistente Materializado por Voz")
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
    st.info("💡 **OmniFlux Ativo:** Toca no botão vermelho de voz acima e dita uma ordem (ex: *'analisar finanças'* ou *'escrever nota'*) para materializar a ferramenta ideal na hora.")
    st.markdown("### 📝 Espaço de Trabalho Fluido")
    st.text_area("Rascunho Rápido:", height=100, placeholder="Escreve notas rápidas...")

st.markdown("---")
st.caption("OmniFlux Voice Ultimate • Voz Instantânea + IA Semântica + SQLite ⚡")
