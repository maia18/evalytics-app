from nicegui import ui
from services.avaliacoes_service import listar_avaliacoes


def ranking_dashboard():

    avaliacoes = listar_avaliacoes()

    ui.card().classes('w-full p-4')

    with ui.card().classes('w-full p-4'):

        ui.label('🏆 Ranking (base)').classes('text-xl font-bold')

        for av in avaliacoes[:5]:

            ui.label(f"Avaliação #{av['id']}")