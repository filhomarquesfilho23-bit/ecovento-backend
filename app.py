import streamlit as st
from loader import obter_system_prompt
from auditor import auditar_codigo_local
from openai import OpenAI

st.set_page_config(page_title="Painel de Cibersegurança - Agente", page_icon="🛡️", layout="wide")

st.title("Centro de Controlo e Cibersegurança IA")
st.markdown("Plataforma baseada no ficheiro de configuração `agente.json` para auditoria e consultoria empresarial.")

aba1, aba2 = st.tabs(["🛡️ Consultor de Cibersegurança", "🔍 Auditor de Código no Repositório"])

with aba1:
    st.subheader("Fale com o Agente Especialista")
    pergunta_utilizador = st.text_area("Descreva a sua dúvida de segurança, infraestrutura ou conformidade:")
    
    if st.button("Enviar para a IA"):
        if pergunta_utilizador.strip():
            with st.spinner("A analisar o cenário com base nas diretrizes do agente..."):
                try:
                    client = OpenAI()
                    system_prompt = obter_system_prompt()
                    
                    resposta = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": pergunta_utilizador}
                        ]
                    )
                    st.success("Análise Concluída:")
                    st.write(resposta.choices[0].message.content)
                except Exception as e:
                    st.error(f"Erro ao ligar à API de IA: {e}")
        else:
            st.warning("Por favor, escreva uma questão.")

with aba2:
    st.subheader("Auditoria de Vulnerabilidades Locais")
    st.markdown("Executa uma verificação rápida por padrões de risco no código-fonte do repositório.")
    
    if st.button("Executar Varredura de Segurança"):
        with st.spinner("A examinar os ficheiros do projeto..."):
            falhas = auditar_codigo_local()
            
        if falhas:
            st.warning(f"Foram encontrados {len(falhas)} potenciais pontos de atenção:")
            for f in falhas:
                st.write(f"- **Ficheiro:** `{f['ficheiro']}` (Linha {f['linha']}) -> _{f['alerta']}_")
        else:
            st.success("Nenhuma falha óbvia de credenciais expostas foi detetada nos ficheiros escaneados!")
