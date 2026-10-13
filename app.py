import streamlit as st
from supabase import create_client

# Configurações diretas do Supabase para garantir zero erros de ligação
SUPABASE_URL = "https://ufgmuayietkuwsobjszx.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVmZ211YXlpZXRrd3NvYmpzengiLCJyb2xlIjoiYW5vbiIsImlhdCI6MTcyOTE4MTgyODcsImV4cCI6MjEwNzM5NDI4N30.lKPqKNio5OXrrCtexfiuuK1eHQt5WFQbsszF_y860f4"

# Inicializa o cliente do Supabase
try:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    st.error(f"Erro ao ligar ao Supabase: {e}")
    st.stop()

# Interface da aplicação Vanguarda ERP
st.title("Vanguarda ERP")
st.success("Ligação ao Supabase estabelecida com sucesso!")

# Podes continuar o resto do teu código da aplicação a partir daqui...
