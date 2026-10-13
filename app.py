import streamlit as st
import pandas as pd
from supabase import create_client
from fpdf import FPDF

st.set_page_config(page_title="Vanguarda ERP", page_icon="🏢", layout="wide")

st.title("🏢 Vanguarda ERP - Sistema de Gestão Integrado")

# --- BARRA LATERAL: CONFIGURAÇÕES E APRESENTAÇÃO DO PROJETO ---
with st.sidebar:
    st.header("⚙️ Configuração do Sistema")
    supabase_url = st.text_input("Supabase URL", value="https://ufgmuayietkuwsobjszx.supabase.co")
    supabase_key = st.text_input("Supabase Key (anon)", type="password", value="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVmZ211YXlpZXRrd3NvYmpzengiLCJyb2xlIjoiYW5vbiIsImlhdCI6MTcyOTE4MTgyODcsImV4cCI6MjEwNzM5NDI4N30.lKPqKNio5OXrrCtexfiuuK1eHQt5WFQbsszF_y860f4")
    
    st.markdown("---")
    st.header("📌 Sobre o Projeto")
    st.markdown("""
    **Vanguarda ERP** é uma solução moderna desenvolvida de raiz para otimizar a gestão de stock, clientes e pontos de venda (POS).
    
    * **⏱️ Tempo de Desenvolvimento:** 1 Dia (Desenvolvimento Ágil e Inovador)
    * **💎 Valor de Mercado Estimado:** 3.500,00 € a 5.000,00 €
    * **🚀 Tecnologias:** Python, Streamlit, Supabase, FPDF
    """)
    
    st.markdown("---")
    st.markdown("🔗 **Link de Acesso Direto:**")
    st.markdown("[Abrir Vanguarda ERP](https://cno7v.streamlit.app)", unsafe_allow_html=True)

@st.cache_resource
def init_supabase(url, key):
    try:
        return create_client(url, key)
    except Exception:
        return None

supabase = init_supabase(supabase_url, supabase_key)

# --- DADOS PRÉ-PREENCHIDOS EM MEMÓRIA ---
if "produtos" not in st.session_state:
    st.session_state.produtos = [
        {"id": 1, "nome": "Caneta Esferográfica", "preco": 1.50, "stock": 100},
        {"id": 2, "nome": "Caderno A4", "preco": 3.50, "stock": 50},
        {"id": 3, "nome": "Portátil Empresarial", "preco": 750.00, "stock": 10},
        {"id": 4, "nome": "Papel A4 (Resma)", "preco": 4.20, "stock": 80}
    ]

if "clientes" not in st.session_state:
    st.session_state.clientes = [
        {"id": 1, "nome": "Empresa Cliente Exemplo, Lda", "nif": "500123456", "telefone": "912345678", "morada": "Lisboa"},
        {"id": 2, "nome": "João Silva", "nif": "200987654", "telefone": "961234567", "morada": "Porto"},
        {"id": 3, "nome": "Tech Solutions, S.A.", "nif": "509888777", "telefone": "933444555", "morada": "Coimbra"}
    ]

if "vendas" not in st.session_state:
    st.session_state.vendas = [
        {"produto": "Caneta Esferográfica", "cliente": "João Silva", "quantidade": 5, "total": 7.50},
        {"produto": "Caderno A4", "cliente": "Tech Solutions, S.A.", "quantidade": 2, "total": 7.00}
    ]

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

def gerar_pdf_vendas(vendas):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Vanguarda ERP - Relatorio de Vendas", 0, 1, "C")
    pdf.ln(10)
    
    pdf.set_font("Arial", "B", 11)
    pdf.cell(65, 10, "Produto", 1)
    pdf.cell(65, 10, "Cliente", 1)
    pdf.cell(25, 10, "Qtd", 1)
    pdf.cell(35, 10, "Total (EUR)", 1)
    pdf.ln()
    
    pdf.set_font("Arial", "", 10)
    for v in vendas:
        pdf.cell(65, 10, str(v.get("produto", "-")), 1)
        pdf.cell(65, 10, str(v.get("cliente", "-")), 1)
        pdf.cell(25, 10, str(v.get("quantidade", 0)), 1)
        pdf.cell(35, 10, f"{v.get('total', 0):.2f}", 1)
        pdf.ln()
        
    return pdf.output(dest='S').encode('latin1', errors='ignore')

# Abas principais
aba_produtos, aba_clientes, aba_vendas = st.tabs(["📦 Produtos & Stock", "👥 Clientes", "🛒 Vendas / POS & PDF"])

# --- ABA 1: PRODUTOS ---
with aba_produtos:
    st.header("Gestão de Produtos e Stock")
    
    with st.expander("➕ Adicionar Novo Produto", expanded=False):
        with st.form("form_produto"):
            nome_prod = st.text_input("Nome do Produto", value="Rato Sem Fios")
            preco_prod = st.number_input("Preço Unitário (€)", min_value=0.0, value=19.99, format="%.2f")
            stock_prod = st.number_input("Quantidade em Stock", min_value=0, value=45, step=1)
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
        df_prod = pd.DataFrame(prods)
        st.dataframe(df_prod, use_container_width=True)
        
        st.markdown("### 📊 Gráfico de Stock por Produto")
        st.bar_chart(df_prod.set_index("nome")["stock"])
    else:
        st.info("Ainda não existem produtos registados.")

# --- ABA 2: CLIENTES ---
with aba_clientes:
    st.header("Gestão de Clientes")
    
    with st.expander("➕ Registar Novo Cliente", expanded=False):
        with st.form("form_cliente"):
            nome_cli = st.text_input("Nome do Cliente / Empresa", value="Inovação Digital, Lda")
            nif_cli = st.text_input("NIF", value="508888999")
            tel_cli = st.text_input("Telefone", value="919888777")
            morada_cli = st.text_input("Morada", value="Braga")
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
        df_cli = pd.DataFrame(clis)
        st.dataframe(df_cli, use_container_width=True)
        
        st.markdown("### 📊 Distribuição de Clientes por Localização")
        if "morada" in df_cli.columns:
            st.bar_chart(df_cli["morada"].value_counts())
    else:
        st.info("Ainda não existem clientes registados.")

# --- ABA 3: VENDAS / POS & PDF ---
with aba_vendas:
    st.header("Registo de Vendas (POS) & Relatórios PDF")
    
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
                
    st.subheader("Histórico de Vendas e Faturação")
    vendas_list = get_vendas()
    if vendas_list:
        df_vendas = pd.DataFrame(vendas_list)
        st.dataframe(df_vendas, use_container_width=True)
        
        st.markdown("### 📊 Gráfico de Faturação por Venda (€)")
        if "total" in df_vendas.columns:
            st.bar_chart(df_vendas["total"])
            
        st.markdown("---")
        st.subheader("📄 Exportar Relatório de Vendas")
        try:
            pdf_bytes = gerar_pdf_vendas(vendas_list)
            st.download_button(
                label="📥 Descarregar Relatório de Vendas em PDF",
                data=pdf_bytes,
                file_name="relatorio_vendas_vanguarda.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"Erro ao gerar PDF: {e}")
    else:
        st.info("Ainda não existem vendas registadas.")
