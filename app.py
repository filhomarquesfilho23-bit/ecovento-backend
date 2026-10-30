import streamlit as st
from google import genai

st.set_page_config(page_title="TikTok AI Creator", page_icon="🎵", layout="centered")

st.title("🎵 TikTok AI Creator Agent")
st.markdown("Cria conteúdos virais, ganchos magnéticos e roteiros de alto impacto para o TikTok.")

# Campos de entrada
niche = st.text_input("Qual é o tema ou nicho do vídeo?", "Programação e Desenvolvimento Mobile")
goal = st.selectbox("Qual é o objetivo principal?", [
    "Educar / Ensinar Algo Rápido", 
    "Bastidores de um Projeto de Software", 
    "Curiosidade / HACK Tecnológico", 
    "Promover um Produto ou SaaS"
])

if st.button("Gerar Estratégia e Roteiro Viral"):
    with st.spinner("A criar o roteiro otimizado para o TikTok..."):
        try:
            # Inicializa o cliente usando explicitamente a chave guardada nos Secrets do Streamlit
            client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
            
            prompt = f"""
            Atua como um criador de conteúdo de sucesso e especialista no algoritmo do TikTok. 
            Cria um roteiro completo e altamente envolvente para o TikTok sobre o nicho: '{niche}', com o objetivo de: '{goal}'.
            
            Estrutura a resposta da seguinte forma:
            1. **Ganchos de Impacto (0-3 segundos):** Dá 3 opções de frases iniciais fortes para agarrar a atenção.
            2. **Desenvolvimento do Roteiro:** Um texto dinâmico, direto ao ponto e pronto a gravar (focado em vídeos de 30 a 60 segundos).
            3. **Chamada para Ação (CTA):** O que dizer no final para gerar comentários e interações.
            4. **Hashtags Virais:** 5 hashtags estratégicas para o nicho.
            """
            
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt
            )
            
            st.success("Roteiro gerado com sucesso! 🚀")
            st.markdown(response.text)
            
        except Exception as e:
            st.error(f"Ocorreu um erro ao gerar o conteúdo. Verifica se a chave de API está correta nos Secrets. Detalhe: {e}")
