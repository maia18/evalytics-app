import flet as ft
from typing import Callable
from components.layout.responsive.responsive import ResponsiveLayout
from models.avaliacoes.layout.conteudo_avaliacoes import criar_conteudo_avaliacoes

def ViewAvaliacoes(page: ft.Page, mudar_tela: Callable[[str], None]) -> ft.View:
    """Constrói a página principal de Avaliações"""
    
    # Configura a estrutura principal (Sidebar, Topbar) chamando o gerenciador de layout base
    layout = ResponsiveLayout(
        page,
        titulo_pagina="Avaliações",
        subtitulo="Acompanhe respostas e métricas em tempo real.",
        mudar_tela=mudar_tela,
    )
    
    # Prepara o "miolo" da tela delegando a construção para a função extraída e injeta o conteúdo no layout global da aplicação
    conteudo = criar_conteudo_avaliacoes(layout, mudar_tela, page) 
    layout.add_content(conteudo) 
    
    # Retorna a View finalizada e montada para o roteador do Flet
    return layout.criar_view("/avaliacoes") 