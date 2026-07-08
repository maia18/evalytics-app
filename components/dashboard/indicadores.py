from nicegui import ui
from services.avaliacoes_service import listar_avaliacoes


def indicadores_dashboard():

    avaliacoes = listar_avaliacoes()

    total = len(avaliacoes)

    ui.card().classes('w-full p-4') \
        .content = ui.column()

    with ui.card().classes('w-full p-4'):

        ui.label('📊 Indicadores gerais').classes('text-xl font-bold')

        ui.label(f'Total de avaliações: {total}')