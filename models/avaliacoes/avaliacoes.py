import flet as ft 
from components.layout.responsive.responsive import ResponsiveLayout 
from components.core.constants.constants import * 
from models.avaliacoes.layout.card_controle_ciclo import criar_card_controle_ciclo 
from models.avaliacoes.layout.card_tabela_dados import criar_card_tabela_dados 

def ViewAvaliacoes(page: ft.Page, mudar_tela): 
    """
    Constrói a página principal de Avaliações, montando o layout base e injetando os componentes visuais.
    """
    
    # Inicializa a estrutura base (Sidebar, Topbar) através da classe ResponsiveLayout
    layout = ResponsiveLayout( 
        page, 
        titulo_pagina="Avaliações", # Define o título exibido no topo
        subtitulo="Acompanhe respostas e métricas em tempo real.", 
        mudar_tela=mudar_tela # Repassa a função de navegação
    ) 

    # Instancia os cartões (widgets) que compõem a tela, passando o layout e a página como contexto
    card_controle_ciclo = criar_card_controle_ciclo(layout, mudar_tela, page) 
    card_tabela_dados = criar_card_tabela_dados(layout, page) 

    # Agrupa o título da seção e os cartões em uma coluna que expande para preencher o espaço
    conteudo = ft.Column( 
        expand=True, # Permite que a coluna ocupe a altura restante
        spacing=20, # Espaçamento entre os elementos principais da tela
        controls=[ 
            # Cabeçalho interno da página
            ft.Column( 
                spacing=5, 
                controls=[ 
                    ft.Text("Gestão de Ciclos e Respostas", size=28, weight="bold", color=layout.cores[TEXTO_PRINCIPAL]), 
                    ft.Text("Monitore campanhas ativas e extraia os dados brutos das avaliações.", size=16, color="grey"), 
                ] 
            ), 
            card_controle_ciclo, # Adiciona o cartão superior de status do ciclo
            card_tabela_dados # Adiciona o cartão inferior com a tabela de resultados
        ] 
    ) 

    # Insere o conteúdo montado na área principal do layout
    layout.add_content(conteudo) 
    
    # Retorna a View finalizada e pronta para ser exibida pelo Flet na rota "/avaliacoes"
    return layout.criar_view("/avaliacoes") 