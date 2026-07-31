import flet as ft
from typing import Callable
from components.core.constants.constants import (
    TEXTO_PRINCIPAL, 
    SURFACE, 
    COR_PRIMARIA,
)
from components.layout.topbar.topbar_utils import obter_icone_tema
from utils.services.location_service import obter_localizacao

# Constrói a disposição dos elementos internos da TopBar
def criar_topbar_content(
    titulo: str,
    subtitulo: str,
    dark_mode: bool,
    cores: dict[str, str],
    menu_button: ft.IconButton,
    atualizar_tema: Callable[[], None],
) -> ft.Row:
    
    local_atual = obter_localizacao() # Busca a localização do usuário a partir de um serviço externo simulado
    icone_tema = obter_icone_tema(dark_mode) # Define se o ícone do botão de tema será uma lua ou um sol com base no estado atual

    return ft.Row(
        
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN, # Empurra o bloco da esquerda para o início e o da direita para o final do espaço disponível
        controls=[
            # ==========================================
            # LADO ESQUERDO: Menu, Título e Subtítulo
            # ==========================================
            ft.Row(
                spacing=10,
                controls=[
                    menu_button,
                    ft.Column(
                        spacing=0,
                        controls=[
                            ft.Text(titulo, size=20, weight="bold", color=cores[TEXTO_PRINCIPAL]),
                            ft.Text(subtitulo, size=12, color=ft.Colors.GREY),
                        ],
                    ),
                ],
            ),
            # ==========================================
            # LADO DIREITO: Localização, Tema e Perfil
            # ==========================================
            ft.Row(
                controls=[
                    # Container estilisado para exibir o local atual
                    ft.Container(
                        padding=10,
                        border_radius=8,
                        bgcolor=cores[SURFACE],
                        content=ft.Row(
                            spacing=6,
                            controls=[
                                ft.Icon(ft.Icons.LOCATION_ON_OUTLINED, size=18, color=COR_PRIMARIA),
                                ft.Text(local_atual, size=14, weight="w500", color=cores[TEXTO_PRINCIPAL]),
                            ],
                        ),
                    ),
                    ft.IconButton(icon=icone_tema, on_click=lambda e: atualizar_tema()), # Botão funcional que inverte o tema ao ser clicado
                    ft.IconButton(icon=ft.Icons.NOTIFICATIONS_NONE),  # Espaço reservado (placeholder) para um futuro sistema de notificações
                    ft.CircleAvatar(radius=18, color=cores[TEXTO_PRINCIPAL], content=ft.Text("AC")), # Foto de perfil / Avatar do usuário logado
                ],
            ),
        ],
    )