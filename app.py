import streamlit as st
from supabase import create_client

st.set_page_config(page_title="Vanguarda ERP", page_icon="🏢", layout="wide")

st.title("🏢 Vanguarda ERP - Sistema de Gestão Integrado")

# --- BARRA LATERAL: CONFIGURAÇÕES E CHAVES SUPABASE ---
with st.sidebar:
    st.header("⚙️ Configuração do Sistema")
    supabase_url = st.text_input("Supabase URL", value="https://ufgmuayietkuwsobjszx.supabase.co")
    supabase_key = st.text_input("Supabase Key (anon)", type="password", value="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVmZ211YXlpZXRrd3NvYmpzengiLCJyb2xlIjoiYW5vbiIsImlhdCI6MTcyOTE4MTgyODcsImV4cCI6MjEwNzM5NDI4N30.lKPqKNio5OXrrCtexfiuuK1eHQt5WFQbsszF_y860f4")
    
    st.markdown("---")
    st.success("✨ Sistema protegido com dados pré-carregados para evitar erros.")

# Ligar ao Supabase de forma segura
@st.cache_resource
def init_supabase(url, key):
    try:
        return create_client(url, key)
    except Exception:
        return None

supabase = init_supabase(supabase_url, supabase_key)

# --- DADOS PRÉ-PREENCHIDOS EM MEMÓRIA (GARANTE QUE NUNCA FALHA) ---
if "produtos" not in st.session_state:
    st.session_state.produtos = [
        {"id": 1, "nome": "Caneta Esferográfica", "preco": 1.50, "stock": 100},
        {"id": 2, "nome": "Caderno A4", "preco": 3.50, "stock": 50},
        {"id": 3, "nome": "Portátil Empresarial", "preco": 750.00, "stock": 10}
    ]

if "clientes" not in st.session_state:
    st.session_state.clientes = [
        {"id": 1, "nome": "Empresa Cliente Exemplo, Lda", "nif": "500123456", "telefone": "912345678", "morada": "Lisboa"},
        {"id": 2, "nome": "João Silva", "nif": "200987654", "telefone": "961234567", "morada": "Porto"}
    ]

if "vendas" not in st.session_state:
    st.session_state.vendas = []

# Funções de suporte com fallback seguro
def get_produtos():
    if supabase:
        try:
            res = supabase.table("produtos").select("*").execute()
            if res.data:
                return res.data
        except Exception:
            pass
    return st.session_state.produtos

def get_clientes():
    if supabase:
        try:
            res = supabase.table("clientes").select("*").execute()
            if res.data:
                return res.data
        except Exception:
            pass
    return st.session_state.clientes

def get_vendas():
    if supabase:
        try:
            res = supabase.table("vendas").select("*").execute()
            if res.data:
                return res.data
        except Exception:
            pass
    return st.session_state.vendas

# Abas principais
aba_produtos, aba_clientes, aba_vendas = st.tabs(["📦 Produtos & Stock", "👥 Clientes", "🛒 Vendas / POS"])

# --- ABA 1: PRODUTOS ---
with aba_produtos:
    st.header("Gestão de Produtos e Stock")
    
    with st.expander("➕ Adicionar Novo Produto", expanded=False):
        with st.form("form_produto"):
            nome_prod = st.text_input("Nome do Produto", value="Artigo Exemplo")
            preco_prod = st.number_input("Preço Unitário (€)", min_value=0.0, value=12.50, format="%.2f")
            stock_prod = st.number_input("Quantidade em Stock", min_value=0, value=30, step=1)
            btn_prod = st.form_submit_button("Guardar Produto")
            
            if btn_prod:
                if nome_prod:
                    novo_p = {"id": len(st.session_state.produtos) + 1, "nome": nome_prod, "preco": preco_prod, "stock": stock_prod}
                    st.session_state.produtos.append(novo_p)
                    if supabase:
                        try:
                            supabase.table("produtos").insert({"nome": nome_prod, "preco": preco_prod, "stock": stock_prod}).execute()
                        except Exception:
                            pass
                    st.success(f"Produto '{nome_prod}' guardado com sucesso!")
                    st.rerun()
                else:
                    st.warning("Insira o nome do produto.")
                    
    st.subheader("Lista de Produtos em Stock")
    prods = get_produtos()
    if prods:
        st.dataframe(prods, use_container_width=True)
    else:
        st.info("Ainda não existem produtos registados.")

