import flet as ft
from typing import Callable

from components.core.constants.constants import (
    COR_TEXTO_TITULO,
    COR_TEXTO_SECUNDARIO,
    COR_PRIMARIA,
)

def criar_hero_texto(mudar_tela: Callable[[str], None], ir_para_recursos: Callable) -> ft.Column:
    """Cria a estrutura de texto e botões da seção Hero (Copywriting da página)."""

    return ft.Column(
        spacing=18,
        horizontal_alignment=ft.CrossAxisAlignment.START, # Garante que todo o texto alinhe à esquerda
        controls=[
            
            # 1. Label/Tag inicial (Prepara o contexto do usuário)
            ft.Text(
                "AVALIAÇÃO INSTITUCIONAL",
                size=13,
                weight=ft.FontWeight.BOLD,
                color=COR_PRIMARIA,
            ),

            # 2. Título Principal (O texto mais forte da página)
            ft.Text(
                "Transforme avaliações\nem melhorias.",
                size=42, # Tamanho grande para criar impacto no primeiro segundo
                weight=ft.FontWeight.BOLD,
                color=COR_TEXTO_TITULO,
            ),

            # 3. Descrição (Subtítulo explicativo)
            ft.Container(
                content=ft.Text(
                    "Uma plataforma para coletar, organizar e "
                    "analisar avaliações institucionais, "
                    "apoiando a tomada de decisões e a "
                    "melhoria contínua.",
                    size=17,
                    color=COR_TEXTO_SECUNDARIO,
                ),
            ),

            # Espaçador invisível para separar mais o texto dos botões
            ft.Container(height=5),

            # 4. Botões de Ação (CTAs) em uma ResponsiveRow
            ft.ResponsiveRow(
                columns=12,
                run_spacing=10, # Espaço vertical entre os botões quando eles quebram de linha no mobile
                controls=[
                    
                    # Botão Primário (Forte, sólido, foco principal)
                    ft.Container(
                        col={
                            "xs": 12, # No celular ocupa a linha toda (100% da largura)
                            "sm": 12,
                            "md": 6,  # No PC ocupa metade do espaço reservado
                            "lg": 6,
                            "xl": 6,
                        },
                        content=ft.ElevatedButton(
                            "Começar agora",
                            bgcolor=COR_PRIMARIA,
                            color=ft.Colors.WHITE,
                            height=48,
                            width=190,
                            on_click=lambda e: mudar_tela("/login"), # Redireciona para login
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=8),
                                padding=ft.Padding.symmetric(horizontal=25),
                            ),
                        ),
                    ),

                    # Botão Secundário (Fantasma / Outlined, ação secundária)
                    ft.Container(
                        col={
                            "xs": 12,
                            "sm": 12,
                            "md": 6,
                            "lg": 6,
                            "xl": 6,
                        },
                        content=ft.OutlinedButton(
                            "Conhecer a plataforma",
                            height=48,
                            width=210,
                            on_click=ir_para_recursos, # Rola a página para baixo
                            style=ft.ButtonStyle(
                                color=COR_PRIMARIA,
                                side=ft.BorderSide(
                                    1,
                                    COR_PRIMARIA, # Borda com a cor principal
                                ),
                                shape=ft.RoundedRectangleBorder(radius=8),
                                padding=ft.Padding.symmetric(horizontal=25),
                            ),
                        ),
                    ),
                ],
            ),
        ],
    )