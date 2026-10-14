# --- IA SEMÂNTICA DE VOZ AVANÇADA (ATUALIZADA) ---
if "intencao_atual" not in st.session_state:
    st.session_state.intencao_atual = "dashboard"

if intencao_voz:
    t = intencao_voz.lower()
    if any(k in t for k in ["equip", "colaborador", "salario", "membro"]):
        st.session_state.intencao_atual = "equipa"
    elif any(k in t for k in ["finan", "dinheiro", "orçamento", "gasto", "fatura"]):
        st.session_state.intencao_atual = "financeiro"
    elif any(k in t for k in ["tarefa", "nota", "fazer", "trabalho", "projeto"]):
        st.session_state.intencao_atual = "tarefas_notas"
    elif any(k in t for k in ["relatório", "exportar", "nuvem", "cloud"]):
        st.session_state.intencao_atual = "relatorios"
    else:
        st.session_state.intencao_atual = "dashboard"
    st.info(f"🎙️ **Comando de Voz Detetado:** \"{intencao_voz}\" ➔ Módulo Ativado!")
