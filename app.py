import streamlit as st
import pandas as pd
from datetime import datetime

# Configuração para Telemóvel / Layout Responsivo
st.set_page_config(
    page_title="OmniFlux - Sistema Líquido",
    page_icon="⚡",
    layout="centered"
)

st.title("⚡ OmniFlux")
st.caption("O teu sistema operativo líquido e dinâmico.")

# Inicializar histórico na sessão se não existir
if "historico_intencoes" not in st.session_state:
    st.session_state.historico_intencoes = []

# Campo de Intenção Absoluta
st.markdown("### 🧠 O que vamos fazer hoje?")
intencao_utilizador = st.text_input(
    "Escreve a tua intenção:",
    placeholder="Ex: analisar finanças, gerir equipa, criar tarefas..."
)

def processar_intencao(texto):
    """Motor semântico avançado para o OmniFlux."""
    texto = texto.lower()
    if "finan" in texto or "despesa" in texto or "fatura" in texto or "dinheiro" in texto:
        return "financeiro"
    elif "equipa" in texto or "contrat" in texto or "salario" in texto:
        return "recursos_humanos"
    elif "tarefa" in texto or "projeto" in texto or "fazer" in texto:
        return "tarefas"
    else:
        return "geral"

# Registar intenção no histórico se for nova
if intencao_utilizador and (not st.session_state.historico_intencoes or st.session_state.historico_intencoes[-1] != intencao_utilizador):
    st.session_state.historico_intencoes.append(intencao_utilizador)

modulo_ativo = processar_intencao(intencao_utilizador) if intencao_utilizador else "geral"

st.markdown("---")

# Materialização líquida da interface baseada na intenção
if modulo_ativo == "financeiro":
    st.success("💧 Módulo Financeiro Materializado")
    st.metric("Total Disponível", "2.450,00 €", "+12.5%")
    
    st.markdown("**Evolução Mensal (€):**")
    st.bar_chart({"Jan": 1200, "Fev": 1800, "Mar": 2450})
    
    orcamento = st.slider("Simular Limite de Gastos (€)", 0, 5000, 2000)
    st.info(f"Orçamento configurado para: {orcamento} €")

elif modulo_ativo == "recursos_humanos":
    st.warning("💧 Módulo de Gestão de Equipa Materializado")
    cargo = st.text_input("Função do Colaborador", value="Especialista IA")
    salario_base = st.number_input("Remuneração Base Mensal (€)", value=2200)
    
    if st.button("Gerar Proposta Contratual"):
        st.success(f"Proposta gerada para {cargo} com custo anual estimado de {salario_base * 14} €.")

elif modulo_ativo == "tarefas":
    st.info("💧 Módulo de Execução de Tarefas Materializado")
    nova_tarefa = st.text_input("Adicionar nova prioridade:")
    if st.button("Registar Tarefa"):
        st.toast(f"Tarefa guardada: {nova_tarefa}", icon="✅")
    
    st.markdown("**Tarefas Ativas:**")
    st.checkbox("Finalizar protótipo do OmniFlux", value=True)
    st.checkbox("Testar integração no telemóvel", value=True)

else:
    st.info("💡 **OmniFlux Ativo:** Escreve em cima o que pretendes (ex: *'analisar finanças'*, *'gerir equipa'* ou *'criar tarefas'*) para transformar a interface instantaneamente!")
    
    st.markdown("### 📝 Bloco de Notas Líquido")
    st.text_area("Regista pensamentos rápidos:", height=120, placeholder="Escreve aqui...")

# Rodapé minimalista
st.markdown("---")
st.caption("OmniFlux Core • Pronto para produção móvel")
