import flet as ft
from typing import Callable
from components.layout.responsive.responsive import ResponsiveLayout
from components.core.constants.constants import (
    TEXTO_PRINCIPAL, 
    ALTURA_CARD_TABELA_DADOS,
)
from models.avaliacoes.layout.card_controle_ciclo import criar_card_controle_ciclo
from models.avaliacoes.layout.card_tabela_dados import criar_card_tabela_dados

def criar_conteudo_avaliacoes(layout, mudar_tela: Callable[[str], None], page: ft.Page) -> ft.Container:
    """Isola os componentes visuais da tela de avaliações para permitir reaproveitamento."""
    
    card_controle_ciclo = criar_card_controle_ciclo(layout, mudar_tela, page) # Instancia o card de métricas superiores (status do ciclo e ações)
    
    '''
    Instancia a tabela de dados brutos. 
        expand=False + altura fixa: impede que a tabela force um tamanho infinito no scroll
    '''
    card_tabela_dados = criar_card_tabela_dados(layout, page, expand=False, height=ALTURA_CARD_TABELA_DADOS)

    '''
    Mesmo padrão de correção do dashboard.py: expand=True no Container "de fora", scroll=AUTO isolado na Column "de dentro" (nunca os dois juntos na mesma Column)
    '''
    return ft.Container(
        expand=True,
        content=ft.Column(
            spacing=14,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Container(height=8), # Spacer do topo para desgrudar a interface da margem superior
                ft.Column(
                    spacing=4,
                    controls=[
                        # Cabeçalho da página
                        ft.Text("Gestão de Ciclos e Respostas", size=28, weight="bold", color=layout.cores[TEXTO_PRINCIPAL]),
                        ft.Text("Monitore campanhas ativas e extraia os dados brutos das avaliações.", size=16, color=ft.Colors.GREY),
                    ],
                ),
                # Injeta os cards gerados acima na estrutura da coluna
                card_controle_ciclo,
                card_tabela_dados,
            ],
        ),
    )
    
def ViewAvaliacoes(page: ft.Page, mudar_tela: Callable[[str], None]) -> ft.View:
    """Constrói a página principal de Avaliações."""
    
    # Configura a estrutura principal chamando o gerenciador de layout que construímos anteriormente
    layout = ResponsiveLayout(
        page,
        titulo_pagina="Avaliações",
        subtitulo="Acompanhe respostas e métricas em tempo real.",
        mudar_tela=mudar_tela,
    )
    conteudo = criar_conteudo_avaliacoes(layout, mudar_tela, page) # Prepara o "miolo" da tela

    layout.add_content(conteudo) # Injeta o conteúdo no layout
    return layout.criar_view("/avaliacoes") # Retorna a View montada para o roteador do Flet