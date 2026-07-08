from nicegui import ui
from components.layout import layout

from components.auth import require_login

from nicegui import ui

from components.layout import layout
from components.header import titulo_pagina
from components.grid import criar_grid
from components.forms import campo, botao

from services.disciplinas_service import (
    listar_disciplinas,
    adicionar_disciplina,
    atualizar_disciplina,
    remover_disciplina,
)

@ui.page('/disciplinas')
def disciplinas():
    
    if not require_login(): return

    layout()

    disciplina_selecionada = None

    titulo_pagina(
        '📚 Disciplinas',
        'Gerencie as disciplinas cadastradas.'
    )

    colunas = [
        {'headerName': 'Código', 'field': 'codigo'},
        {'headerName': 'Nome', 'field': 'nome'},
        {'headerName': 'Curso', 'field': 'curso'},
        {'headerName': 'Semestre', 'field': 'semestre'},
    ]
    
    async def selecionar_linha():
        nonlocal disciplina_selecionada
        selecionados = await grid.get_selected_rows()

        if not selecionados:
            return

        disciplina = selecionados[0]
        disciplina_selecionada = disciplina['id']

        input_codigo.value = disciplina['codigo'] or ''
        input_nome.value = disciplina['nome'] or ''
        input_curso.value = disciplina['curso'] or ''
        input_semestre.value = str(disciplina['semestre']) if disciplina['semestre'] else ''

    grid = criar_grid(
        colunas,
        listar_disciplinas(),
        selecionar_linha # Ação direta ao clicar na linha
    )

    def atualizar_grid():
        grid.options['rowData'] = listar_disciplinas()
        grid.update()

    ui.separator()

    ui.label('Editar Disciplina').classes('text-xl font-bold mt-4')

    with ui.column().classes('w-full gap-2'):
        # Substituí o campo 'numero' por 'campo' normal
        input_codigo = campo('Código (ex: ELETRO-01)')
        input_nome = campo('Nome (ex: Eletromagnetismo Aplicado)')
        input_curso = campo('Curso (ex: Eng. de Telecomunicações)')
        input_semestre = campo('Semestre (ex: 2026.1)')

    def novo():
        nonlocal disciplina_selecionada
        disciplina_selecionada = None

        input_codigo.value = ''
        input_nome.value = ''
        input_curso.value = ''
        input_semestre.value = ''

        ui.notify('Pronto para cadastrar uma nova disciplina.')

    def salvar():
        nonlocal disciplina_selecionada

        if not input_codigo.value or not input_nome.value:
            ui.notify('Informe o código e o nome da disciplina.', type='warning')
            return
            
        if disciplina_selecionada is None:
            adicionar_disciplina(
                input_codigo.value,
                input_nome.value,
                input_curso.value,
                input_semestre.value,
            )
            ui.notify('Disciplina cadastrada!', type='positive')
        else:
            atualizar_disciplina(
                disciplina_selecionada,
                input_codigo.value,
                input_nome.value,
                input_curso.value,
                input_semestre.value,
            )
            ui.notify('Disciplina atualizada!', type='positive')

        atualizar_grid()
        novo()

    def excluir():
        nonlocal disciplina_selecionada

        if disciplina_selecionada is None:
            ui.notify('Selecione uma disciplina na tabela.', type='warning')
            return

        remover_disciplina(disciplina_selecionada)
        ui.notify('Disciplina removida.', type='warning')
        atualizar_grid()
        novo()

    with ui.row().classes('mt-4 gap-2'):
        botao('Novo', novo)
        botao('Salvar', salvar, 'positive')
        botao('Excluir', excluir, 'negative')