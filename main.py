import flet as ft
from configurations.global_configs import configurar_aplicacao
from components.core.navigator import Navigator

def main(page: ft.Page):
    
    configurar_aplicacao(page) # Aplica configurações globais na página
    Navigator(page).go("/") # Inicializa o navegador e direciona para a página de login

if __name__ == "__main__":
    ft.run(main, assets_dir="assets") # O parâmetro assets_dir define a pasta onde ficam os arquivos estáticos (imagens, ícones, etc.)