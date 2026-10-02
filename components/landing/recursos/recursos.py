import flet as ft

from components.core.constants.constants import (
    COR_TEXTO_TITULO,
    COR_TEXTO_SECUNDARIO,
    COR_CARD,
)

from components.landing.recursos.card import criar_card_responsivo

def criar_secao_recursos() -> ft.Container:
    """
    Constrói a seção "Recursos/Features" da Landing Page.
        Composta por um cabeçalho centralizado e uma grade de 4 cards responsivos.
    """

    # 1. Bloco de Cabeçalho (Título e Subtítulo da seção)
    titulo_recursos = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER, # Centraliza os textos horizontalmente
        spacing=8, # Espaçamento curto entre o título principal e o texto de apoio
        controls=[
            ft.Text(
                "Uma plataforma para melhoria contínua",
                size=28,
                weight=ft.FontWeight.BOLD,
                color=COR_TEXTO_TITULO,
                text_align=ft.TextAlign.CENTER,
            ),

            ft.Container(
                # Padding horizontal no texto evita que ele encoste nas bordas em telas de celular
                padding=ft.Padding.symmetric(
                    horizontal=10,
                ),
                content=ft.Text(
                    "Organize avaliações, acompanhe indicadores e "
                    "transforme informações acadêmicas em apoio "
                    "para a gestão institucional.",
                    size=15,
                    color=COR_TEXTO_SECUNDARIO,
                    text_align=ft.TextAlign.CENTER,
                ),
            ),
        ],
    )

    # 2. Grade de Cards (ResponsiveRow)
    cards_recursos = ft.ResponsiveRow(
        columns=12, # Define o sistema base de 12 colunas para os filhos (os cards)
        alignment=ft.MainAxisAlignment.CENTER,

        run_spacing=18, # run_spacing controla o espaço VERTICAL entre as linhas quando os cards "quebram" para a linha de baixo em telas menores (tablets e celulares).
        
        controls=[
            criar_card_responsivo(
                ft.Icons.RATE_REVIEW_OUTLINED,
                "Avaliações",
                "Colete e organize avaliações institucionais de forma estruturada.",
            ),
            criar_card_responsivo(
                ft.Icons.INSERT_CHART_OUTLINED,
                "Indicadores",
                "Acompanhe indicadores para compreender os resultados das avaliações.",
            ),
            criar_card_responsivo(
                ft.Icons.SCHOOL_OUTLINED,
                "Cursos",
                "Organize informações relacionadas aos cursos e à realidade acadêmica.",
            ),
            criar_card_responsivo(
                ft.Icons.ASSESSMENT_OUTLINED,
                "Relatórios",
                "Visualize resultados de forma organizada para apoiar a análise institucional.",
            ),
        ],
    )

    # 3. Retorna o Container "Pai" da seção
    return ft.Container(
        key=ft.ScrollKey("recursos"), # Permite usar page.scroll_to(key="recursos") no clique do botão "Conhecer a plataforma" do Hero.

        # Espaçamento generoso para separar visualmente esta seção da anterior e da próxima
        padding=ft.Padding.symmetric(
            horizontal=20,
            vertical=75, # 75px de respiro no topo e na base
        ),
        bgcolor=COR_CARD, # Pode ser usado para dar um fundo levemente diferente (ex: cinza claro) e alternar seções
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=35, # Espaço entre o bloco de título e a grade de cards
            controls=[
                titulo_recursos,
                cards_recursos,
            ],
        ),
    )