import flet as ft
from components.layout.responsive.responsive import ResponsiveLayout
from models.inicio.widgets.card_inicio import criar_card
from components.core.constants.constants import *
from components.core.constants.texts import *

def ViewInicio(page: ft.Page, mudar_tela):
    """
    Constrói a tela inicial (Home) da aplicação.
    Apresenta um painel de boas-vindas com um atalho rápido para iniciar uma avaliação,
    além de uma grade de cartões de navegação para as demais áreas do sistema.

    Aprimoramentos em relação à versão anterior:
        - Hero section com ícone de destaque, sombra e hierarquia tipográfica mais clara.
        - Botão de CTA com ícone e cantos arredondados, alinhado ao padrão do restante do app.
        - Grade de cards usando ResponsiveRow, melhorando o comportamento em telas menores.
    """

    # Inicializa o layout responsivo padrão, consumindo os textos definidos nas constantes
    layout = ResponsiveLayout(
        page,
        TXTS_INICIO[0],  # Título da aba/página (Ex: "Início")
        TXTS_INICIO[1],  # Título de boas-vindas (Ex: "Bem-vindo ao Evalytics")
        mudar_tela=mudar_tela
    )

    # === Painel de destaque (Hero Section) ===
    hero = ft.Container(
        bgcolor=layout.cores[CARD],
        padding=28,
        border_radius=14,
        border=ft.Border(
            left=ft.BorderSide(1, layout.cores[BORDA]),
            top=ft.BorderSide(1, layout.cores[BORDA]),
            right=ft.BorderSide(1, layout.cores[BORDA]),
            bottom=ft.BorderSide(1, layout.cores[BORDA]),
        ),
        # Sombra suave para dar profundidade ao card principal da tela
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=20,
            color=ft.Colors.with_opacity(0.10, COR_PRIMARIA),
            offset=ft.Offset(0, 8),
        ),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            wrap=True,
            spacing=20,
            run_spacing=16,
            controls=[
                ft.Column(
                    spacing=8,
                    tight=True,
                    controls=[
                        ft.Text(
                            TXTS_INICIO[2],  # Ex: "Sistema de Avaliação Institucional"
                            weight="bold",
                            size=22,
                            color=layout.cores[TEXTO_PRINCIPAL],
                        ),
                        ft.Text(
                            "Crie, acompanhe e analise avaliações institucionais em um só lugar.",
                            size=13,
                            color=COR_TEXTO_SECUNDARIO,
                        ),
                        ft.Container(height=6),
                        ft.ElevatedButton(
                            TXTS_INICIO[3],  # Texto do botão (Ex: "Iniciar nova avaliação")
                            icon=ft.Icons.ADD_ROUNDED,
                            bgcolor=COR_PRIMARIA,
                            color="white",
                            height=44,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=10),
                                elevation=0,
                            ),
                            # Gatilho que redireciona o usuário diretamente para a rota do formulário
                            on_click=lambda e: mudar_tela("/formulario"),
                        ),
                    ],
                ),
            ],
        ),
    )

    # === Grade de cartões de navegação (Menu de atalhos rápidos) ===
    grade_cards = ft.ResponsiveRow(
        spacing=20,
        run_spacing=20,
        controls=[
            ft.Container(
                col={"xs": 12, "sm": 6, "md": 4, "lg": 3},
                content=criar_card(layout, TXTS_DASHBOARD[0], TXTS_DASHBOARD[1], ft.Icons.GRID_VIEW, "/dashboard", mudar_tela),
            ),
            ft.Container(
                col={"xs": 12, "sm": 6, "md": 4, "lg": 3},
                content=criar_card(layout, TXTS_CURSOS[0], TXTS_CURSOS[1], ft.Icons.MENU_BOOK, "/cursos", mudar_tela),
            ),
            ft.Container(
                col={"xs": 12, "sm": 6, "md": 4, "lg": 3},
                content=criar_card(layout, TXTS_RELATORIOS[0], TXTS_RELATORIOS[1], ft.Icons.PIE_CHART, "/relatorios", mudar_tela),
            ),
            ft.Container(
                col={"xs": 12, "sm": 6, "md": 4, "lg": 3},
                content=criar_card(layout, TXTS_CONFIGS[0], TXTS_CONFIGS[1], ft.Icons.VIEW_COMFY, "/configuracoes", mudar_tela),
            ),
        ],
    )

    # Estrutura principal da página
    conteudo = ft.Column(
        expand=True,  # Ocupa todo o espaço vertical disponível
        controls=[
            hero,
            ft.Container(height=24),  # Espaçador vertical entre o banner e os cartões
            grade_cards,
        ],
    )

    # Injeta o conteúdo montado na área central do layout responsivo
    layout.add_content(conteudo)

    # Retorna a View estruturada e pronta para ser registrada no sistema de rotas (Router) do Flet
    return layout.criar_view("/inicio")