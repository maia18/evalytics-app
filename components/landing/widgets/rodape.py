import flet as ft

from components.core.constants.constants import (
    COR_TEXTO_TITULO,
    COR_TEXTO_SECUNDARIO,
)

def criar_rodape() -> ft.Container:
    """
    Cria o rodapé (footer) da Landing Page.
        Organiza a marca, o slogan e os direitos autorais em uma linha responsiva que se divide em 3 colunas no desktop ou se empilha no celular.
    """

    return ft.Container(
        # Espaçamento interno: respiro de 25px no topo e na base do rodapé
        padding=ft.Padding.symmetric(
            horizontal=20,
            vertical=25,
        ),
        
        # Cria uma linha muito sutil apenas na parte de cima (separador visual do resto da página)
        border=ft.Border(
            top=ft.BorderSide(
                1,                  # Espessura de 1 pixel
                ft.Colors.BLACK12,  # Cinza bem claro (preto com 12% de opacidade)
            ),
        ),
        
        # Utiliza ResponsiveRow para distribuir o espaço de forma inteligente
        content=ft.ResponsiveRow(
            columns=12,
            alignment=ft.MainAxisAlignment.CENTER,       # Alinha o conteúdo horizontalmente
            vertical_alignment=ft.CrossAxisAlignment.CENTER, # Alinha os textos pelo meio na vertical
            
            run_spacing=8, # Espaço vertical de 8px caso os itens precisem quebrar de linha (ex: no celular)
            
            controls=[
                
                # 1. BLOCO DA ESQUERDA: Logotipo / Nome do Sistema
                ft.Container(
                    # Configuração de grade (12 colunas totais):
                    # No mobile (xs, sm) ocupa tudo (12), forçando os outros itens para baixo.
                    # No PC/Tablet (md, lg, xl) ocupa 4 colunas (1/3 da tela exato).
                    col={
                        "xs": 12,
                        "sm": 12,
                        "md": 4,
                        "lg": 4,
                        "xl": 4,
                    },
                    alignment=ft.Alignment.CENTER_LEFT, # Joga o texto para a extrema esquerda da sua coluna
                    content=ft.Text(
                        "Evalytics",
                        size=14,
                        weight=ft.FontWeight.BOLD,
                        color=COR_TEXTO_TITULO,
                    ),
                ),

                # 2. BLOCO CENTRAL: Slogan / Descrição Curta
                ft.Container(
                    col={
                        "xs": 12,
                        "sm": 12,
                        "md": 4, # Ocupa mais 1/3 da tela
                        "lg": 4,
                        "xl": 4,
                    },
                    alignment=ft.Alignment.CENTER, # Mantém o texto no centro absoluto
                    content=ft.Text(
                        "Avaliação institucional orientada por dados",
                        size=12,
                        color=COR_TEXTO_SECUNDARIO,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ),

                # 3. BLOCO DA DIREITA: Copyright
                ft.Container(
                    col={
                        "xs": 12,
                        "sm": 12,
                        "md": 4, # Ocupa o último 1/3 da tela (4 + 4 + 4 = 12 colunas)
                        "lg": 4,
                        "xl": 4,
                    },
                    alignment=ft.Alignment.CENTER_RIGHT, # Joga o copyright para a extrema direita
                    content=ft.Text(
                        "© 2026 Evalytics",
                        size=12,
                        color=COR_TEXTO_SECUNDARIO,
                    ),
                ),
            ],
        ),
    )