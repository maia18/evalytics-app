import flet as ft
from typing import Callable

# Importação dos subcomponentes que formam a seção Hero
from components.landing.hero.texto import criar_hero_texto
from components.landing.hero.painel import criar_painel_hero

def criar_hero(mudar_tela: Callable[[str], None], ir_para_recursos: Callable) -> ft.Container:
    """
    Cria a seção principal (Hero) da Landing Page.
        Organiza os textos à esquerda e o painel ilustrativo à direita de forma responsiva.
    """

    # 1. Instancia os dois grandes blocos da tela
    hero_texto = criar_hero_texto(
        mudar_tela,
        ir_para_recursos,
    )
    painel = criar_painel_hero()

    # 2. Retorna o Container principal com espaçamento generoso (respiro visual)
    return ft.Container(
        padding=ft.Padding.symmetric(
            horizontal=60, # Espaçamento lateral padrão da página
            vertical=90,   # Espaçamento superior e inferior para destacar o Hero
        ),
        
        # ResponsiveRow usa um sistema de 12 colunas (similar ao Bootstrap)
        content=ft.ResponsiveRow(
            columns=12,
            alignment=ft.MainAxisAlignment.CENTER,       # Centraliza horizontalmente
            vertical_alignment=ft.CrossAxisAlignment.CENTER, # Alinha os itens no meio da tela verticalmente
            controls=[
                
                # Bloco da Esquerda: Textos e Botões
                ft.Container(
                    # Configuração de responsividade:
                    # xs, sm, md (telas menores): Ocupa as 12 colunas (100% da largura)
                    # lg, xl (telas grandes): Ocupa 7 colunas (aprox. 58% da largura)
                    col={
                        "xs": 12,
                        "sm": 12,
                        "md": 12,
                        "lg": 7,
                        "xl": 7,
                    },
                    padding=ft.Padding.only(
                        right=30, # Evita que o texto cole no painel em telas grandes
                    ),
                    content=hero_texto,
                ),

                # Bloco da Direita: Painel (Dashboard mockado)
                ft.Container(
                    # Configuração de responsividade complementar:
                    # Em telas grandes ocupa as 5 colunas restantes (7 + 5 = 12)
                    col={
                        "xs": 12,
                        "sm": 12,
                        "md": 12,
                        "lg": 5,
                        "xl": 5,
                    },
                    alignment=ft.Alignment.CENTER,
                    padding=ft.Padding.only(
                        top=20, # Espaço extra no topo quando empilhado em telas menores
                    ),
                    content=painel,
                ),
            ],
        ),
    )