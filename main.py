import flet as ft
from views.login import ViewLogin
from views.dashboard import ViewDashboard

def main(page: ft.Page):
    # Configurações Globais
    page.title = "Evalytics - Avaliação Institucional"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.window.width = 1200
    page.window.height = 800
    page.bgcolor = ft.Colors.BLUE_GREY_50 

    # Gerenciador de Rotas Enxuto
    def mudar_tela(rota):
        page.views.clear()

        if rota == "/dashboard":
            page.views.append(ViewDashboard(page, mudar_tela))
        else:
            page.views.append(ViewLogin(page, mudar_tela))
        
        page.update()

    # Inicia o app
    mudar_tela("/")

if __name__ == "__main__":
    ft.run(main, assets_dir="assets")