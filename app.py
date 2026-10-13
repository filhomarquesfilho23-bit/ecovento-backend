import streamlit as st
import pandas as pd

# Configuração para Telemóvel / Layout Responsivo
st.set_page_config(
    page_title="OmniFlux Mobile",
    page_icon="⚡",
    layout="centered"
)

st.title("⚡ OmniFlux")
st.caption("O teu sistema operativo líquido e dinâmico.")

# Campo de Intenção (Onde dizes o que queres fazer)
st.markdown("### 🧠 O que vamos fazer agora?")
intencao_utilizador = st.text_input(
    "Escreve a tua intenção:",
    placeholder="Ex: analisar finanças, criar notas, gerir equipa..."
)

def processar_intencao(texto):
    """Motor semântico leve para telemóvel."""
    texto = texto.lower()
    if "finan" in texto or "despesa" in texto or "fatura" in texto or "dinheiro" in texto:
        return "financeiro"
    elif "equipa" in texto or "contrat" in texto or "salario" in texto:
        return "recursos_humanos"
    else:
        return "geral"

# Determinar o módulo ativo com base na intenção
modulo_ativo = processar_intencao(intencao_utilizador) if intencao_utilizador else "geral"

st.markdown("---")

# Materialização líquida da interface no telemóvel
if modulo_ativo == "financeiro":
    st.success("💧 Módulo Financeiro Materializado")
    
    # Componentes adaptados a toque vertical
    st.metric("Total em Caixa", "1.250,00 €", "+15%")
    
    st.markdown("**Evolução Recente:**")
    st.bar_chart({"Jan": 200, "Fev": 450, "Mar": 600})
    
    valor_simulado = st.slider("Simular Ajuste (€)", 0, 2000, 500)
    st.info(f"Valor selecionado para simulação: {valor_simulado} €")

elif modulo_ativo == "recursos_humanos":
    st.warning("💧 Módulo de Equipa Materializado")
    
    cargo = st.text_input("Cargo Pretendido", value="Engenheiro de Software")
    salario = st.number_input("Orçamento Mensal (€)", value=2500)
    
    if st.button("Calcular Impacto Anual"):
        st.success(f"O impacto anual para '{cargo}' será de {salario * 14} € (incluindo subsídios).")

else:
    st.info("💡 **Dica:** Escreve em cima o que pretendes (ex: *'analisar finanças'* ou *'gerir equipa'*) para ver o OmniFlux transformar-se instantaneamente!")
    
    st.markdown("### 📝 Bloco de Notas Líquido")
    st.text_area("Escreve ideias rápidas:", height=120)
