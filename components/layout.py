from nicegui import app, ui
from components.auth import logout # Importe a função que criamos


def layout():
    # As cores entram aqui, dentro da função de layout!
    ui.colors(
        primary='#1E3A8A',    # Azul escuro
        secondary='#10B981',  # Verde esmeralda
        accent='#F59E0B',     # Laranja/Amarelo
        positive='#22C55E',   # Verde sucesso
        negative='#EF4444',   # Vermelho perigo
    )

    with ui.header().classes('justify-between items-center bg-primary text-white'):
        ui.label('Evalytics').classes('text-2xl font-bold')
        
        # Só mostra o botão de sair se o usuário estiver logado
        if app.storage.user.get('autenticado', False):
            ui.button('Sair', on_click=logout, icon='logout').props('flat color=white')

    with ui.left_drawer().classes('bg-gray-50'):
        with ui.column().classes('w-full gap-2 p-4'):
            
            # Links Públicos
            ui.label('Público').classes('text-xs text-gray-500 font-bold uppercase mt-4')
            ui.button('Nova Avaliação', on_click=lambda: ui.navigate.to('/nova_avaliacao'), icon='add').classes('w-full text-left').props('flat')
            
            # Só renderiza os links administrativos se estiver autenticado
            if app.storage.user.get('autenticado', False):
                ui.label('Administração').classes('text-xs text-gray-500 font-bold uppercase mt-4')
                ui.button('Dashboard', on_click=lambda: ui.navigate.to('/dashboard'), icon='dashboard').classes('w-full text-left').props('flat')
                ui.button('Relatórios', on_click=lambda: ui.navigate.to('/relatorios'), icon='bar_chart').classes('w-full text-left').props('flat')
                ui.button('Professores', on_click=lambda: ui.navigate.to('/professores'), icon='person').classes('w-full text-left').props('flat')
                ui.button('Disciplinas', on_click=lambda: ui.navigate.to('/disciplinas'), icon='school').classes('w-full text-left').props('flat')