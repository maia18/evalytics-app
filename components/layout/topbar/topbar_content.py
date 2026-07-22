import flet as ft 
from utils.services.location_service import obter_localizacao 
from components.layout.topbar.topbar_utils import obter_icone_tema 
from components.core.constants.constants import * 

def criar_topbar_content(titulo, subtitulo, dark_mode, cores, menu_button, atualizar_tema): 
    """
    Constrói a disposição dos elementos internos da TopBar.
    """
    local_atual = obter_localizacao() # Recupera a string de localização do serviço externo
    icone_tema = obter_icone_tema(dark_mode) # Define o ícone correto dependendo do estado atual

    return ft.Row( 
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN, # Empurra os blocos para as pontas (Esquerda e Direita)
        controls=[ 
            # Lado esquerdo
            ft.Row( 
                spacing=10, 
                controls=[ 
                    menu_button, # Injeta o botão de abrir sidebar
                    ft.Column( 
                        spacing=0, # Cola o subtítulo logo abaixo do título
                        controls=[ 
                            ft.Text(titulo, size=20, weight="bold", color=cores[TEXTO_PRINCIPAL]), 
                            ft.Text(subtitulo, size=12, color="grey"), 
                        ], 
                    ), 
                ], 
            ), 
            # Lado direito
            ft.Row( 
                controls=[ 
                    # Emblema com o local atual do usuário
                    ft.Container( 
                        padding=10, 
                        border_radius=8, 
                        bgcolor=cores[SURFACE], # Cor de destaque leve
                        content=ft.Row( 
                            spacing=6, 
                            controls=[ 
                                ft.Icon(ft.Icons.LOCATION_ON_OUTLINED, size=18, color=COR_PRIMARIA), 
                                ft.Text(local_atual, size=14, weight="w500", color=cores[TEXTO_PRINCIPAL]), 
                            ], 
                        ), 
                    ), 
                    # Botões de Ação do Sistema e Perfil
                    ft.IconButton(icon=icone_tema, on_click=lambda e: atualizar_tema()), # Executa a troca de cores
                    ft.IconButton(icon=ft.Icons.NOTIFICATIONS_NONE), # Ícone decorativo/futuro para avisos
                    ft.CircleAvatar(radius=18, color=cores[TEXTO_PRINCIPAL], content=ft.Text("AC")), # Placeholder para avatar
                ], 
            ), 
        ], 
    ) 