import flet as ft
'''
Importa 'Callable' do módulo de tipagem (typing). 
Isso é usado para avisar ao Python (e ao seu editor de código) que uma variável vai receber uma função.
'''
import logging as lg # módulo nativo de logs para rastreamento do sistema.
from typing import Callable
from components.core.auth import auth_state
from components.core.router import ViewBuilder, obter_view # Importações customizadas do sistema de roteamento do seu projeto

# Cria um logger específico para este módulo.
logger = lg.getLogger(__name__)

'''
Criação de um "Type Alias" (Apelido de Tipo).
    Isso diz que 'NavigateCallback' representa qualquer função que receba uma string (str) e não retorne nada (None).
    Isso deixa o código mais legível e ajuda na hora de tipar as telas que vão receber a função de navegação.
'''
NavigateCallback = Callable[[str], None]

class Navigator:
    """
    Gerencia a navegação entre diferentes rotas/views da aplicação Flet.
    Centralizar a navegação em uma classe evita que você precise reescrever a lógica de troca de telas em cada botão do seu aplicativo.
    """
    def __init__(self, page: ft.Page) -> None:
        '''
        Salva a referência da página principal (a janela do app) dentro da classe.
        Assim, os métodos da classe podem manipular a interface.
        '''
        self.page = page

    # Navega para a rota informada, substituindo a view (tela) atual
    def go(self, rota: str) -> None:

        rotas_publicas = {
            "/",
            "/login",
        }

        if rota not in rotas_publicas and not auth_state.autenticado:
            logger.warning(
                "Acesso bloqueado à rota '%s'. Usuário não autenticado.",
                rota,
            )
            rota = "/login"

        self.page.views.clear()
        self.page.overlay.clear()

        view_builder: ViewBuilder = obter_view(rota)

        self.page.views.append(
            view_builder(self.page, self.go)
        )

        self.page.update()