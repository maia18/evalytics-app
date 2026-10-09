import flet as ft
from typing import Callable
from components.core.constants.constants import (
    COR_PRIMARIA,
)

def criar_cta(mudar_tela: Callable[[str], None]) -> ft.Container:
    """
    Cria o banner final de conversão (Call to Action) da Landing Page.
        Ele utiliza uma cor forte de fundo para se destacar e guiar o usuário  para o objetivo principal (fazer login).
    """

    return ft.Container(
        
        # Margin empurra os elementos *externos* (afasta do conteúdo vizinho).
        margin=ft.Margin.symmetric(
            horizontal=40,
            vertical=45,
        ),
        # Padding afasta o conteúdo *interno* das bordas do card.
        padding=ft.Padding.symmetric(
            horizontal=45,
            vertical=38,
        ),
        bgcolor=COR_PRIMARIA, # Cor de destaque sólida do banner
        border_radius=18,     # Borda bem arredondada, estilo moderno
        
        content=ft.ResponsiveRow(
            columns=12,
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            run_spacing=24, # Espaçamento se o botão quebrar pra linha de baixo no celular
            controls=[
                
                # =====================================================
                # BLOCO ESQUERDO: MENSAGEM (Ocupa 2/3 do espaço no PC)
                # =====================================================
                ft.Container(
                    col={"xs": 12, "sm": 12, "md": 8, "lg": 8, "xl": 8},
                    content=ft.Column(
                        spacing=8,
                        controls=[
                            ft.Text(
                                "Pronto para começar?",
                                size=26,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.WHITE, # Letra branca para contrastar com o fundo colorido
                            ),
                            ft.Text(
                                "Acesse o Evalytics e acompanhe as avaliações da sua instituição.",
                                size=14,
                                color=ft.Colors.WHITE70, # Leve transparência para hierarquia (subtítulo)
                            ),
                        ],
                    ),
                ),

                # =====================================================
                # BLOCO DIREITO: BOTÃO DE AÇÃO (Ocupa 1/3 do espaço no PC)
                # =====================================================
                ft.Container(
                    col={"xs": 12, "sm": 12, "md": 4, "lg": 4, "xl": 4},
                    alignment=ft.Alignment.CENTER_RIGHT, # Empurra o botão para a extrema direita no PC
                    
                    content=ft.ElevatedButton(
                        "Entrar na plataforma",
                        height=46,
                        
                        # Inversão de cores: Botão branco com texto na cor primária
                        bgcolor=ft.Colors.WHITE,
                        color=COR_PRIMARIA,
                        
                        on_click=lambda e: mudar_tela("/login"),
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=8),
                            padding=ft.Padding.symmetric(horizontal=24),
                        ),
                    ),
                ),
            ],
        ),
    )