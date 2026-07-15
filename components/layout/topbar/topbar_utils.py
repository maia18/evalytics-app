import flet as ft

def obter_icone_tema(dark_mode: bool):
    """Retorna o ícone correto para o tema"""
    return ft.Icons.LIGHT_MODE_OUTLINED if dark_mode else ft.Icons.DARK_MODE_OUTLINED
