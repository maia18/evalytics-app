import flet as ft
from components.core.constants.constants import (
    COR_CARD,
)
from components.landing.helpers import criar_etapa
from components.landing.sobre.conteudo import criar_sobre_conteudo

def criar_secao_sobre() -> ft.Container:
    """
    Constrói a seção explicativa da Landing Page, dividindo a tela entre
        um bloco de texto de apresentação e uma lista visual de etapas (1, 2, 3).
    """

    # 1. Recupera o bloco de texto (lado esquerdo no desktop)
    sobre_conteudo = criar_sobre_conteudo()
    
    # 2. Constrói a lista de etapas (lado direito no desktop)
    etapas = ft.Column(
        spacing=22, # Respiro uniforme entre as etapas
        controls=[
            criar_etapa("01", "Avaliar", "Colete informações por meio das avaliações institucionais."),
            criar_etapa("02", "Analisar", "Organize os resultados e acompanhe os indicadores."),
            criar_etapa("03", "Melhorar", "Use as informações para apoiar decisões e melhorias."),
        ],
    )

    # 3. Retorna a junção desses blocos encapsulados e responsivos
    return ft.Container(
        key=ft.ScrollKey("sobre"), # Ponto de âncora para o scroll da página
        padding=ft.Padding.symmetric(
            horizontal=60,
            vertical=75,
        ),
        bgcolor=COR_CARD,
        content=ft.ResponsiveRow(
            columns=12,
            vertical_alignment=ft.CrossAxisAlignment.CENTER, # Mantém ambos os lados alinhados pelo meio
            run_spacing=35, # Espaço aplicado quando quebra de linha (mobile)
            controls=[
                
                # =====================================================
                # BLOCO ESQUERDO: TEXTO
                # =====================================================
                ft.Container(
                    # No desktop ocupa metade da tela (6/12), no mobile ocupa tudo (12/12)
                    col={"xs": 12, "sm": 12, "md": 6, "lg": 6, "xl": 6},
                    padding=ft.Padding.only(
                        right=40, # Evita colisão visual com a lista de etapas
                    ),
                    content=sobre_conteudo,
                ),

                # =====================================================
                # BLOCO DIREITO: ETAPAS
                # =====================================================
                ft.Container(
                    col={"xs": 12, "sm": 12, "md": 6, "lg": 6, "xl": 6},
                    padding=ft.Padding.only(
                        top=10, # Pequeno ajuste vertical fino para equilibrar visualmente com o título da esquerda
                    ),
                    content=etapas,
                ),
            ],
        ),
    )