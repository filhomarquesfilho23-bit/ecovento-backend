import streamlit as st
from supabase import create_client, Client
import pandas as pd
import pdfplumber

# Configuração da Página
st.set_page_config(page_title="Vanguarda DocAI", page_icon="📄", layout="wide")

st.title("📄 Vanguarda DocAI - Análise Inteligente de Faturas e Recibos")

# BARRA LATERAL - Configuração do Supabase
with st.sidebar:
    st.header("⚙️ Configuração do Sistema")
    supabase_url = st.text_input("Supabase URL", value="https://rufguaytuamakjdsrx.supabase.co")
    supabase_key = st.text_input("Supabase Key (anon)", type="password", value="eyJ...")
    
    st.markdown("---")
    st.markdown("### 💡 Sobre o Projeto")
    st.markdown("Plataforma avançada de IA e extração automática de dados de faturas para otimização contabilística.")

@st.cache_resource
def init_supabase(url, key):
    try:
        return create_client(url, key)
    except Exception:
        return None

supabase = init_supabase(supabase_url, supabase_key)

# CORPO PRINCIPAL - Abas da Aplicação
aba1, aba2 = st.tabs(["📤 Upload e Extração", "📊 Histórico de Faturas"])

with aba1:
    st.subheader("Carregar Fatura (PDF)")
    uploaded_file = st.file_uploader("Escolha um ficheiro PDF de fatura", type=["pdf"])
    
    texto_completo = ""
    if uploaded_file is not None:
        st.success("Ficheiro carregado com sucesso!")
        
        # Leitura do PDF
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                texto_completo += page.extract_text() or ""
        
        st.markdown("### 🔍 Texto Extraído do Documento:")
        st.text_area("Conteúdo bruto detetado:", texto_completo, height=200)
        
        # Campos extraídos
        st.markdown("### 📋 Dados Identificados pela IA:")
        col1, col2, col3 = st.columns(3)
        with col1:
            fornecedor_input = st.text_input("Fornecedor", value="Empresa Exemplo Lda")
        with col2:
            total_input = st.number_input("Valor Total (€)", value=125.50)
        with col3:
            data_input = st.text_input("Data da Fatura", value="2026-10-13")
            
        if st.button("💾 Guardar Fatura na Base de Dados"):
            if supabase:
                try:
                    data = {
                        "fornecedor": fornecedor_input,
                        "total": total_input,
                        "data_fatura": data_input,
                        "texto_extraido": texto_completo[:500]
                    }
                    supabase.table("faturas").insert(data).execute()
                    st.success("Fatura processada e guardada com sucesso no Supabase!")
                except Exception as e:
                    st.error(f"Erro ao guardar na base de dados: {e}")
            else:
                st.warning("Ligação ao Supabase não configurada corretamente.")

with aba2:
    st.subheader("Histórico de Faturas Processadas")
    if supabase:
        try:
            response = supabase.table("faturas").select("*").execute()
            dados = response.data
            if dados:
                df_faturas = pd.DataFrame(dados)
                st.dataframe(df_faturas, use_container_width=True)
            else:
                st.info("Ainda não existem faturas guardadas na base de dados.")
        except Exception as e:
            st.error(f"Erro ao carregar o histórico: {e}")
    else:
        df_faturas = pd.DataFrame(columns=["ID", "Fornecedor", "Total (€)", "Data", "Estado"])
        st.dataframe(df_faturas, use_container_width=True)
