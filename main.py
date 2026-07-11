import flet as ft

from configurations.global_configs import configurar_aplicacao
from components.router import obter_view


def main(page: ft.Page):

    configurar_aplicacao(page)

    def mudar_tela(rota: str):

        page.views.clear()

        view = obter_view(rota)

        page.views.append(view(page, mudar_tela))

        page.update()

    mudar_tela("/")

if __name__ == "__main__":
    ft.run(main, assets_dir="assets")