from nicegui import ui
from components.layout import layout

@ui.page('/configuracoes')
def configuracoes():

    layout()

    ui.label('⚙️ Configurações').classes('text-2xl font-bold')

    ui.label('Sistema de avaliação MEC')