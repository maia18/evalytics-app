from typing import Callable
import flet as ft

def criar_pasta_indicador(titulo: str, qtd: int, abrir_pasta: Callable[[str], None]) -> ft.Container:
    """Cria um grande botão com visual de 'Pasta' para agrupar indicadores de um mesmo eixo na visualização raiz."""
    return ft.Container(
        bgcolor="#F4F6F9", border_radius=8, padding=20,
        ink=True,  # Adiciona Efeito visual de 'ripple' interativo
        on_click=lambda e: abrir_pasta(titulo),
        content=ft.Row(
            spacing=15,
            controls=[
                ft.Icon(ft.Icons.FOLDER, color=ft.Colors.BLUE_700, size=28),
                ft.Column(
                    spacing=2,
                    controls=[
                        ft.Text(
                            titulo, 
                            size=16, 
                            weight="bold", 
                            color=ft.Colors.BLACK87
                        ),
                        ft.Text(
                            f"{qtd} indicadores", 
                            size=13, 
                            color=ft.Colors.BLACK54
                        ),
                    ],
                ),
            ],
        ),
    )