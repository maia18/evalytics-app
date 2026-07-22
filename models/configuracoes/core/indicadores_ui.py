import flet as ft 

def criar_linha_indicador(item, abrir_modal_criterios, abrir_modal_edicao, preparar_exclusao): 
    """Cria o card retangular (linha) para representar um único indicador cadastrado."""
    # Define verde para ATIVO e amarelo/âmbar para qualquer outro status
    cor_status = "green600" if item.get("status") == "ATIVO" else "amber600" 
    
    return ft.Container( 
        padding=15, 
        bgcolor="white", 
        border_radius=8, 
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color="black12"), 
        content=ft.Row( 
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN, 
            controls=[ 
                # Bloco do Título clicável (Abre os critérios)
                ft.Container( 
                    content=ft.Text(item["titulo"], size=15, weight="w500", color="blue700"), 
                    expand=True, # Empurra os próximos elementos para a direita
                    on_click=lambda e, i=item: abrir_modal_criterios(e, i) 
                ), 
                # Etiqueta visual de Status
                ft.Container( 
                    bgcolor=cor_status, padding=5, border_radius=4, 
                    content=ft.Text(item.get("status", "ATIVO"), size=12, color="white", weight="bold") 
                ), 
                # Botões de ação rápida
                ft.Row([ 
                    ft.IconButton(icon=ft.Icons.EDIT, icon_color="blue700", tooltip="Editar", on_click=lambda e, i=item: abrir_modal_edicao(e, i)), 
                    ft.IconButton(icon=ft.Icons.DELETE, icon_color="red700", tooltip="Excluir", on_click=lambda e: preparar_exclusao(item)) 
                ]) 
            ] 
        ) 
    ) 

def criar_pasta_indicador(titulo, qtd, abrir_pasta): 
    """Cria um grande botão com visual de 'Pasta' para agrupar indicadores de um mesmo eixo."""
    return ft.Container( 
        bgcolor="#F4F6F9", 
        border_radius=8, 
        padding=20, 
        ink=True, # Adiciona efeito visual de onda ('ripple') ao clicar nativo do Material Design
        on_click=lambda e: abrir_pasta(titulo), 
        content=ft.Row( 
            spacing=15, 
            controls=[ 
                ft.Icon(ft.Icons.FOLDER, color="blue700", size=28), 
                ft.Column( 
                    spacing=2, 
                    controls=[ 
                        ft.Text(titulo, size=16, weight="bold", color="black87"), 
                        ft.Text(f"{qtd} indicadores", size=13, color="black54"), # Mostra o count total dinâmico
                    ] 
                ) 
            ] 
        ) 
    ) 