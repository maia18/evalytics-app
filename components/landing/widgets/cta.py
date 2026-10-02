import flet as ft
from typing import Callable

from components.core.constants.constants import COR_PRIMARIA

def criar_cta(mudar_tela: Callable[[str], None]) -> ft.Container:
    """
    Cria a seção CTA (Call To Action) da Landing Page.
        Tem o objetivo de incentivar o usuário a acessar a plataforma através de uma chamada visual destacada e um botão de ação.
    """

    return ft.Container(
        # Espaçamento externo da seção em relação aos demais blocos da página.
        margin=ft.Margin.symmetric(
            horizontal=20,
            vertical=30,
        ),
        padding=35, # Espaçamento interno.
        bgcolor=COR_PRIMARIA, # Cor de fundo principal da marca.
        border_radius=16, # Bordas arredondadas para um visual moderno.
        
        # =====================================================
        # LAYOUT RESPONSIVO
        # =====================================================
        content=ft.ResponsiveRow(
            columns=12,
            alignment=ft.MainAxisAlignment.CENTER, # Centraliza horizontalmente os elementos.
            vertical_alignment=ft.CrossAxisAlignment.CENTER, # Centraliza verticalmente os elementos.
            run_spacing=20, # Espaçamento entre linhas quando houver quebra.
            controls=[
                
                # =================================================
                # BLOCO DE TEXTO
                # =================================================
                ft.Container(
                    
                    # Configuração de responsividade.
                    #   xs e sm:
                    #      ocupa toda a largura.
                    #   md+:
                    #       ocupa 8 das 12 colunas.
                    
                    col={
                        "xs": 12,
                        "sm": 12,
                        "md": 8,
                        "lg": 8,
                        "xl": 8,
                    },
                    content=ft.Column(
                        spacing=10,
                        controls=[
                            
                            # -------------------------------------
                            # Título principal da CTA
                            # -------------------------------------
                            ft.Text(
                                "Pronto para começar?",
                                size=25,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.WHITE,
                            ),
                            
                            # -------------------------------------
                            # Texto complementar
                            # -------------------------------------
                            ft.Text(
                                "Acesse o Evalytics e acompanhe "
                                "as avaliações da sua instituição.",
                                size=14,
                                color=ft.Colors.WHITE70,
                            ),
                        ],
                    ),
                ),
                
                # =================================================
                # BLOCO DO BOTÃO
                # =================================================
                
                # Responsividade:
                #    Mobile:
                #        ocupa linha inteira.
                #    Desktop:
                #        ocupa 4 colunas.
                
                ft.Container(
                    col={
                        "xs": 12,
                        "sm": 12,
                        "md": 4,
                        "lg": 4,
                        "xl": 4,
                    },
                    alignment=ft.Alignment.CENTER, # Centraliza o botão dentro da área disponível.
                    content=ft.ElevatedButton(
                        "Entrar na plataforma", # Texto exibido ao usuário.
                        bgcolor=ft.Colors.WHITE,
                        color=COR_PRIMARIA,
                        height=45,
                        on_click=lambda e: mudar_tela("/login"), # Redireciona para a tela de login.
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(
                                radius=8,
                            ),
                            padding=ft.Padding.symmetric(
                                horizontal=24,
                            ),
                        ),
                    ),
                ),
            ],
        ),
    )