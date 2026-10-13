import streamlit as st
from supabase import create_client

# Tenta ler dos secrets do Streamlit, mas se falhar ou estiver vazio, pede na barra lateral
supabase_config = st.secrets.get("supabase", {})
default_url = supabase_config.get("url", "https://ufgmuayietkuwsobjszx.supabase.co")
default_key = supabase_config.get("key", "")

st.sidebar.header("Configuração Supabase")
url = st.sidebar.text_input("Supabase URL", value=default_url)
key = st.sidebar.text_input("Supabase Key (anon)", value=default_key, type="password")

if not url or not key:
    st.warning("Por favor, insere o URL e a chave 'anon' do Supabase na barra lateral à esquerda para continuar.")
    st.stop()

# Inicializa o cliente do Supabase
supabase = create_client(url, key)
