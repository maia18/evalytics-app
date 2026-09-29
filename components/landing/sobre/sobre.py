import flet as ft

from components.landing.sobre.conteudo import criar_sobre_conteudo
from components.landing.sobre.visual import criar_sobre_visual

def criar_secao_sobre() -> ft.Container:
    """
    Constrói a seção "Sobre" completa, orquestrando o layout responsivo.
        Posiciona o conteúdo em texto de um lado e o elemento visual do outro em telas grandes.
    """

    # Instancia as duas metades da seção
    sobre_conteudo = criar_sobre_conteudo()
    sobre_visual = criar_sobre_visual()

    return ft.Container(
        # Cria uma âncora para permitir navegação direta via scroll (ex: link no menu superior)
        key=ft.ScrollKey("sobre"),
        padding=ft.Padding.symmetric(
            horizontal=20,
            vertical=75, # Mantém a consistência de respiro vertical com as outras seções
        ),
        
        # O ResponsiveRow divide a tela em 12 colunas imaginárias
        content=ft.ResponsiveRow(
            columns=12,
            alignment=ft.MainAxisAlignment.CENTER,       # Centraliza o bloco todo horizontalmente
            vertical_alignment=ft.CrossAxisAlignment.CENTER, # Centraliza os itens pelo eixo vertical (meio a meio)
            run_spacing=35, # Espaçamento gerado quando a tela é pequena e o visual "cai" para debaixo do texto
            controls=[
                
                # METADE ESQUERDA: Textos
                ft.Container(
                    col={
                        "xs": 12, # Celular: Ocupa toda a largura (100%)
                        "sm": 12,
                        "md": 12, # Tablet: Ocupa toda a largura
                        "lg": 7,  # Desktop: Ocupa 7 das 12 colunas (~58% do espaço)
                        "xl": 7,
                    },
                    padding=ft.Padding.only(
                        right=20, # Cria uma margem para o texto não encostar no card visual em telas grandes
                    ),
                    content=sobre_conteudo,
                ),

                # METADE DIREITA: Card Visual
                ft.Container(
                    col={
                        "xs": 12, 
                        "sm": 12,
                        "md": 12,
                        "lg": 5,  # Desktop: Ocupa as 5 colunas restantes (7 + 5 = 12)
                        "xl": 5,
                    },
                    alignment=ft.Alignment.CENTER, # Garante que o card fique centralizado na sua própria coluna
                    content=sobre_visual,
                ),
            ],
        ),
    )