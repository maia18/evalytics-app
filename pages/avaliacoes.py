from nicegui import ui
from components.layout import layout

from components.auth import require_login

from nicegui import ui

from components.layout import layout
from components.header import titulo_pagina
from components.grid import criar_grid

from services.avaliacoes_service import (
    listar_avaliacoes,
    detalhes_avaliacao,
    remover_avaliacao,
)

@ui.page('/avaliacoes')
def avaliacoes():
    
    if not require_login(): return

    layout()
    
    titulo_pagina(
        '📋 Histórico de Avaliações',
        'Todas as avaliações cadastradas e seus detalhes.'
    )

    colunas = [
        {
            "headerName": "ID",
            "field": "id",
            "width": 100,
        },
        {
            "headerName": "Professor",
            "field": "professor",
            "flex": 1,
        },
        {
            "headerName": "Disciplina",
            "field": "disciplina",
            "flex": 1,
        },
        {
            "headerName": "Status",
            "field": "status",
            "width": 140,
        },
        {
            "headerName": "Data",
            "field": "data_avaliacao",
            "width": 140,
        },
    ]

    grid = criar_grid(
        colunas,
        listar_avaliacoes(),
    )
    
    def atualizar_grid():
        grid.options['rowData'] = listar_avaliacoes()
        grid.update()
    
    async def excluir():
        selecionados = await grid.get_selected_rows()

        if not selecionados:
            ui.notify('Selecione uma avaliação na tabela.', type='warning')
            return

        sucesso = remover_avaliacao(selecionados[0]["id"])
        
        if sucesso:
            atualizar_grid()
            ui.notify('Avaliação removida com sucesso!', type='positive')
        else:
            ui.notify('Erro ao remover a avaliação.', type='negative')
    
    dialog = ui.dialog()

    # Ajustado para ter limite de altura e scroll (overflow-y-auto)
    with dialog:
        with ui.card().classes('w-[900px] max-w-full max-h-[80vh] overflow-y-auto p-6'):
            
            ui.label('Detalhes da Avaliação').classes('text-2xl font-bold text-gray-800 mb-4')
            detalhes = ui.column().classes('w-full gap-4')
            
    async def visualizar():
        selecionados = await grid.get_selected_rows()

        if not selecionados:
            ui.notify('Selecione uma avaliação.', type='warning')
            return

        avaliacao = selecionados[0]
        detalhes.clear()

        with detalhes:
            
            with ui.row().classes('w-full gap-8 mb-2'):
                ui.label(f"Professor: {avaliacao['professor']}").classes('text-lg font-bold text-primary')
                ui.label(f"Disciplina: {avaliacao['disciplina']}").classes('text-lg text-gray-700')

            ui.separator()

            respostas = detalhes_avaliacao(avaliacao["id"])
            
            if not respostas:
                ui.label("Nenhuma resposta vinculada a esta avaliação.").classes('italic text-gray-500')
            else:
                for resposta in respostas:
                    with ui.card().classes('w-full bg-gray-50 shadow-sm border border-gray-100 p-4'):
                        # Exibe o Eixo e o Título do Indicador
                        ui.label(f"Eixo {resposta['eixo']} | {resposta['indicador']}").classes('font-bold text-gray-800')
                        
                        with ui.row().classes('w-full justify-between mt-2'):
                            ui.label(f"Nota: {resposta['nota']}").classes('text-lg font-bold text-blue-600')
                            comentario_txt = resposta['comentario'] if resposta['comentario'] else "-"
                            ui.label(f"Comentário: {comentario_txt}").classes('text-gray-600 italic')

        dialog.open()
        
    with ui.row().classes('mt-4 gap-4'):
        ui.button(
            '👁️ Visualizar',
            on_click=visualizar
        ).props('color=primary')

        ui.button(
            '🗑️ Excluir',
            on_click=excluir
        ).props('color=negative')