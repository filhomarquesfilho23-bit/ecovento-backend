import streamlit as st
import pandas as pd
import pdfplumber
import io

try:
    from supabase import create_client, Client
except ImportError:
    pass

# Configuração da Página
st.set_page_config(
    page_title="Vanguarda DocAI",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📄 Vanguarda DocAI - Análise Inteligente de Faturas e Recibos")

# BARRA LATERAL - Configuração do Supabase com Link Direto
with st.sidebar:
    st.header("⚙️ Configuração do Sistema")
    
    # Link direto para o Supabase
    st.markdown("[🔗 Abrir o Painel do Supabase](https://supabase.com)", unsafe_allow_html=True)
    st.markdown("---")
    
    supabase_url = st.text_input("Supabase URL", value="")
    supabase_key = st.text_input("Supabase Key (anon)", type="password", value="")
    
    st.markdown("---")
    st.markdown("### 💡 Sobre o Projeto")
    st.markdown("Plataforma avançada de IA e extração automática de dados de faturas para otimização contabilística.")

# Inicialização segura do Supabase
supabase = None
if supabase_url and supabase_key and "supabase.co" in supabase_url:
    try:
        supabase = create_client(supabase_url, supabase_key)
    except Exception:
        supabase = None

# CORPO PRINCIPAL - Abas da Aplicação
aba1, aba2 = st.tabs(["📤 Upload e Extração", "📊 Histórico de Faturas"])

with aba1:
    st.subheader("Carregar Documento ou Inserir Texto")
    
    uploaded_file = st.file_uploader("Escolha o documento da fatura (PDF)", type=None)
    
    texto_completo = ""
    if uploaded_file is not None:
        st.success("Ficheiro carregado com sucesso!")
        try:
            bytes_data = uploaded_file.getvalue()
            with pdfplumber.open(io.BytesIO(bytes_data)) as pdf:
                for page in pdf.pages:
                    texto_completo += page.extract_text() or ""
        except Exception as e:
            st.warning("Não foi possível ler automaticamente o PDF. Podes colar o texto abaixo.")
            
    st.markdown("---")
    st.markdown("💡 **Alternativa para Telemóvel:** Podes colar o texto da fatura diretamente aqui em baixo:")
    texto_manual = st.text_area("Texto da Fatura (Extração manual ou colar conteúdo):", value=texto_completo, height=150)
    
    texto_final = texto_manual if texto_manual else texto_completo
    
    if texto_final:
        st.markdown("### 📋 Dados Identificados para Registo:")
        col1, col2, col3 = st.columns(3)
        with col1:
            fornecedor_input = st.text_input("Fornecedor", value="Empresa Exemplo Lda")
        with col2:
            total_input = st.number_input("Valor Total (€)", value=125.50)
        with col3:
            data_input = st.text_input("Data da Fatura", value="2026-10-13")
            
        # Gráfico individual da fatura atual
        st.markdown("### 📊 Representação Gráfica do Valor Atual")
        df_chart = pd.DataFrame({
            "Categoria": ["Valor Total Registado"],
            "Montante (€)": [total_input]
        })
        st.bar_chart(df_chart.set_index("Categoria"))
            
        if st.button("💾 Guardar Fatura na Base de Dados"):
            if supabase:
                try:
                    data = {
                        "fornecedor": fornecedor_input,
                        "total": total_input,
                        "data_fatura": data_input,
                        "texto_extraido": texto_final[:500]
                    }
                    supabase.table("faturas").insert(data).execute()
                    st.success("Fatura processada e guardada com sucesso no Supabase!")
                except Exception as e:
                    st.error(f"Erro ao guardar na base de dados: {e}")
            else:
                st.warning("⚠️ Para guardar na base de dados, insere o teu URL e Chave real do Supabase na barra lateral.")

with aba2:
    st.subheader("Histórico e Evolução Mensal de Faturas")
    if supabase:
        try:
            response = supabase.table("faturas").select("*").execute()
            dados = response.data
            if dados:
                df_faturas = pd.DataFrame(dados)
                
                # Tratamento de datas e valores para o gráfico mensal
                if "data_fatura" in df_faturas.columns and "total" in df_faturas.columns:
                    df_faturas["data_fatura"] = pd.to_datetime(df_faturas["data_fatura"], errors="coerce")
                    df_faturas["Mes"] = df_faturas["data_fatura"].dt.to_period("M").astype(str)
                    
                    # Agrupamento por mês
                    df_mensal = df_faturas.groupby("Mes")["total"].sum().reset_index()
                    df_mensal = df_mensal.sort_values("Mes")
                    
                    st.markdown("### 📈 Evolução Mensal de Despesas (€)")
                    if not df_mensal.empty and df_mensal["total"].sum() > 0:
                        st.bar_chart(df_mensal.set_index("Mes")["total"])
                    else:
                        st.info("Ainda não há dados suficientes para gerar o gráfico mensal.")
                
                st.markdown("### 📋 Registo Detalhado")
                st.dataframe(df_faturas, use_container_width=True)
            else:
                st.info("Ainda não existem faturas guardadas na base de dados.")
        except Exception as e:
            st.error(f"Erro ao carregar o histórico: {e}")
    else:
        st.info("ℹ️ Insere o URL e a chave real do Supabase na barra lateral para visualizar o histórico e o gráfico mensal.")
