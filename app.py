from datetime import datetime
import numpy as np
import pandas as pd
import sqlite3
import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Micro-Habit Mesh - Otimizador de Rotina",
    page_icon="⚡",
    layout="wide",
)


# Inicializar Base de Dados SQLite
def init_db():
  conn = sqlite3.connect("micro_habit_mesh.db", check_same_thread=False)
  c = conn.cursor()
  c.execute("""
        CREATE TABLE IF NOT EXISTS energy_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            energy_level INTEGER,
            mood TEXT
        )
    """)
  c.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            energy_required TEXT,
            status TEXT
        )
    """)
  conn.commit()
  conn.close()


init_db()


# Funções de base de dados
def log_energy(level, mood):
  conn = sqlite3.connect("micro_habit_mesh.db", check_same_thread=False)
  c = conn.cursor()
  c.execute(
      "INSERT INTO energy_logs (timestamp, energy_level, mood) VALUES (?, ?,"
      " ?)",
      (datetime.now().strftime("%Y-%m-%d %H:%M"), level, mood),
  )
  conn.commit()
  conn.close()


def add_task(title, energy_required):
  conn = sqlite3.connect("micro_habit_mesh.db", check_same_thread=False)
  c = conn.cursor()
  c.execute(
      "INSERT INTO tasks (title, energy_required, status) VALUES (?, ?, ?)",
      (title, energy_required, "Pendente"),
  )
  conn.commit()
  conn.close()


def get_tasks():
  conn = sqlite3.connect("micro_habit_mesh.db", check_same_thread=False)
  c = conn.cursor()
  c.execute("SELECT id, title, energy_required, status FROM tasks")
  rows = c.fetchall()
  conn.close()
  return rows


def update_task_status(task_id, status):
  conn = sqlite3.connect("micro_habit_mesh.db", check_same_thread=False)
  c = conn.cursor()
  c.execute("UPDATE tasks SET status = ? WHERE id = ?", (status, task_id))
  conn.commit()
  conn.close()


# Interface Principal (Streamlit)
st.title("⚡ Micro-Habit Mesh")
st.markdown(
    "### O seu Otimizador Dinâmico de Rotina e Energia Baseado em IA"
)

# Painel Lateral para Registo de Energia
st.sidebar.header("🧠 Como está a sua energia?")
energy_level = st.sidebar.slider(
    "Nível de Foco / Energia (1 a 5)", 1, 5, 3, help="1 = Exausto, 5 = No topo"
)
mood = st.sidebar.selectbox(
    "Estado de espírito", ["Focado", "Cansado", "Ansioso", "Criativo", "Neutro"]
)

if st.sidebar.button("Registar Estado de Energia"):
  log_energy(energy_level, mood)
  st.sidebar.success("Estado registado com sucesso!")

# Layout em Separadores
tab1, tab2, tab3 = st.tabs(
    ["📊 Matriz Dinâmica", "➕ Adicionar Tarefas", "📈 Histórico & Estatísticas"]
)

with tab1:
  st.subheader("O seu Fluxo de Tarefas Adaptativo")

  # --- DIAGNÓSTICO E RECOMENDAÇÃO DE IA ---
  st.markdown("### 🤖 Diagnóstico e Recomendação de IA")
  if energy_level <= 2:
    st.warning(
        "⚠️ **Alerta de Sobrecarga Preventiva:** A sua energia está baixa"
        f" ({energy_level}/5) e o seu estado é '{mood}'. A IA sugere pausar"
        " tarefas complexas e focar-se apenas em micro-hábitos de exigência"
        " **Baixa**."
    )
    recommended_energy = "Baixa"
  elif energy_level == 3:
    st.info(
        "⚖️ **Modo de Ritmo Constante:** Energia moderada. Ideal para tarefas"
        " de exigência **Média** ou para organizar pendentes sem pressas."
    )
    recommended_energy = "Média"
  else:
    st.success(
        "🚀 **Pico de Alta Performance:** Energia no topo! O momento ideal para"
        " avançar com projetos complexos ou de exigência **Alta**."
    )
    recommended_energy = "Alta"

  st.markdown("---")

  # --- FILTRO INTELIGENTE DE TAREFAS ---
  st.write("#### Filtrar Tarefas")
  filtro_modo = st.radio(
      "Mostrar:",
      ["Todas as tarefas", "✨ Apenas recomendadas para o meu estado atual"],
      horizontal=True,
  )

  tasks = get_tasks()

  if not tasks:
    st.info(
        "Ainda não tem tarefas criadas. Adicione tarefas no separador ao lado!"
    )
  else:
    if "Apenas recomendadas" in filtro_modo:
      tasks_filtradas = [
          t for t in tasks if t[2].lower() == recommended_energy.lower()
      ]
      st.caption(
          f"A mostrar apenas tarefas compatíveis com o nível recomendado:"
          f" **{recommended_energy}**"
      )
    else:
      tasks_filtradas = tasks

    if not tasks_filtradas:
      st.warning(
          "Não tem tarefas pendentes correspondentes a este nível de energia"
          " neste momento."
      )
    else:
      st.markdown("---")
      for task_id, title, req_energy, status in tasks_filtradas:
        col1, col2, col3 = st.columns([3, 2, 2])
        with col1:
          st.write(f"**{title}**")
        with col2:
          st.write(f"Exigência: {req_energy}")
        with col3:
          if status == "Pendente":
            if st.button("Concluir", key=f"done_{task_id}"):
              update_task_status(task_id, "Concluído")
              st.rerun()
          else:
            st.markdown("✅ Concluído")

with tab2:
  st.subheader("Criar Nova Tarefa ou Micro-Hábito")

  # --- GERADOR AUTOMÁTICO DE MICRO-HÁBITOS POR IA ---
  st.markdown("### 🪄 Gerador Inteligente por IA")
  st.write(
      "Deixe a IA criar automaticamente micro-hábitos ajustados ao seu estado"
      f" atual (Energia: {energy_level}/5 | Estado: {mood})."
  )

  if st.button("✨ Gerar Micro-Hábitos Automáticos"):
    # Lógica de sugestões dinâmicas com base no nível de energia atual
    if energy_level <= 2:
      sugestoes = [
          ("Fazer respiração profunda durante 3 minutos", "Baixa"),
          ("Organizar apenas a secretária ou ambiente de trabalho", "Baixa"),
          ("Beber um copo de água e fazer uma pausa visual", "Baixa"),
      ]
    elif energy_level == 3:
      sugestoes = [
          ("Rever pendentes e limpar caixa de e-mails", "Média"),
          ("Fazer uma caminhada ligeira de 15 minutos", "Média"),
          ("Planear as prioridades principais do dia seguinte", "Média"),
      ]
    else:
      sugestoes = [
          ("Esboçar o projeto estratégico principal", "Alta"),
          ("Avançar com a tarefa criativa mais difícil", "Alta"),
          ("Conduzir reunião de planeamento de alto impacto", "Alta"),
      ]

    for titulo_sug, energia_sug in sugestoes:
      add_task(titulo_sug, energia_sug)

    st.success(
        "✨ 3 Micro-hábitos gerados e adicionados com sucesso ao seu fluxo!"
    )
    st.rerun()

  st.markdown("---")

  with st.form("task_form"):
    new_task_title = st.text_input("Título da Tarefa Manual")
    new_task_energy = st.selectbox(
        "Nível de Energia Necessário", ["Baixa", "Média", "Alta"]
    )
    submit_task = st.form_submit_button("Adicionar Tarefa Manual")

    if submit_task and new_task_title:
      add_task(new_task_title, new_task_energy)
      st.success(f"Tarefa '{new_task_title}' adicionada com sucesso!")
      st.rerun()

with tab3:
  st.subheader("📈 Estatísticas e Histórico de Produtividade")

  conn = sqlite3.connect("micro_habit_mesh.db", check_same_thread=False)
  df_energy = pd.read_sql_query(
      "SELECT timestamp, energy_level, mood FROM energy_logs", conn
  )
  tasks_list = get_tasks()
  conn.close()

  # --- MÉTRICAS DE PRODUTIVIDADE (KPIs) ---
  total_tasks = len(tasks_list)
  completed_tasks = sum(1 for t in tasks_list if t[3] == "Concluído")
  pending_tasks = total_tasks - completed_tasks

  col_m1, col_m2, col_m3 = st.columns(3)
  col_m1.metric("Total de Tarefas", total_tasks)
  col_m2.metric("Tarefas Concluídas", completed_tasks)
  col_m3.metric("Tarefas Pendentes", pending_tasks)

  st.markdown("---")

  if df_energy.empty:
    st.info(
        "Ainda não existem registos de energia efetuados. Registe o seu"
        " estado na barra lateral para ver os gráficos!"
    )
  else:
    st.write("#### Evolução do Nível de Energia")
    st.line_chart(df_energy.set_index("timestamp")["energy_level"])

    st.write("#### Histórico de Registos")
    st.dataframe(df_energy, use_container_width=True)
