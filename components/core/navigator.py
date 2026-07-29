import flet as ft
'''
Importa 'Callable' do módulo de tipagem (typing). 
Isso é usado para avisar ao Python (e ao seu editor de código) que uma variável vai receber uma função.
'''
from typing import Callable
import logging as lg # módulo nativo de logs para rastreamento do sistema.
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
        
        self.page.views.clear() # Limpa o histórico de telas (views) atual da página para garantir que a nova tela vai substituir a anterior por completo, em vez de empilhar uma tela sobre a outra (o que consumiria mais memória).

        view_builder: ViewBuilder = obter_view(rota) # Chama a função 'obter_view' passando a string da rota (ex: "/login" ou "/dashboard"). Ela retorna a função construtora (ViewBuilder) responsável por desenhar aquela tela específica.

        '''
            1. view_builder(self.page, self.go) executa a função construtora da tela.
            2. Ela passa o objeto 'page' e o PRÓPRIO método 'go' para a tela. (Injeção de dependência).
            3. O Flet exige que as telas fiquem dentro de uma lista chamada 'views', por isso o .append().
        '''
        self.page.views.append(view_builder(self.page, self.go))

        '''
        Avisa ao Flet que a estrutura da interface mudou e ele precisa renderizar a nova tela.
        Sem o .update(), a tela ficaria travada visualmente na view antiga.
        '''
        self.page.update()