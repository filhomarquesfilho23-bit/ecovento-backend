# --- FORMULÁRIO PARA ADICIONAR NOVO TRABALHADOR ---
with st.expander("➕ Registar Novo Trabalhador / Cargo"):
    with st.form("form_novo_trabalhador", clear_on_submit=True):
        st.write("Insere os dados do novo elemento da equipa:")
        
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            novo_cargo = st.text_input("Cargo ou Função")
            nova_qtd = st.number_input("Quantidade", min_value=1, value=1, step=1)
            novo_custo_diario = st.number_input("Custo Diário (EUR)", min_value=0.0, value=75.0, step=5.0)
            
        with col_f2:
            novos_dias = st.number_input("Dias de Trabalho Mensal", min_value=1, value=22, step=1)
            
        # Botão de submissão do formulário
        submit_button = st.form_submit_button(label="Guardar na Base de Dados")
        
        if submit_button:
            if novo_cargo.strip() == "":
                st.warning("Por favor, escreve um cargo válido.")
            else:
                # Calcular custo mensal automaticamente
                custo_mensal = nova_qtd * novo_custo_diario * novos_dias
                
                # Inserir na base de dados SQLite
                conexao = sqlite3.connect('vanguarda_erp.db')
                cursor = conexao.cursor()
                cursor.execute(
                    "INSERT INTO mao_obra (cargo, quantidade, custo_diario, dias, custo_mensal) VALUES (?, ?, ?, ?, ?)",
                    (novo_cargo, nova_qtd, novo_custo_diario, novos_dias, custo_mensal)
                )
                conexao.commit()
                conexao.close()
                
                st.success(f"Trabalhador '{novo_cargo}' adicionado com sucesso!")
                # Atualizar a página para refletir os novos dados imediatamente
                st.rerun()
