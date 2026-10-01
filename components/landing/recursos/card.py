import flet as ft

from components.landing.helpers import criar_card_recurso

def criar_card_responsivo(icone, titulo: str, descricao: str) -> ft.Container:
    """
    Atua como um 'wrapper' (embrulho) responsivo para o card de recurso.
        Define quantas colunas o card deve ocupar dependendo do tamanho da tela.
    """

    return ft.Container(
        # Configuração do Grid de 12 colunas (ResponsiveRow):
        col={
            "xs": 12, # Celulares (Telas extra pequenas): Ocupa as 12 colunas (1 por linha)
            "sm": 12, # Celulares deitados/Tablets pequenos: Mantém 1 por linha
            "md": 6,  # Tablets (Telas médias): Ocupa 6 colunas (Caberão 2 cards por linha)
            "lg": 3,  # Notebooks/Desktops (Telas grandes): Ocupa 3 colunas (Caberão 4 cards por linha)
            "xl": 3,  # Monitores Ultrawide: Mantém 4 cards por linha
        },
        
        # Garante que, caso o espaço da coluna seja maior que a largura fixa do card (235px), o card fique perfeitamente centralizado no espaço disponível.
        alignment=ft.Alignment.CENTER,
        
        # Injeta o componente visual base criado anteriormente
        content=criar_card_recurso(
            icone,
            titulo,
            descricao,
        ),
    )