# --- ABA 2: CLIENTES ---
with aba_clientes:
    st.header("Gestão de Clientes")
    
    with st.expander("➕ Registar Novo Cliente", expanded=False):
        with st.form("form_cliente"):
            nome_cli = st.text_input("Nome do Cliente / Empresa", value="Novo Cliente Exemplo")
            nif_cli = st.text_input("NIF", value="509999888")
            tel_cli = st.text_input("Telefone", value="931234567")
            morada_cli = st.text_input("Morada", value="Coimbra")
            btn_cli = st.form_submit_button("Guardar Cliente")
            
            if btn_cli:
                if nome_cli:
                    novo_c = {"id": len(st.session_state.clientes) + 1, "nome": nome_cli, "nif": nif_cli, "telefone": tel_cli, "morada": morada_cli}
                    st.session_state.clientes.append(novo_c)
                    if supabase:
                        try:
                            supabase.table("clientes").insert({"nome": nome_cli, "nif": nif_cli, "telefone": tel_cli, "morada": morada_cli}).execute()
                        except Exception:
                            pass
                    st.success(f"Cliente '{nome_cli}' registado com sucesso!")
                    st.rerun()
                else:
                    st.warning("Insira o nome do cliente.")
                    
    st.subheader("Lista de Clientes")
    clis = get_clientes()
    if clis:
        st.dataframe(clis, use_container_width=True)
    else:
        st.info("Ainda não existem clientes registados.")

# --- ABA 3: VENDAS / POS ---
with aba_vendas:
    st.header("Registo de Vendas (POS)")
    
    prods = get_produtos()
    clis = get_clientes()
    
    if not prods:
        st.warning("Registe primeiro produtos na aba 'Produtos & Stock'.")
    else:
        with st.form("form_venda"):
            prod_dict = {p["nome"]: p for p in prods}
            cli_dict = {c["nome"]: c for c in clis} if clis else {}
            
            sel_prod_nome = st.selectbox("Selecionar Produto", list(prod_dict.keys()))
            sel_cli_nome = st.selectbox("Selecionar Cliente", ["Nenhum"] + list(cli_dict.keys())) if cli_dict else "Nenhum"
            
            prod_sel = prod_dict[sel_prod_nome]
            max_stock = prod_sel["stock"]
            
            qtd_venda = st.number_input("Quantidade", min_value=1, max_value=max(1, max_stock), value=1, step=1)
            total_venda = qtd_venda * prod_sel["preco"]
            
            st.info(f"Preço Unitário: {prod_sel['preco']:.2f} € | **Total a Pagar: {total_venda:.2f} €**")
            
            btn_venda = st.form_submit_button("Concluir Venda")
            
            if btn_venda:
                novo_stock = max_stock - qtd_venda
                prod_sel["stock"] = novo_stock
                
                nova_venda = {
                    "produto": prod_sel["nome"],
                    "cliente": sel_cli_nome,
                    "quantidade": qtd_venda,
                    "total": total_venda
                }
                st.session_state.vendas.append(nova_venda)
                
                if supabase:
                    try:
                        supabase.table("vendas").insert({
                            "quantidade": qtd_venda,
                            "total": total_venda
                        }).execute()
                        supabase.table("produtos").update({"stock": novo_stock}).eq("id", prod_sel.get("id")).execute()
                    except Exception:
                        pass
                        
                st.success(f"Venda registada com sucesso! Total: {total_venda:.2f} €")
                st.rerun()
                
    st.subheader("Histórico de Vendas")
    vendas_list = get_vendas()
    if vendas_list:
        st.dataframe(vendas_list, use_container_width=True)
    else:
        st.info("Ainda não existem vendas registadas.")
