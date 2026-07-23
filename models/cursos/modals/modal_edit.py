import flet as ft 
from database.services.firestore_courses import atualizar_curso_db 

def criar_modal_edit(page, estado, campos_edit, atualizar_interface): 
    """
    Constrói a janela de edição. Ela se aproveita do dicionário 'estado' para
    saber EXATAMENTE qual linha visual e qual ID do banco ela está manipulando.
    """
    
    def fechar_modal(e): 
        modal.open = False 
        page.update() 

    def salvar_edicao(e): 
        # Resgata a referência em memória da linha clicada
        linha_em_edicao = estado["linha_atual"] 
        id_banco = estado["id_firebase"] 
        
        # Pega os novos textos digitados
        nome = campos_edit["nome"].value 
        depto = campos_edit["departamento"].value 
        coord = campos_edit["coordenador"].value 

        if linha_em_edicao and id_banco: 
            # Chama a atualização do Firestore
            sucesso = atualizar_curso_db(id_banco, nome, depto, coord) 
            if sucesso: 
                # Se o DB confirmar, injeta os textos diretamente nas células visuais (Omitimos a Célula 0 que é o Código)
                linha_em_edicao.cells[1].content.value = nome 
                linha_em_edicao.cells[2].content.value = depto 
                linha_em_edicao.cells[3].content.value = coord 
                
        fechar_modal(e) 
        atualizar_interface() # Para atualizar os contadores de departamento, caso o usuário tenha mudado

    modal = ft.AlertDialog( 
        modal=True, 
        title=ft.Text("Editar Curso", size=20, weight="bold"), 
        content=ft.Column(width=400, height=220, spacing=15, controls=list(campos_edit.values())), 
        actions=[ 
            ft.TextButton("Cancelar", on_click=fechar_modal, style=ft.ButtonStyle(color="red700")), 
            ft.ElevatedButton("Atualizar", on_click=salvar_edicao, bgcolor="blue700", color="white"), 
        ], 
    ) 

    return modal 