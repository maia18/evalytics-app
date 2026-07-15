import flet as ft
from components.widgets.menu.menu import MENU_ITEMS_COLLAPSED
from components.widgets.menu.botao_icon import criar_botao_icon
from components.layout.sidebar.sidebar_logo import criar_logo

def criar_sidebar_colapsada(dark_mode, mudar_tela, cores):
    
    """Sidebar compacta (apenas ícones)"""
    
    controles = [
        criar_logo(cores, compact=True),
        ft.Divider(height=1),
    ]

    for icone, texto, rota in MENU_ITEMS_COLLAPSED:
        controles.append(
            criar_botao_icon(
                icone, texto, rota, dark_mode, cores["TEXTO_PRINCIPAL"], mudar_tela
            )
        )

    controles.append(ft.Divider(height=1))

    return ft.Column(
        controls=controles,
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
        alignment=ft.MainAxisAlignment.START,
    )
