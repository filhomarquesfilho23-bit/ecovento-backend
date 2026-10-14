import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import streamlit.components.v1 as components
import hashlib

# Configuração da página para telemóvel
st.set_page_config(
    page_title="OmniFlux Pro - Multi-utilizador",
    page_icon="⚡",
    layout="centered"
)

# --- FUNÇÃO PARA ENCRIPITAR PASSWORDS ---
def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

# --- BASE DE DADOS HÍBRIDA (NOVA VERSÃO V2) ---
def init_db():
    conn = sqlite3.connect('omniflux_pro_v2.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS utilizadores (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS notas (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, texto TEXT, data TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS tarefas (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, tarefa TEXT, concluida INTEGER, data TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS transacoes (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, tipo TEXT, valor REAL, descricao TEXT, data TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS equipa (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, nome TEXT, cargo TEXT, salario REAL, data TEXT)''')
    
    # Criar um utilizador de exemplo padrão se a tabela estiver vazia
    c.execute("SELECT COUNT(*) FROM utilizadores")
    if c.fetchone()[0] == 0:
        pass_exemplo = hash_password("1234")
        c.execute("INSERT INTO utilizadores (username, password) VALUES (?, ?)", ("admin", pass_exemplo))
        
        # Inserir dados de exemplo para o admin
        c.execute("INSERT INTO tarefas (username, tarefa, concluida, data) VALUES (?, ?, ?, ?)", ("admin", "Lançar nova versão do OmniFlux Pro", 0, datetime.now().strftime("%Y-%m-%d")))
        c.execute("INSERT INTO equipa (username, nome, cargo, salario, data) VALUES (?, ?, ?, ?, ?)", ("admin", "Ana Silva", "Arquiteta de Software IA", 2200.0, datetime.now().strftime("%Y-%m-%d")))
        c.execute("INSERT INTO transacoes (username, tipo, valor, descricao, data) VALUES (?, ?, ?, ?, ?)", ("admin", "Receita", 1500.0, "Consultoria Inicial", datetime.now().strftime("%Y-%m-%d")))
        c.execute("INSERT INTO notas (username, texto, data) VALUES (?, ?, ?)", ("admin", "Sistema operativo líquido com multi-utilizador ativo.", datetime.now().strftime("%Y-%m-%d %H:%M")))

    conn.commit()
    conn.close()

init_db()

# --- GESTÃO DE SESSÃO DE AUTENTICAÇÃO ---
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False
if "user_atual" not in st.session_state:
    st.session_state.user_atual = ""

# --- CAPTURAR VOZ VIA URL PARAMS ---
query_params = st.query_params
intencao_voz = ""
if "intencao" in query_params:
    intencao_voz = query_params["intencao"]
    st.query_params.clear()

# --- FUNÇÕES DE DADOS FILTRADAS POR UTILIZADOR ---
def guardar_nota(user, texto):
    conn = sqlite3.connect('omniflux_pro_v2.db')
    c = conn.cursor()
    c.execute("INSERT INTO notas (username, texto, data) VALUES (?, ?, ?)", (user, texto, datetime.now().strftime("%Y-%m-%d %H:%M")))
    conn.commit()
    conn.close()

def obter_notas(user):
    conn = sqlite3.connect('omniflux_pro_v2.db')
    df = pd.read_sql_query("SELECT * FROM notas WHERE username = ? ORDER BY id DESC", conn, params=(user,))
    conn.close()
    return df

def guardar_tarefa(user, tarefa):
    conn = sqlite3.connect('omniflux_pro_v2.db')
    c = conn.cursor()
    c.execute("INSERT INTO tarefas (username, tarefa, concluida, data) VALUES (?, ?, 0, ?)", (user, tarefa, datetime.now().strftime("%Y-%m-%d")))
    conn.commit()
    conn.close()

def obter_tarefas(user):
    conn = sqlite3.connect('omniflux_pro_v2.db')
    df = pd.read_sql_query("SELECT * FROM tarefas WHERE username = ? ORDER BY id DESC", conn, params=(user,))
    conn.close()
    return df

