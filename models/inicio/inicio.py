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
    """
    
    # Inicializa o layout responsivo padrão, consumindo os textos definidos nas constantes
    layout = ResponsiveLayout(
        page, 
        TXTS_INICIO[0], # Título da aba/página (Ex: "Início")
        TXTS_INICIO[1], # Título de boas-vindas (Ex: "Bem-vindo ao Evalytics")
        mudar_tela=mudar_tela
    )

    # Estrutura principal da página
    conteudo = ft.Column(
        expand=True, # Ocupa todo o espaço vertical disponível
        controls=[
            # Painel de destaque (Hero Section) no topo da tela
            ft.Container(
                bgcolor=layout.cores[CARD], # Cor de fundo adaptável (claro/escuro)
                padding=25,
                border_radius=12,
                # Aplica bordas delimitadoras em todos os lados
                border=ft.Border(
                    left=ft.BorderSide(1, layout.cores[BORDA]),
                    top=ft.BorderSide(1, layout.cores[BORDA]),
                    right=ft.BorderSide(1, layout.cores[BORDA]),
                    bottom=ft.BorderSide(1, layout.cores[BORDA])
                ),
                content=ft.Column([
                    # Subtítulo descritivo do sistema
                    ft.Text(
                        TXTS_INICIO[2], # Ex: "Sistema de Avaliação Institucional"
                        weight="bold",
                        size=20,
                        color=layout.cores[TEXTO_PRINCIPAL]
                    ),
                    # Botão de Ação Principal (Call to Action)
                    ft.ElevatedButton(
                        TXTS_INICIO[3], # Texto do botão (Ex: "Iniciar nova avaliação")
                        bgcolor=COR_PRIMARIA,
                        color="white",
                        # Gatilho que redireciona o usuário diretamente para a rota do formulário
                        on_click=lambda e: mudar_tela("/formulario")
                    )
                ])
            ),
            
            # Espaçador vertical invisível para separar o banner dos cartões
            ft.Container(height=20),
            
            # Grade de cartões de navegação (Menu de atalhos rápidos)
            ft.Row(
                wrap=True, # Propriedade crucial: permite que os cartões pulem para a linha de baixo se não houver largura suficiente
                spacing=20, # Espaço horizontal entre os cartões
                run_spacing=20, # Espaço vertical entre as linhas de cartões (quando ocorre a quebra)
                controls=[
                    # Instancia os cartões de menu repassando as constantes de texto e ícones
                    criar_card(layout, TXTS_AVALIACAO[0], TXTS_AVALIACAO[1], ft.Icons.ADD, "/formulario", mudar_tela),
                    criar_card(layout, TXTS_DASHBOARD[0], TXTS_DASHBOARD[1], ft.Icons.GRID_VIEW, "/dashboard", mudar_tela),
                    criar_card(layout, TXTS_CURSOS[0], TXTS_CURSOS[1], ft.Icons.MENU_BOOK, "/cursos", mudar_tela),
                    criar_card(layout, TXTS_RELATORIOS[0], TXTS_RELATORIOS[1], ft.Icons.PIE_CHART, "/relatorios", mudar_tela),
                ]
            )
        ]
    )

    # Injeta o conteúdo montado na área central do layout responsivo
    layout.add_content(conteudo)
    
    # Retorna a View estruturada e pronta para ser registrada no sistema de rotas (Router) do Flet
    return layout.criar_view("/inicio")