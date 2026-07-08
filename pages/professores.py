from nicegui import ui
from components.layout import layout

from components.auth import require_login

from nicegui import ui
from components.layout import layout
from components.grid import criar_grid
from components.forms import campo

from services.professores_service import (
    listar_professores,
    adicionar_professor,
    atualizar_professor,
    remover_professor,
)

@ui.page('/professores')
def professores():
    
    if not require_login(): return

    layout()
        
    professor_selecionado = None

    ui.label('👨‍🏫 Professores').classes('text-3xl font-bold mb-4')

    colunas = [
        {'headerName': 'Nome', 'field': 'nome'},
        {'headerName': 'Departamento', 'field': 'departamento'},
        {'headerName': 'Email', 'field': 'email'},
    ]
    
    async def selecionar_linha():
        nonlocal professor_selecionado
        selecionados = await grid.get_selected_rows()

        if not selecionados:
            return

        professor = selecionados[0]
        professor_selecionado = professor["id"]

        input_nome.value = professor["nome"] or ""
        input_email.value = professor["email"] or ""
        input_departamento.value = professor["departamento"] or ""

    grid = criar_grid(
        colunas,
        listar_professores(),
        selecionar_linha # Ação direta ao clicar na linha
    )
    
    ui.separator().classes('my-4')
    
    def atualizar_grid():
        grid.options['rowData'] = listar_professores()
        grid.update()

    ui.label('Editar Professor').classes('text-xl font-bold mt-4 mb-2')

    with ui.column().classes('w-full gap-2'):
        input_nome = campo('Nome (ex: João Batista)')
        input_email = campo('Email')
        input_departamento = campo('Departamento (ex: Engenharia)')
        
    def novo():
        nonlocal professor_selecionado
        professor_selecionado = None

        input_nome.value = ''
        input_email.value = ''
        input_departamento.value = ''

        ui.notify('Pronto para cadastrar um novo professor.')
        
    def salvar():
        nonlocal professor_selecionado

        if not input_nome.value:
            ui.notify('Informe o nome do professor.', type='warning')
            return

        if professor_selecionado is None:
            adicionar_professor(
                input_nome.value,
                input_departamento.value,
                input_email.value,
            )
            ui.notify('Professor cadastrado!', type='positive')
        else:
            atualizar_professor(
                professor_selecionado,
                input_nome.value,
                input_departamento.value,
                input_email.value,
            )
            ui.notify('Professor atualizado!', type='positive')

        novo()
        atualizar_grid()
        
    def excluir():
        nonlocal professor_selecionado

        if professor_selecionado is None:
            ui.notify('Selecione um professor na tabela.', type='warning')
            return

        remover_professor(professor_selecionado)
        ui.notify('Professor removido.', type='warning')
        
        novo()
        atualizar_grid()
    
    with ui.row().classes('mt-4 gap-2'):
        ui.button('Novo', on_click=novo)
        ui.button('Salvar', on_click=salvar).props('color=positive')
        ui.button('Excluir', on_click=excluir).props('color=negative')