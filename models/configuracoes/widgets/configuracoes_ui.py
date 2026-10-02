import flet as ft
from components.core.constants.constants import (
    TEXTO_PRINCIPAL, 
    CARD
)

def criar_layout_principal(
    cores_layout: dict, 
    menu_abas: ft.Control, 
    area_conteudo_aba: ft.Control
) -> ft.Column:
    """
    Constrói a hierarquia visual principal (o "esqueleto") da página de configurações.
        Esta função atua como um 'Wrapper' de layout: ela não cria as abas nem o conteúdo, apenas os recebe prontos e os organiza perfeitamente na tela.
    """
    
    return ft.Column(
        expand=True,
        
        controls=[
            # 1. Cabeçalho da Página (Título e Subtítulo)
            ft.Text(
                "Configurações do Sistema", 
                size=28, 
                weight="bold", 
                color=cores_layout[TEXTO_PRINCIPAL]
            ),
            ft.Text(
                "Gerencie indicadores, acessos e manutenção de dados.", 
                size=16,
                color=ft.Colors.GREY # Cor neutra para não competir com o título principal
            ),
            
            ft.Divider(
                height=20, 
                color=ft.Colors.TRANSPARENT
            ),
            
            # 2. Área Principal de Configurações (Card Branco/Escuro)
            ft.Container(
                expand=True, 
                
                bgcolor=cores_layout[CARD], 
                border_radius=10, 
                padding=20,
                
                # Sombra sutil para dar o aspecto de "folha" ou "painel" flutuante sobre o fundo da aplicação.
                shadow=ft.BoxShadow(
                    spread_radius=1, 
                    blur_radius=5, 
                    color=ft.Colors.BLACK12
                ),
                
                # O interior do Card é outra Coluna para empilhar o Menu e o Conteúdo
                content=ft.Column(
                    expand=True, # Repassa o comportamento de expandir para o conteúdo interno
                    controls=[
                        
                        # 2.1 Injeta o menu de navegação (As abas clicáveis) recebido por parâmetro
                        menu_abas,
                        
                        # Linha divisória real e visível separando o menu do conteúdo em si
                        ft.Divider(
                            height=20, 
                            color=ft.Colors.GREY_200
                        ),
                        
                        # 2.2 Área do Conteúdo Dinâmico
                        ft.Container(
                            expand=True, 
                            padding=10, 
                            
                            # Injeta o painel de conteúdo específico da aba selecionada
                            content=area_conteudo_aba
                        ),
                    ],
                ),
            ),
        ],
    )