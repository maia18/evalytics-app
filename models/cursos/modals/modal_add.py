import flet as ft 
from database.services.firestore_courses import adicionar_curso_db 

def criar_modal_add(page, tabela_cursos, criar_linha_curso, atualizar_interface, campos_add): 
    """Constrói a janela sobreposta para cadastro e lida com a inserção no banco."""
    
    def fechar_modal(e): 
        modal.open = False 
        page.update() 

    def salvar_curso(e): 
        """Coleta o texto dos inputs, joga pro backend e reflete na tabela."""
        nome = campos_add["nome"].value 
        depto = campos_add["departamento"].value 
        coord = campos_add["coordenador"].value 
        codigo_novo = "NOVO" # Placeholder visual de código

        if nome: # Validação básica (nome obrigatório)
            # Dispara a gravação no Firebase
            novo_id = adicionar_curso_db(codigo_novo, nome, depto, coord) 
            
            if novo_id: # Se o banco retornar o ID confirmando sucesso
                # Cria e anexa instantaneamente a linha na UI sem precisar recarregar todo o banco
                nova_linha = criar_linha_curso(page, tabela_cursos, atualizar_interface, None, campos_add, {}, novo_id, codigo_novo, nome, depto, coord) 
                tabela_cursos.rows.append(nova_linha) 
                
                # Esvazia o formulário para o próximo uso
                for campo in campos_add.values(): 
                    campo.value = "" 
                    
                fechar_modal(e) 
                atualizar_interface() # Atualiza os contadores

    modal = ft.AlertDialog( 
        modal=True, # Trava o clique fora do fundo
        title=ft.Text("Cadastrar Novo Curso", size=20, weight="bold"), 
        # Injeta dinamicamente os inputs criados na ViewCursos extraindo-os do dicionário
        content=ft.Column(width=400, height=220, spacing=15, controls=list(campos_add.values())), 
        actions=[ 
            ft.TextButton("Cancelar", on_click=fechar_modal, style=ft.ButtonStyle(color="red700")), 
            ft.ElevatedButton("Salvar", on_click=salvar_curso, bgcolor="blue700", color="white"), 
        ], 
    ) 

    def abrir_modal_add(e): 
        if modal not in page.overlay: 
            page.overlay.append(modal) 
        modal.open = True 
        page.update() 

    return abrir_modal_add 