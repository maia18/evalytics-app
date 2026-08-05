from typing import Callable
import flet as ft

from components.layout.responsive.responsive import ResponsiveLayout
from models.inicio.widgets.card_inicio import criar_card
from components.core.constants.constants import (
    CARD, 
    BORDA, 
    TEXTO_PRINCIPAL, 
    COR_PRIMARIA, 
    COR_TEXTO_SECUNDARIO,
)
from components.core.constants.texts import (
    TXTS_INICIO, 
    TXTS_DASHBOARD, 
    TXTS_CURSOS, 
    TXTS_RELATORIOS, 
    TXTS_CONFIGS,
)

def ViewInicio(page: ft.Page, mudar_tela: Callable[[str], None]) -> ft.View:
    """Constrói a tela inicial (Home): hero de boas-vindas + grade de atalhos de navegação."""

    # Inicializa o layout responsivo injetando os textos globais armazenados nas constantes.
    layout = ResponsiveLayout(
        page, TXTS_INICIO[0], TXTS_INICIO[1], mudar_tela=mudar_tela,
    ) 

    # Criação do "Hero Banner" (Bloco superior de boas-vindas e ações rápidas).
    hero = ft.Container(
        bgcolor=layout.cores[CARD], padding=28, border_radius=14,
        
        # Aplica bordas respeitando o tema atual (claro/escuro) e adiciona sombra difusa
        border=ft.Border(
            left=ft.BorderSide(1, layout.cores[BORDA]), top=ft.BorderSide(1, layout.cores[BORDA]),
            right=ft.BorderSide(1, layout.cores[BORDA]), bottom=ft.BorderSide(1, layout.cores[BORDA]),
        ),
        shadow=ft.BoxShadow(spread_radius=0, blur_radius=20, color=ft.Colors.with_opacity(0.10, COR_PRIMARIA), offset=ft.Offset(0, 8)),
        
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER,
            wrap=True, spacing=20, run_spacing=16,
            controls=[
                ft.Column(
                    spacing=8, tight=True,
                    controls=[
                        # Título e subtítulo do Hero
                        ft.Text(TXTS_INICIO[2], weight="bold", size=22, color=layout.cores[TEXTO_PRINCIPAL]),
                        ft.Text("Crie, acompanhe e analise avaliações institucionais em um só lugar.", size=13, color=COR_TEXTO_SECUNDARIO),
                        ft.Container(height=6),
                        
                        # Call to Action (CTA): Botão direto para preencher um novo formulário
                        ft.ElevatedButton(
                            TXTS_INICIO[3], icon=ft.Icons.ADD_ROUNDED, bgcolor=COR_PRIMARIA, color=ft.Colors.WHITE,
                            height=44, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), elevation=0),
                            on_click=lambda e: mudar_tela("/formulario"),
                        ),
                    ],
                ),
            ],
        ),
    )

    '''
    Container de grade responsiva (ResponsiveRow).
        O atributo 'col' ajusta a largura ocupada pelo card em diferentes tamanhos de tela:
            xs (celular) = 12 colunas (ocupa 100%), sm = 6 colunas (50%), md = 4 colunas (33%), lg = 3 colunas (25%).
    '''
    grade_cards = ft.ResponsiveRow(
        spacing=20, run_spacing=20,
        controls=[
            ft.Container(col={"xs": 12, "sm": 6, "md": 4, "lg": 3}, content=criar_card(layout, TXTS_DASHBOARD[0], TXTS_DASHBOARD[1], ft.Icons.GRID_VIEW, "/dashboard", mudar_tela)),
            ft.Container(col={"xs": 12, "sm": 6, "md": 4, "lg": 3}, content=criar_card(layout, TXTS_CURSOS[0], TXTS_CURSOS[1], ft.Icons.MENU_BOOK, "/cursos", mudar_tela)),
            ft.Container(col={"xs": 12, "sm": 6, "md": 4, "lg": 3}, content=criar_card(layout, TXTS_RELATORIOS[0], TXTS_RELATORIOS[1], ft.Icons.PIE_CHART, "/relatorios", mudar_tela)),
            ft.Container(col={"xs": 12, "sm": 6, "md": 4, "lg": 3}, content=criar_card(layout, TXTS_CONFIGS[0], TXTS_CONFIGS[1], ft.Icons.VIEW_COMFY, "/configuracoes", mudar_tela)),
        ],
    )

    conteudo = ft.Column(expand=True, controls=[hero, ft.Container(height=24), grade_cards]) # Montagem final da página: Hero no topo + espaçamento de 24px + grade de cartões

    layout.add_content(conteudo)
    return layout.criar_view("/inicio")