def atualizar_estado_tarefa(tarefa_id, concluida):
    conn = sqlite3.connect('omniflux_pro_v2.db')
    c = conn.cursor()
    c.execute("UPDATE tarefas SET concluida = ? WHERE id = ?", (1 if concluida else 0, tarefa_id))
    conn.commit()
    conn.close()

def guardar_transacao(user, tipo, valor, descricao):
    conn = sqlite3.connect('omniflux_pro_v2.db')
    c = conn.cursor()
    c.execute("INSERT INTO transacoes (username, tipo, valor, descricao, data) VALUES (?, ?, ?, ?, ?)", 
              (user, tipo, valor, descricao, datetime.now().strftime("%Y-%m-%d")))
    conn.commit()
    conn.close()

def obter_transacoes(user):
    conn = sqlite3.connect('omniflux_pro_v2.db')
    df = pd.read_sql_query("SELECT * FROM transacoes WHERE username = ? ORDER BY id DESC", conn, params=(user,))
    conn.close()
    return df

def guardar_membro(user, nome, cargo, salario):
    conn = sqlite3.connect('omniflux_pro_v2.db')
    c = conn.cursor()
    c.execute("INSERT INTO equipa (username, nome, cargo, salario, data) VALUES (?, ?, ?, ?, ?)", 
              (user, nome, cargo, salario, datetime.now().strftime("%Y-%m-%d")))
    conn.commit()
    conn.close()

def obter_equipa(user):
    conn = sqlite3.connect('omniflux_pro_v2.db')
    df = pd.read_sql_query("SELECT * FROM equipa WHERE username = ? ORDER BY id DESC", conn, params=(user,))
    conn.close()
    return df

