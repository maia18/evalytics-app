import flet as ft 

# Cria um item de menu com ícone e texto
def criar_item_menu(icone: str, texto: str, rota: str, dark_mode: bool, cor_texto: str, mudar_tela) -> ft.Container: 
    """
    Cria o botão de navegação tradicional contendo um ícone à esquerda alinhado a um texto.
    """
    return ft.Container( 
        height=45, # A mesma altura fixa do botão de ícone para manter o design consistente
        content=ft.TextButton( 
            content=ft.Row( 
                spacing=12, # Distância entre o ícone e o texto dentro da linha
                controls=[ 
                    ft.Icon( 
                        icone, 
                        size=20, # Ícone sutilmente menor que a versão colapsada (que era 24)
                        # Aplica um tom de cinza (mais escuro no modo claro, mais claro no modo escuro) 
                        # para não competir tanta atenção com o texto principal
                        color="grey700" if not dark_mode else "grey300", 
                    ), 
                    ft.Text( 
                        texto, 
                        size=14, 
                        weight="w500", # Peso médio da fonte para legibilidade
                        color=cor_texto, 
                    ), 
                ], 
            ), 
            style=ft.ButtonStyle( 
                padding=10, 
                shape=ft.RoundedRectangleBorder(radius=8), # Bordas arredondadas
                overlay_color="#3C3C3C" if dark_mode else "#CCCCCC", # Efeito hover/ripple adaptável ao tema atual
            ), 
            # Gatilho de navegação
            on_click=lambda _: mudar_tela(rota) if mudar_tela else None, 
        ), 
    ) 