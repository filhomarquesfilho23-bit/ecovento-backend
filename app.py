import streamlit as st
from supabase import create_client

# Configurações do Supabase (URL e Chave corretos e completos)
SUPABASE_URL = "https://ufgmuayietkuwsobjszx.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVmZ211YXlpZXRrd3NvYmpzengiLCJyb2xlIjoiYW5vbiIsImlhdCI6MTcyOTE4MTgyODcsImV4cCI6MjEwNzM5NDI4N30.lKPqKNio5OXrrCtexfiuuK1eHQt5WFQbsszF_y860f4"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.title("📦 Vanguarda ERP - Gestão de Produtos")

# --- ADICIONAR NOVO PRODUTO ---
with st.expander("➕ Adicionar Novo Produto"):
    with st.form("form_novo_produto"):
        nome = st.text_input("Nome do Produto")
        preco = st.number_input("Preço (€)", min_value=0.0, format="%.2f")
        stock = st.number_input("Quantidade em Stock", min_value=0, step=1)
        submitted = st.form_submit_button("Guardar Produto")
        
        if submitted:
            if nome:
                try:
                    supabase.table("produtos").insert({
                        "nome": nome, 
                        "preco": preco, 
                        "stock": stock
                    }).execute()
                    st.success(f"Produto '{nome}' guardado com sucesso!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao guardar na base de dados: {e}")
            else:
                st.warning("Por favor, preenche o nome do produto.")

# --- LISTAR PRODUTOS ---
st.subheader("Lista de Produtos em Stock")
try:
    response = supabase.table("produtos").select("*").execute()
    produtos = response.data
    
    if produtos:
        st.dataframe(produtos, use_container_width=True)
    else:
        st.info("Ainda não existem produtos registados. Usa o botão acima para adicionar o primeiro!")
except Exception as e:
    st.error(f"Erro ao carregar produtos: {e}")
