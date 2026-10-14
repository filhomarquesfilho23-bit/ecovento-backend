import streamlit as st
import pandas as pd

# Configuração para Telemóvel / Layout Responsivo
st.set_page_config(
    page_title="OmniFlux - Sistema Líquido",
    page_icon="⚡",
    layout="centered"
)

# --- ESTILO AZUL FUTURISTA (CUSTOM CSS) ---
st.markdown("""
    <style>
    /* Fundo geral da aplicação em tons de azul escuro / tecnológico */
    .stApp {
        background-color: #0b1329;
        color: #e2e8f0;
    }
    
    /* Estilização dos títulos e textos */
    h1, h2, h3 {
        color: #38bdf8 !important;
        font-family: -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Caixas de input e texto */
    .stTextInput input, .stTextArea textarea {
        background-color: #1e293b !important;
        color: #ffffff !important;
        border: 1px solid #38bdf8 !important;
        border-radius: 8px;
    }
    
    /* Botões estilizados com tom azul néon */
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

st.title("⚡ OmniFlux")
st.caption("O teu sistema operativo líquido e dinâmico.")

# --- PAINEL DE DEMONSTRAÇÃO RÁPIDA ---
st.markdown("### 🎬 Painel de Demonstração Rápida")
col_d1, col_d2, col_d3 = st.columns(3)
with col_d1:
    btn_fin = st.button("💰 Finanças")
with col_d2:
    btn_rh = st.button("👥 Equipa")
with col_d3:
    btn_tarefas = st.button("📋 Tarefas")

# Definir intenção por clique ou por texto livre
if "intencao_atual" not in st.session_state:
    st.session_state.intencao_atual = ""

if btn_fin:
    st.session_state.intencao_atual = "analisar finanças"
elif btn_rh:
    st.session_state.intencao_atual = "gerir equipa"
elif btn_tarefas:
    st.session_state.intencao_atual = "criar tarefas"

# Campo de Intenção Absoluta (Texto livre)
st.markdown("---")
st.markdown("### 🧠 Escrever Intenção")
intencao_utilizador = st.text_input(
    "Ou escreve o que queres fazer:",
    value=st.session_state.intencao_atual,
    placeholder="Ex: analisar finanças, gerir equipa..."
)

# Atualizar estado global
st.session_state.intencao_atual = intencao_utilizador

def processar_intencao(texto):
    """Motor semântico do OmniFlux."""
    texto = texto.lower()
    if "finan" in texto or "despesa" in texto or "fatura" in texto or "dinheiro" in texto:
        return "financeiro"
    elif "equipa" in texto or "contrat" in texto or "salario" in texto:
        return "recursos_humanos"
    elif "tarefa" in texto or "projeto" in texto or "fazer" in texto:
        return "tarefas"
    else:
        return "geral"

modulo_ativo = processar_intencao(intencao_utilizador) if intencao_utilizador else "geral"

st.markdown("---")

# Materialização líquida da interface baseada na intenção
if modulo_ativo == "financeiro":
    st.success("💧 Módulo Financeiro Materializado Instantaneamente")
    st.metric("Total Disponível", "2.450,00 €", "+12.5%")
    
    st.markdown("**Evolução Mensal (€):**")
    st.bar_chart({"Jan": 1200, "Fev": 1800, "Mar": 2450})
    
    orcamento = st.slider("Simular Limite de Gastos (€)", 0, 5000, 2000)
    st.info(f"Orçamento configurado para: {orcamento} €")

elif modulo_ativo == "recursos_humanos":
    st.warning("💧 Módulo de Gestão de Equipa Materializado Instantaneamente")
    cargo = st.text_input("Função do Colaborador", value="Especialista IA")
    salario_base = st.number_input("Remuneração Base Mensal (€)", value=2200)
    
    if st.button("Gerar Proposta Contratual"):
        st.success(f"Proposta gerada para {cargo} com custo anual estimado de {salario_base * 14} €.")

elif modulo_ativo == "tarefas":
    st.info("💧 Módulo de Execução de Tarefas Materializado Instantaneamente")
    nova_tarefa = st.text_input("Adicionar nova prioridade:")
    if st.button("Registar Tarefa"):
        st.toast(f"Tarefa guardada: {nova_tarefa}", icon="✅")
    
    st.markdown("**Tarefas Ativas:**")
    st.checkbox("Finalizar protótipo do OmniFlux", value=True)
    st.checkbox("Testar transição fluida no telemóvel", value=True)

else:
    st.info("💡 **OmniFlux Pronto:** Usa os botões de demonstração em cima ou escreve uma intenção para transformar o ecrã na hora!")
    
    st.markdown("### 📝 Bloco de Notas Líquido")
    st.text_area("Regista pensamentos rápidos:", height=120, placeholder="Escreve aqui...")

# Rodapé minimalista
st.markdown("---")
st.caption("OmniFlux Core • Sistema Operativo Líquido v1.0")
