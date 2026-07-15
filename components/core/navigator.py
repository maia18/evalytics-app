""" Importações """  
import flet as ft

from components.core.router import obter_view # função que retorna a view correspondente a uma rota

class Navigator:
    
    """
    Classe responsável por gerenciar a navegação entre diferentes rotas/views dentro da aplicação Flet.
    """
    def __init__(self, page: ft.Page):
        
        self.page = page # Armazena a referência da página principal da aplicação

    def go(self, rota: str):
        
        """
        Método que realiza a navegação para uma rota específica.
        - Limpa as views atuais
        - Obtém a view correspondente à rota
        - Adiciona a nova view à página
        - Atualiza a interface
        """

        self.page.views.clear() # Remove todas as views existentes da página

        view = obter_view(rota) # Obtém a função que constrói a view para a rota informada

        """ 
        Adiciona a nova view à página, passando a referência da página e o método go (para permitir navegação interna)
        """
        self.page.views.append(view(self.page, self.go))

        self.page.update() # Atualiza a interface para refletir a nova view