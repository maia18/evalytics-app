import flet as ft 
from components.layout.responsive.responsive import ResponsiveLayout 
from components.core.constants.constants import * 
from models.avaliacoes.layout.card_controle_ciclo import criar_card_controle_ciclo 
from models.avaliacoes.layout.card_tabela_dados import criar_card_tabela_dados 

def criar_conteudo_avaliacoes(layout, mudar_tela, page):
    """
    Isola os componentes visuais da tela de avaliações para permitir reaproveitamento.
    """
    card_controle_ciclo = criar_card_controle_ciclo(layout, mudar_tela, page)
    card_tabela_dados = criar_card_tabela_dados(layout, page)   

    # ESSENCIAL: Impede que a tabela force um tamanho infinito no scroll
    card_tabela_dados.expand = False
    card_tabela_dados.height = 420

    return ft.Column( 
        expand=True, # Ancora a coluna no TabBarView
        spacing=20,
        scroll=ft.ScrollMode.AUTO,
        controls=[ 
            ft.Container(height=20),
            ft.Column( 
                spacing=5,
                controls=[ 
                    ft.Text("Gestão de Ciclos e Respostas", size=28, weight="bold", color=layout.cores[TEXTO_PRINCIPAL]),
                    ft.Text("Monitore campanhas ativas e extraia os dados brutos das avaliações.", size=16, color="grey"),
                ] 
            ), 
            card_controle_ciclo,
            card_tabela_dados
        ] 
    )

def ViewAvaliacoes(page: ft.Page, mudar_tela): 
    """
    Constrói a página principal de Avaliações.
    """
    layout = ResponsiveLayout( 
        page, 
        titulo_pagina="Avaliações",
        subtitulo="Acompanhe respostas e métricas em tempo real.",
        mudar_tela=mudar_tela
    ) 

    # Chama a interface isolada
    conteudo = criar_conteudo_avaliacoes(layout, mudar_tela, page)
    
    layout.add_content(conteudo)
    return layout.criar_view("/avaliacoes")