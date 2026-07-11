import flet as ft

from configurations.global_configs import configurar_aplicacao
from components.navigator import Navigator

def main(page: ft.Page):

    configurar_aplicacao(page)
    Navigator(page).go("/")

if __name__ == "__main__":
    ft.run(main, assets_dir="assets")