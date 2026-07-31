import flet as ft
from components.core.constants.constants import COR_PRIMARIA, TEXTO_PRINCIPAL

def criar_logo(cores: dict[str, str], compact: bool = False) -> ft.Container:
    """Cria o cabeçalho da marca na parte superior do menu.

    Responde à flag de menu compactado para omitir o texto da marca se necessário.
    """
    
    # Se a flag 'compact' for True, renderiza apenas o ícone centralizado, ideal para o menu colapsado
    if compact:
        return ft.Container(
            content=ft.Icon(ft.Icons.ANALYTICS, color=COR_PRIMARIA, size=28),
            padding=8,
            alignment=ft.Alignment.CENTER,
        )
        
    # Se o menu estiver expandido, retorna uma linha (Row) contendo o ícone e o nome da marca
    return ft.Container(
        content=ft.Row(
            spacing=10,
            controls=[
                ft.Icon(ft.Icons.ANALYTICS, color=COR_PRIMARIA, size=28),
                ft.Text("Evalytics", size=18, weight="bold", color=cores[TEXTO_PRINCIPAL]),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=15,
        height=60,  # Trava a altura do logo para manter a proporção da gaveta e alinhar corretamente
    )