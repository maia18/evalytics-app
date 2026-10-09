import flet as ft
from typing import Callable
from components.landing.hero.texto import criar_hero_texto
from components.landing.hero.painel import criar_painel_hero

def criar_hero(
    mudar_tela: Callable[[str], None],
    ir_para_recursos: Callable,
) -> ft.Container:
    """
    Cria a seção principal (Hero) da Landing Page.
        Organiza os textos à esquerda e o painel ilustrativo à direita de forma responsiva.
    """

    hero_texto = criar_hero_texto(
        mudar_tela,
        ir_para_recursos,
    )
    painel = criar_painel_hero()

    return ft.Container(
        padding=ft.Padding.symmetric(
            horizontal=60,
            vertical=56,
        ),
        content=ft.ResponsiveRow(
            columns=12,
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                
                # =========================================================
                # TEXTO
                # =========================================================

                ft.Container(
                    col={
                        "xs": 12,
                        "sm": 12,
                        "md": 12,
                        "lg": 7,
                        "xl": 7,
                    },
                    padding=ft.Padding.only(
                        right=40,
                    ),
                    content=hero_texto,
                ),

                # =========================================================
                # PAINEL
                # =========================================================

                ft.Container(
                    col={
                        "xs": 12,
                        "sm": 12,
                        "md": 12,
                        "lg": 5,
                        "xl": 5,
                    },
                    alignment=ft.Alignment.CENTER,
                    padding=ft.Padding.only(
                        top=12,
                    ),
                    content=painel,
                ),
            ],
        ),
    )