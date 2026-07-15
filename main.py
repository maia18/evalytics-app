""" Importações """  
import flet as ft # biblioteca Flet, usada para criar interfaces gráficas em Python

from configurations.global_configs import configurar_aplicacao # função de configuração global da aplicação

from components.core.navigator import Navigator # componente responsável pela navegação entre páginas/rotas

# Função principal da aplicação
def main(page: ft.Page):
    
    configurar_aplicacao(page) # Aplica configurações globais na página (tema, idioma, etc.)

    Navigator(page).go("/") # Inicializa o navegador e direciona para a rota inicial "/"

# Ponto de entrada da aplicação
if __name__ == "__main__":
    """ 
    Executa a aplicação Flet chamando a função main
    
    O parâmetro assets_dir define a pasta onde ficam os arquivos estáticos (imagens, ícones, etc.)
    """
    ft.run(main, assets_dir="assets")