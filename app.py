import sqlite3
from datetime import datetime
import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Micro-Habit Mesh", page_icon="⚡", layout="wide"
)


# Inicializar Base de Dados SQLite
def init_db():
  conn = sqlite3.connect("micro_habit_mesh.db")
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
  conn = sqlite3.connect("micro_habit_mesh.db")
  c = conn.cursor()
  c.execute(
      "INSERT INTO energy_logs (timestamp, energy_level, mood) VALUES (?, ?,"
      " ?)",
      (datetime.now().strftime("%Y-%m-%d %H:%M"), level, mood),
  )
  conn.commit()
  conn.close()


def add_task(title, energy_required):
  conn = sqlite3.connect("micro_habit_mesh.db")
  c = conn.cursor()
  c.execute(
      "INSERT INTO tasks (title, energy_required, status) VALUES (?, ?, ?)",
      (title, energy_required, "Pendente"),
  )
  conn.commit()
  conn.close()


def get_tasks():
  conn = sqlite3.connect("micro_habit_mesh.db")
  c = conn.cursor()
  c.execute("SELECT id, title, energy_required, status FROM tasks")
  rows = c.fetchall()
  conn.close()
  return rows


def update_task_status(task_id, status):
  conn = sqlite3.connect("micro_habit_mesh.db")
  c = conn.cursor()
  c.execute("UPDATE tasks SET status = ? WHERE id = ?", (status, task_id))
  conn.commit()
  conn.close()


# Interface Gráfica (Streamlit)
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

# Layout Principal em Separadores
tab1, tab2, tab3 = st.tabs(
    ["📊 Matriz Dinâmica", "➕ Adicionar Tarefas", "📈 Histórico de Energia"]
)

with tab1:
  st.subheader("O seu Fluxo de Tarefas Adaptativo")
  tasks = get_tasks()

  if not tasks:
    st.info(
        "Ainda não tem tarefas criadas. Adicione tarefas no separador ao lado!"
    )
  else:
    # Lógica inteligente de recomendação baseada na energia atual
    st.write(
        f"**Estado atual detetado:** Nível de Energia {energy_level}/5 ({mood})"
    )

    if energy_level <= 2:
      st.warning(
          "⚠️ Detetámos baixa energia. O sistema recomenda focar-se apenas em"
          " micro-tarefas de baixa exigência hoje."
      )
    elif energy_level >= 4:
      st.success(
          "🚀 Energia alta detetada! Excelente momento para avançar com tarefas"
          " complexas e criativas."
      )

    st.markdown("---")
    for task_id, title, req_energy, status in tasks:
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
  with st.form("task_form"):
    new_task_title = st.text_input("Título da Tarefa")
    new_task_energy = st.selectbox(
        "Nível de Energia Necessário", ["Baixa", "Média", "Alta"]
    )
    submit_task = st.form_submit_button("Adicionar Tarefa")

    if submit_task and new_task_title:
      add_task(new_task_title, new_task_energy)
      st.success(f"Tarefa '{new_task_title}' adicionada com sucesso!")
      st.rerun()

with tab3:
  st.subheader("Registo de Padrões e Histórico")
  conn = sqlite3.connect("micro_habit_mesh.db")
  import pandas as pd

  df_energy = pd.read_sql_query(
      "SELECT timestamp, energy_level, mood FROM energy_logs", conn
  )
  conn.close()

  if df_energy.empty:
    st.info("Ainda não existem registos de energia efetuados.")
  else:
    st.dataframe(df_energy, use_container_width=True)
    st.line_chart(df_energy.set_index("timestamp")["energy_level"])
