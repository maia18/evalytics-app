import flet as ft

from components.core.constants.constants import COR_PRIMARIA, TEXTO_PRINCIPAL


def criar_logo(cores: dict[str, str], compact: bool = False) -> ft.Container:
    """Cria o cabeçalho da marca na parte superior do menu.

    Responde à flag de menu compactado para omitir o texto da marca se necessário.
    """
    if compact:
        return ft.Container(
            content=ft.Icon(ft.Icons.ANALYTICS, color=COR_PRIMARIA, size=28),
            padding=8,
            alignment=ft.Alignment.CENTER,
        )

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
        height=60,  # Trava a altura do logo para manter a proporção da gaveta
    )