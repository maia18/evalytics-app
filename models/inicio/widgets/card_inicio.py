from typing import Callable
import flet as ft

from components.core.constants.constants import (
    CARD, 
    BORDA, 
    TEXTO_PRINCIPAL, 
    COR_PRIMARIA, 
    COR_TEXTO_SECUNDARIO,
)
from components.core.theme.border_utils import criar_borda_uniforme

from models.inicio.core.card_hover import obter_funcao_hover # Importa a nova fábrica de funções separada para a lógica de hover (Closure)

def criar_card(
    layout, titulo: str,
    descricao: str,
    icone: str,
    rota: str,
    mudar_tela: Callable[[str], None],
) -> ft.Container:
    """Gera um cartão interativo padronizado para uso como atalho de navegação."""
    
    # Ícone de seta invisível por padrão (TRANSPARENT), que aparecerá suavemente via animação de opacidade
    seta_indicadora = ft.Icon(
        ft.Icons.ARROW_FORWARD_ROUNDED,
        color=ft.Colors.TRANSPARENT,
        size=18,
        animate_opacity=200,
    )

    # Container estilizado que serve de 'fundo' arredondado para o ícone principal do atalho
    badge_icone = ft.Container(
        width=44, height=44, border_radius=10, bgcolor=ft.Colors.with_opacity(0.12, COR_PRIMARIA),
        alignment=ft.alignment.Alignment.CENTER, content=ft.Icon(icone, color=COR_PRIMARIA, size=22),
    )

    # Estrutura principal do cartão interativo
    card = ft.Container(
        width=300,
        height=200, # Altura travada para garantir alinhamento vertical perfeito na grade (ResponsiveRow)
        bgcolor=layout.cores[CARD], padding=20, border_radius=14,
        border=criar_borda_uniforme(layout.cores[BORDA]),
        
        # Sombra inicial invisível (blur_radius=0), preparada para aparecer na animação de hover
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=0,
            color=ft.Colors.with_opacity(0.18, COR_PRIMARIA),
            offset=ft.Offset(0, 6)
        ),
        animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
        ink=True,
        on_click=lambda e: mudar_tela(rota),
        
        # Conteúdo interno distribuído em coluna com espaçamento fixo
        content=ft.Column(
            spacing=12,
            controls=[
                ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER, controls=[badge_icone, seta_indicadora]),
                ft.Text(titulo, weight="bold", size=16, color=layout.cores[TEXTO_PRINCIPAL]),
                ft.Text(descricao, size=12, color=COR_TEXTO_SECUNDARIO),
            ],
        ),
    )
    
    # Usa a fábrica importada para gerar e acoplar a função de evento do hover, injetando as referências exatas deste cartão recém-criado na memória.
    card.on_hover = obter_funcao_hover(layout, card, seta_indicadora)
    
    return card