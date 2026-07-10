import os
import flet as ft

from views.login import ViewLogin
from views.dashboard import ViewDashboard
from views.avaliacoes import ViewAvaliacoes

def main(page: ft.Page):
    
    # Configurações Globais
    page.window.icon = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "logo.ico")
    page.title = "Evalytics - Avaliação Institucional"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.width = 1280
    page.window.height = 720
    page.padding = 0
    page.bgcolor = ft.Colors.BLUE_GREY_50 

    # Gerenciador de Rotas Enxuto
    def mudar_tela(rota):
        page.views.clear()

        if rota == "/":
            page.views.append(ViewLogin(page, mudar_tela))
        elif rota == "/dashboard":
            page.views.append(ViewDashboard(page, mudar_tela))
        elif rota == "/avaliacoes":
            page.views.append(ViewAvaliacoes(page, mudar_tela))

        page.update()

    # Inicia o app
    mudar_tela("/")

if __name__ == "__main__":
    ft.run(main, assets_dir="assets")