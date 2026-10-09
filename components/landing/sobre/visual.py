import flet as ft
from components.core.constants.constants import (
    COR_TEXTO_TITULO,
    COR_CARD,
    COR_PRIMARIA,
)
from components.landing.helpers import criar_etapa # Importação de um helper que cria as linhas de passo-a-passo (01, 02, 03)

def criar_sobre_visual() -> ft.Container:
    """Cria um componente visual simulando um mini-painel ou infográfico."""

    return ft.Container(
        width=420,       # Limita a largura para manter a estética de um card elegante
        height=270,      # Altura fixa para manter o alinhamento consistente com o texto vizinho
        padding=28,
        bgcolor=COR_CARD,
        border_radius=16,
        
        # Aplica uma sombra esfumaçada para destacar o card do fundo da página
        shadow=ft.BoxShadow(
            blur_radius=20,
            color=ft.Colors.BLACK12,
        ),
        
        content=ft.Column(
            spacing=18,
            controls=[
                
                # Cabeçalho do Card (Bolinha indicadora + Título)
                ft.Row(
                    spacing=10,
                    controls=[
                        # Pequeno indicador visual (ponto/bullet point customizado)
                        ft.Container(
                            width=10,
                            height=10,
                            bgcolor=COR_PRIMARIA,
                            border_radius=10, # Borda arredondada no mesmo valor de width/height cria um círculo perfeito
                        ),

                        ft.Text(
                            "Fluxo de avaliação",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=COR_TEXTO_TITULO,
                        ),
                    ],
                ),

                # Lista de Etapas (Utilizando a função helper para evitar repetição de código)
                criar_etapa(
                    "01",
                    "Avaliar",
                    "Coleta das percepções institucionais.",
                ),

                criar_etapa(
                    "02",
                    "Analisar",
                    "Organização dos resultados e indicadores.",
                ),

                criar_etapa(
                    "03",
                    "Melhorar",
                    "Informações para apoiar ações de melhoria.",
                ),
            ],
        ),
    )