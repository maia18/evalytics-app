import flet as ft
from typing import Callable
from components.core.constants.constants import (
    TEXTO_PRINCIPAL,
)
from models.avaliacoes.layout.cards.card_controle_ciclo import criar_card_controle_ciclo
from models.avaliacoes.layout.cards.card_tabela_dados import criar_card_tabela_dados

def criar_conteudo_avaliacoes(layout, mudar_tela: Callable[[str], None], page: ft.Page) -> ft.Container:
    """Isola os componentes visuais da tela de avaliações para permitir reaproveitamento em outras rotas"""

    '''
    Instancia o card superior que exibe o status atual do ciclo e ações de controle
    '''
    card_controle_ciclo = criar_card_controle_ciclo(
        layout, 
        mudar_tela, 
        page,
    ) 
        
    '''
    Instancia a tabela de dados brutos.
    '''
    card_tabela_dados = criar_card_tabela_dados(
        layout, 
        page, 
        expand=True, 
        height=None,
    )
    
    return ft.Container(
        expand=True,
        content=ft.Column(
            expand=True,
            spacing=14,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Column(
                    spacing=4,
                    controls=[
                        # Cabeçalho interno da página
                        ft.Text(
                            "Gestão de Ciclos e Respostas", 
                            size=28, 
                            weight="bold", 
                            color=layout.cores[TEXTO_PRINCIPAL]
                        ),
                        ft.Text(
                            "Monitore campanhas ativas e extraia os dados brutos das avaliações.", 
                            size=16, 
                            color=ft.Colors.GREY
                        ),
                    ],
                ),
                
                # Injeta os cards gerados dinamicamente na estrutura da coluna
                card_controle_ciclo,
                ft.Container(
                    expand=True,
                    content=card_tabela_dados,
                ),
            ],
        ),
    )