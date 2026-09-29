import flet as ft

from components.core.constants.constants import (
    COR_TEXTO_TITULO,
    COR_TEXTO_SECUNDARIO,
    COR_PRIMARIA,
    COR_CARD,
)
from components.landing.helpers import criar_indicador

def criar_painel_hero() -> ft.Container:
    """
    Cria um card ilustrativo simulando o painel de controle (dashboard) do sistema.
        Serve como chamariz visual para a Landing Page.
    """

    return ft.Container(
        width=430,          # Largura fixa máxima para não distorcer o design
        padding=32,
        bgcolor=COR_CARD,
        border_radius=16,
        
        # Cria o efeito de profundidade (3D/Elevação) fazendo o card "flutuar"
        shadow=ft.BoxShadow(
            blur_radius=20,
            color=ft.Colors.BLACK12,
        ),
        
        content=ft.Column(
            spacing=20,
            controls=[
                
                # Cabeçalho do Card: Título e Badge de Status
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN, # Joga título para a esquerda e badge para a direita
                    controls=[
                        ft.Text(
                            "Visão geral",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color=COR_TEXTO_TITULO,
                        ),

                        # Badge (Etiqueta) de "Ativo"
                        ft.Container(
                            padding=ft.Padding.symmetric(
                                horizontal=10,
                                vertical=5,
                            ),
                            bgcolor=ft.Colors.with_opacity(
                                0.10,
                                COR_PRIMARIA, # Fundo translúcido com a cor principal
                            ),
                            border_radius=20, # Bordas bem arredondadas (formato pílula)
                            content=ft.Text(
                                "Ativo",
                                size=11,
                                color=COR_PRIMARIA,
                                weight=ft.FontWeight.BOLD,
                            ),
                        ),
                    ],
                ),

                # Linha com os mini-cards de indicadores numéricos
                ft.Row(
                    spacing=15,
                    controls=[
                        criar_indicador("Avaliações", "128"),
                        criar_indicador("Indicadores", "24"),
                    ],
                ),

                # Divisor sutil (Linha horizontal separadora)
                ft.Container(
                    height=1,
                    bgcolor=ft.Colors.BLACK12,
                ),

                # Seção inferior: Progresso
                ft.Text(
                    "Acompanhamento institucional",
                    size=14,
                    color=COR_TEXTO_SECUNDARIO,
                ),

                # Barra indicadora visual simulando carregamento/meta atingida
                ft.ProgressBar(
                    value=0.78,             # Representa 78% preenchido
                    color=COR_PRIMARIA,     # Cor da barra cheia
                    bgcolor=ft.Colors.BLACK12, # Cor da trilha de fundo
                ),

                # Legenda da barra de progresso (Texto esquerdo e Porcentagem direita)
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text(
                            "Progresso das avaliações",
                            size=12,
                            color=COR_TEXTO_SECUNDARIO,
                        ),
                        ft.Text(
                            "78%",
                            size=12,
                            weight=ft.FontWeight.BOLD,
                            color=COR_PRIMARIA,
                        ),
                    ],
                ),
            ],
        ),
    )