import streamlit as st
from supabase import create_client

# Configurações do Supabase
SUPABASE_URL = "https://ufgmuayietkuwsobjszx.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVmZ211YXlpZXRrd3NvYmpzengiLCJyb2xlIjoiYW5vbiIsImlhdCI6MTcyOTE4MTgyODcsImV4cCI6MjEwNzM5NDI4N30.lKPqKNio5OXrrCtexfiuuK1eHQt5WFQbsszF_y860f4"

try:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    st.error(f"Erro ao ligar ao Supabase: {e}")

st.set_page_config(page_title="Vanguarda ERP", page_icon="🏢", layout="wide")
st.title("🏢 Vanguarda ERP - Sistema de Gestão Integrado")

# Abas principais do ERP
aba_produtos, aba_clientes, aba_vendas = st.tabs(["📦 Produtos & Stock", "👥 Clientes", "🛒 Vendas / POS"])

# --- ABA 1: PRODUTOS ---
with aba_produtos:
    st.header("Gestão de Produtos e Stock")
    
    with st.expander("➕ Adicionar Novo Produto"):
        with st.form("form_produto"):
            nome_prod = st.text_input("Nome do Produto")
            preco_prod = st.number_input("Preço Unitário (€)", min_value=0.0, format="%.2f")
            stock_prod = st.number_input("Quantidade em Stock", min_value=0, step=1)
            btn_prod = st.form_submit_button("Guardar Produto")
            
            if btn_prod:
                if nome_prod:
                    try:
                        supabase.table("produtos").insert({
                            "nome": nome_prod,
                            "preco": preco_prod,
                            "stock": stock_prod
                        }).execute()
                        st.success(f"Produto '{nome_prod}' guardado com sucesso!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erro ao guardar produto: {e}")
                else:
                    st.warning("Insira o nome do produto.")
                    
    st.subheader("Lista de Produtos em Stock")
    try:
        res_prod = supabase.table("produtos").select("*").execute()
        produtos = res_prod.data
        if produtos:
            st.dataframe(produtos, use_container_width=True)
        else:
            st.info("Ainda não existem produtos registados.")
    except Exception as e:
        st.error(f"Erro ao carregar produtos: {e}")

# --- ABA 2: CLIENTES ---
with aba_clientes:
    st.header("Gestão de Clientes")
    
    with st.expander("➕ Registar Novo Cliente"):
        with st.form("form_cliente"):
            nome_cli = st.text_input("Nome do Cliente / Empresa")
            nif_cli = st.text_input("NIF")
            tel_cli = st.text_input("Telefone")
            morada_cli = st.text_input("Morada")
            btn_cli = st.form_submit_button("Guardar Cliente")
            
            if btn_cli:
                if nome_cli:
                    try:
                        supabase.table("clientes").insert({
                            "nome": nome_cli,
                            "nif": nif_cli,
                            "telefone": tel_cli,
                            "morada": morada_cli
                        }).execute()
                        st.success(f"Cliente '{nome_cli}' registado com sucesso!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erro ao guardar cliente: {e}")
                else:
                    st.warning("Insira o nome do cliente.")
                    
    st.subheader("Lista de Clientes")
    try:
        res_cli = supabase.table("clientes").select("*").execute()
        clientes = res_cli.data
        if clientes:
            st.dataframe(clientes, use_container_width=True)
        else:
            st.info("Ainda não existem clientes registados.")
    except Exception as e:
        st.error(f"Erro ao carregar clientes: {e}")

# --- ABA 3: VENDAS / POS ---
with aba_vendas:
    st.header("Registo de Vendas (POS)")
    
    try:
        p_res = supabase.table("produtos").select("*").execute()
        c_res = supabase.table("clientes").select("*").execute()
        
        lista_produtos = p_res.data or []
        lista_clientes = c_res.data or []
        
        if not lista_produtos:
            st.warning("Registe primeiro produtos na aba 'Produtos & Stock' para poder efetuar vendas.")
        else:
            with st.form("form_venda"):
                prod_dict = {p["nome"]: p for p in lista_produtos}
                cli_dict = {c["nome"]: c for c in lista_clientes} if lista_clientes else {}
                
                sel_prod_nome = st.selectbox("Selecionar Produto", list(prod_dict.keys()))
                sel_cli_nome = st.selectbox("Selecionar Cliente (Opcional)", ["Nenhum"] + list(cli_dict.keys())) if cli_dict else "Nenhum"
                
                prod_selecionado = prod_dict[sel_prod_nome]
                max_stock = prod_selecionado["stock"]
                
                qtd_venda = st.number_input("Quantidade", min_value=1, max_value=max(1, max_stock), step=1)
                
                total_venda = qtd_venda * prod_selecionado["preco"]
                st.info(f"Preço Unitário: {prod_selecionado['preco']:.2f} € | **Total a Pagar: {total_venda:.2f} €**")
                
                btn_venda = st.form_submit_button("Concluir Venda")
                
                if btn_venda:
                    cliente_id = cli_dict[sel_cli_nome]["id"] if sel_cli_nome != "Nenhum" else None
                    novo_stock = max_stock - qtd_venda
                    
                    try:
                        # Registar a venda
                        supabase.table("vendas").insert({
                            "produto_id": prod_selecionado["id"],
                            "cliente_id": cliente_id,
                            "quantidade": qtd_venda,
                            "total": total_venda
                        }).execute()
                        
                        # Atualizar o stock automaticamente
                        supabase.table("produtos").update({"stock": novo_stock}).eq("id", prod_selecionado["id"]).execute()
                        
                        st.success(f"Venda registada com sucesso! Total: {total_venda:.2f} €")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erro ao processar venda: {e}")
                        
        st.subheader("Histórico de Vendas")
        res_vendas = supabase.table("vendas").select("*").execute()
        vendas_data = res_vendas.data
        if vendas_data:
            st.dataframe(vendas_data, use_container_width=True)
        else:
            st.info("Ainda não existem vendas registadas.")
            
    except Exception as e:
        st.error(f"Erro ao carregar o módulo de vendas: {e}")
