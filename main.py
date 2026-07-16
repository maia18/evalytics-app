import flet as ft

from configurations.global_configs import configurar_aplicacao # função de configuração global da aplicação

from components.core.navigator import Navigator # componente responsável pela navegação entre páginas/rotas

def main(page: ft.Page):
    
    configurar_aplicacao(page) # Aplica configurações globais na página (tema, idioma, etc.)
    Navigator(page).go("/") # Inicializa o navegador e direciona para a rota inicial "/"

if __name__ == "__main__":
    
    """ 
    O parâmetro assets_dir define a pasta onde ficam os arquivos estáticos (imagens, ícones, etc.)
    """
    
    ft.run(main, assets_dir="assets")