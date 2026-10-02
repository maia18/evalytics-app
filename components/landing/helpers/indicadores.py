import flet as ft

from components.core.constants.constants import (
    COR_TEXTO_SECUNDARIO,
    COR_PRIMARIA,
)

def criar_indicador(titulo: str, valor: str) -> ft.Container:
    """
    Cria um mini-card de indicador (kpi) utilizado para destacar métricas ou números.
        Este componente é usado dentro do painel flutuante (dashboard) na seção Hero.
    """

    return ft.Container(
        expand=True, # Garante que ambos dividam o espaço igualmente (50% da largura para cada).
        padding=15, # Espaçamento interno confortável para não colar o texto nas bordas.
        
        # Cria um fundo suave usando a cor primária com apenas 6% de opacidade.
        bgcolor=ft.Colors.with_opacity(
            0.06,
            COR_PRIMARIA,
        ),
        border_radius=10, # Arredondamento das bordas do mini-card.
        
        # Empilha o título e o valor verticalmente
        content=ft.Column(
            spacing=5, # Espaçamento bem curto (5px) para manter o rótulo e o número agrupados visualmente
            controls=[
                
                # 1. Rótulo (Título da métrica)
                ft.Text(
                    titulo,
                    size=12,                     # Fonte pequena pois é apenas texto de apoio
                    color=COR_TEXTO_SECUNDARIO,  # Cor mais neutra/cinza para não roubar a atenção do número
                ),

                # 2. Dado em Destaque (Valor)
                ft.Text(
                    valor,
                    size=26,                     # Fonte bem maior para criar forte hierarquia visual
                    weight=ft.FontWeight.BOLD,   # Negrito para impacto
                    color=COR_PRIMARIA,          # Usa a cor da marca para dar vida e foco ao número
                ),
            ],
        ),
    )