# --- ESTILO AZUL FUTURISTA TOTALMENTE PREENCHIDO ---
st.markdown("""
    <style>
    .stApp {
        background-color: #0b1329;
        color: #ffffff;
    }
    h1, h2, h3 {
        color: #38bdf8 !important;
        font-family: -apple-system, BlinkMacSystemFont, sans-serif;
    }
    .stTextInput input, .stTextArea textarea, .stNumberInput input, .stSelectbox select {
        background-color: #1e293b !important;
        color: #ffffff !important;
        border: 1px solid #38bdf8 !important;
        border-radius: 8px;
    }
    .stButton button, div.stFormSubmitButton > button {
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%) !important;
        color: #ffffff !important;
        border: 1px solid #38bdf8 !important;
        border-radius: 8px;
        font-weight: bold;
        width: 100%;
        padding: 0.6rem 1rem;
        box-shadow: 0 4px 12px rgba(14, 165, 233, 0.4);
    }
    .stButton button:hover, div.stFormSubmitButton > button:hover {
        background: linear-gradient(135deg, #38bdf8 0%, #0284c7 100%) !important;
        color: #ffffff !important;
    }
    .stSuccess, .stInfo, .stWarning, .stError {
        background-color: #1e293b !important;
        border: 1px solid #38bdf8 !important;
        color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ OmniFlux Pro")
st.caption("Sistema Operativo Líquido • Segurança & Controlo Multi-utilizador.")

# --- ECRA DE LOGIN / REGISTO SE O UTILIZADOR NÃO ESTIVER AUTENTICADO ---
if not st.session_state.autenticado:
    tab_login, tab_registo = st.tabs(["🔐 Iniciar Sessão", "📝 Criar Conta"])
    
    with tab_login:
        with st.form("form_login"):
            username_input = st.text_input("Utilizador", placeholder="Ex: admin")
            password_input = st.text_input("Palavra-passe", type="password", placeholder="Ex: 1234")
            btn_entrar = st.form_submit_button("Entrar no Sistema")
            
            if btn_entrar:
                conn = sqlite3.connect('omniflux_pro_v2.db')
                c = conn.cursor()
                hashed_pass = hash_password(password_input)
                c.execute("SELECT * FROM utilizadores WHERE username = ? AND password = ?", (username_input, hashed_pass))
                user_encontrado = c.fetchone()
                conn.close()
                
                if user_encontrado:
                    st.session_state.autenticado = True
                    st.session_state.user_atual = username_input
                    st.success("Sessão iniciada com sucesso!")
                    st.rerun()
                else:
                    st.error("Utilizador ou palavra-passe incorretos.")

    with tab_registo:
        with st.form("form_registo"):
            novo_user = st.text_input("Escolha um Utilizador", placeholder="Ex: joao_silva")
            nova_pass = st.text_input("Escolha uma Palavra-passe", type="password")
            btn_registar_conta = st.form_submit_button("Criar Nova Conta")
            
            if btn_registar_conta:
                if novo_user.strip() and nova_pass.strip():
                    try:
                        conn = sqlite3.connect('omniflux_pro_v2.db')
                        c = conn.cursor()
                        hashed_pass = hash_password(nova_pass)
                        c.execute("INSERT INTO utilizadores (username, password) VALUES (?, ?)", (novo_user, hashed_pass))
                        conn.commit()
                        conn.close()
                        st.success("Conta criada com sucesso! Podes agora iniciar sessão na aba ao lado.")
                    except sqlite3.IntegrityError:
                        st.warning("Esse nome de utilizador já existe. Escolhe outro.")
                else:
                    st.warning("Preenche todos os campos.")

else:
    # --- APLICAÇÃO PRINCIPAL APÓS LOGIN ---
    user = st.session_state.user_atual
    
    col_info, col_logout = st.columns([3, 1])
    with col_info:
        st.info(f"👤 Utilizador Ativo: **{user}**")
    with col_logout:
        if st.button("Sair"):
            st.session_state.autenticado = False
            st.session_state.user_atual = ""
            st.rerun()

    # --- COMPONENTE DE VOZ NATIVO ---
    st.markdown("### 🎙️ Assistente de Voz Inteligente")
    voice_component = """
    <div style="text-align: center; margin-bottom: 15px;">
        <button onclick="startListening()" style="background: linear-gradient(135deg, #f43f5e 0%, #e11d48 100%); color: white; border: none; border-radius: 25px; padding: 12px 24px; font-weight: bold; font-size: 16px; box-shadow: 0 4px 15px rgba(244, 63, 94, 0.4); cursor: pointer; width: 100%;">
            🎤 Tocar para Falar com o OmniFlux
        </button>
        <p id="status" style="color: #38bdf8; font-size: 13px; margin-top: 8px;">Diga um comando (ex: finanças, equipa, tarefas, relatórios)...</p>
    </div>

    <script>
    function startListening() {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!SpeechRecognition) {
            alert("O seu browser não suporta reconhecimento de voz direto.");
            return;
        }
        const recognition = new SpeechRecognition();
        recognition.lang = 'pt-PT';
        recognition.interimResults = false;
        
        document.getElementById("status").innerText = "A escutar a sua voz...";
        
        recognition.onresult = function(event) {
            const speechToText = event.results[0][0].transcript;
            document.getElementById("status").innerText = "Comando detetado: " + speechToText;
            
            setTimeout(() => {
                const baseUrl = window.parent.location.origin + window.parent.location.pathname;
                window.parent.location.href = baseUrl + '?intencao=' + encodeURIComponent(speechToText);
            }, 400);
        };
        
        recognition.onerror = function(event) {
            document.getElementById("status").innerText = "Erro ao escutar. Tente novamente.";
        };
        
        recognition.start();
    }
    </script>
    """
    components.html(voice_component, height=100)

    # --- IA SEMÂNTICA DE VOZ AVANÇADA ---
    if "intencao_atual" not in st.session_state:
        st.session_state.intencao_atual = "dashboard"

    if intencao_voz:
        t = intencao_voz.lower()
        if any(k in t for k in ["finan", "kit", "dinheiro", "orçamento", "gasto", "fatura"]):
            st.session_state.intencao_atual = "financeiro"
        elif any(k in t for k in ["equip", "colaborador", "salario", "membro"]):
            st.session_state.intencao_atual = "equipa"
        elif any(k in t for k in ["tarefa", "nota", "fazer", "trabalho", "projeto"]):
            st.session_state.intencao_atual = "tarefas_notas"
        elif any(k in t for k in ["relatório", "exportar", "nuvem", "cloud"]):
            st.session_state.intencao_atual = "relatorios"
        else:
            st.session_state.intencao_atual = "dashboard"
        st.info(f"🎙️ **Comando de Voz Detetado:** \"{intencao_voz}\" ➔ Módulo Ativado!")

    st.markdown("### 🎛️ Painel de Controlo Rápido")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🏠 Dashboard"):
            st.session_state.intencao_atual = "dashboard"
        if st.button("💰 Finanças"):
            st.session_state.intencao_atual = "financeiro"
    with col2:
        if st.button("👥 Equipa"):
            st.session_state.intencao_atual = "equipa"
        if st.button("📊 Relatórios & Nuvem"):
            st.session_state.intencao_atual = "relatorios"

    if st.button("📋 Aceder a Tarefas & Notas"):
        st.session_state.intencao_atual = "tarefas_notas"

    modulo_ativo = st.session_state.intencao_atual
    st.markdown("---")

    # --- 1. DASHBOARD COM ALERTAS INTELIGENTES ---
    if modulo_ativo == "dashboard":
        st.success("💧 Dashboard Dinâmico Personalizado")
        
        df_t = obter_tarefas(user)
        total_tarefas = len(df_t) if not df_t.empty else 0
        pendentes = len(df_t[df_t['concluida'] == 0]) if not df_t.empty else 0
        concluidas = total_tarefas - pendentes
        
        df_fin = obter_transacoes(user)
        total_receitas = df_fin[df_fin['tipo'] == 'Receita']['valor'].sum() if not df_fin.empty else 0.0
        total_despesas = df_fin[df_fin['tipo'] == 'Despesa']['valor'].sum() if not df_fin.empty else 0.0
        
        df_eq = obter_equipa(user)
        total_membros = len(df_eq) if not df_eq.empty else 0
        
        saldo_liquido = 4850.0 + total_receitas - total_despesas

        st.markdown("### 🔔 Centro de Alertas do Sistema")
        if total_despesas > total_receitas:
            st.error("🚨 **Alerta Financeiro:** As despesas registadas superam as receitas atuais!")
        elif pendentes > 2:
            st.warning(f"⚠️ **Atenção:** Tens {pendentes} tarefas pendentes acumuladas que requerem atenção.")
        else:
            st.success("✅ **Sistema Otimizado:** Indicadores operacionais saudáveis e equilibrados.")

        c1, c2 = st.columns(2)
        with c1:
            st.metric("Saldo Líquido", f"{saldo_liquido:,.2f} €")
        with c2:
            st.metric("Tarefas Pendentes", f"{pendentes}")

        st.markdown("### 📊 Gráficos de Atividade do Sistema")
        df_chart_fin = pd.DataFrame({
            "Fluxo": ["Receitas", "Despesas"],
            "Montante (€)": [total_receitas, total_despesas]
        }).set_index("Fluxo")
        st.bar_chart(df_chart_fin)

    # --- 2. MÓDULO FINANCEIRO ---
    elif modulo_ativo == "financeiro":
        st.success("💧 Módulo Financeiro Interativo")
        
        with st.form("form_financas"):
            st.markdown("**Registar Movimento Financeiro:**")
            tipo_mov = st.selectbox("Tipo", ["Receita", "Despesa"])
            valor_mov = st.number_input("Valor (€)", min_value=0.0, value=100.0)
            desc_mov = st.text_input("Descrição", placeholder="Ex: Venda de serviço, Assinatura...")
            btn_registar = st.form_submit_button("Adicionar ao Sistema")
            
            if btn_registar:
                guardar_transacao(user, tipo_mov, valor_mov, desc_mov)
                st.success("Movimento financeiro registado com sucesso!")
                st.rerun()

        df_fin = obter_transacoes(user)
        st.markdown("### 📊 Histórico de Transações")
        if not df_fin.empty:
            st.dataframe(df_fin[['data', 'tipo', 'descricao', 'valor']], use_container_width=True)
        else:
            st.write("Ainda sem transações registadas.")

    # --- 3. MÓDULO DE EQUIPA ---
    elif modulo_ativo == "equipa":
        st.warning("💧 Módulo de Recursos Humanos e Talento")
        
        with st.form("form_equipa"):
            st.markdown("**Adicionar Novo Colaborador:**")
            nome_colab = st.text_input("Nome do Colaborador", value="Exemplo: João Pereira")
            cargo_colab = st.text_input("Cargo / Função", value="Exemplo: Gestor de Projetos")
            salario_colab = st.number_input("Salário Mensal Bruto (€)", min_value=0.0, value=1600.0)
            btn_colab = st.form_submit_button("Contratar / Registar Colaborador")
            
            if btn_colab:
                if nome_colab.strip():
                    guardar_membro(user, nome_colab, cargo_colab, salario_colab)
                    st.success(f"Colaborador {nome_colab} registado com sucesso!")
                    st.rerun()
                else:
                    st.warning("Indica o nome do colaborador.")

        st.markdown("### 👥 Equipa Ativa & Custos Anuais")
        df_eq = obter_equipa(user)
        if not df_eq.empty:
            for index, row in df_eq.iterrows():
                custo_anual = row['salario'] * 14
                st.info(f"**{row['nome']}** ({row['cargo']}) — Salário: {row['salario']:,.2f} €/mês | Custo Anual (14 meses): **{custo_anual:,.2f} €**")
        else:
            st.write("Ainda não existem colaboradores registados.")

    # --- 4. MÓDULO DE RELATÓRIOS & EXPORTAÇÃO ---
    elif modulo_ativo == "relatorios":
        st.info("📊 Módulo de Relatórios Executivos & Nuvem")
        st.markdown("Podes descarregar o **Relatório Executivo** em formato CSV com os teus dados consolidados.")
        
        df_trans = obter_transacoes(user)
        if not df_trans.empty:
            csv_global = df_trans.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Descarregar Relatório Executivo (CSV)",
                data=csv_global,
                file_name=f"relatorio_{user}.csv",
                mime="text/csv"
            )
        else:
            st.write("Ainda não há dados suficientes para exportação.")

    # --- 5. MÓDULO DE TAREFAS & NOTAS ---
    elif modulo_ativo == "tarefas_notas":
        st.info("💧 Módulo Unificado de Tarefas e Memória")
        
        tab1, tab2 = st.tabs(["📋 Tarefas", "📝 Notas"])
        
        with tab1:
            nova_t = st.text_input("Adicionar nova prioridade:", value="Exemplo: Rever orçamento mensal")
            if st.button("Registar Tarefa"):
                if nova_t.strip():
                    guardar_tarefa(user, nova_t)
                    st.success("Tarefa guardada!")
                    st.rerun()
                else:
                    st.warning("Escreve uma tarefa.")
                    
            df_t = obter_tarefas(user)
            if not df_t.empty:
                for index, row in df_t.iterrows():
                    concluida_atual = bool(row['concluida'])
                    novo_estado = st.checkbox(f"[{row['data']}] {row['tarefa']}", value=concluida_atual, key=f"t_{row['id']}")
                    if novo_estado != concluida_atual:
                        atualizar_estado_tarefa(row['id'], novo_estado)
                        st.rerun()
            else:
                st.write("Sem tarefas.")
                
        with tab2:
            texto_nota = st.text_area("Regista o teu pensamento:", value="Exemplo: Nota importante gravada no sistema.")
            if st.button("Salvar Nota"):
                if texto_nota.strip():
                    guardar_nota(user, texto_nota)
                    st.success("Nota gravada!")
                    st.rerun()
                else:
                    st.warning("Escreve algo.")
                    
            df_notas = obter_notas(user)
            if not df_notas.empty:
                for index, row in df_notas.iterrows():
                    st.info(f"[{row['data']}] {row['texto']}")
                
                csv_data = df_notas.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Descarregar Notas CSV", data=csv_data, file_name=f"notas_{user}.csv", mime="text/csv")
            else:
                st.write("Sem notas.")

st.markdown("---")
st.caption("OmniFlux Pro • Multi-utilizador Ativo ⚡")
