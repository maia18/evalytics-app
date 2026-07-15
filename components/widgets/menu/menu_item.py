import flet as ft

def criar_item_menu(icone: str, texto: str, rota: str, dark_mode: bool, cor_texto: str, mudar_tela) -> ft.Container:
    """Cria um item de menu com ícone e texto"""
    return ft.Container(
        height=45,
        content=ft.TextButton(
            content=ft.Row(
                spacing=12,
                controls=[
                    ft.Icon(
                        icone,
                        size=20,
                        color="grey700" if not dark_mode else "grey300",
                    ),
                    ft.Text(
                        texto,
                        size=14,
                        weight="w500",
                        color=cor_texto,
                    ),
                ],
            ),
            style=ft.ButtonStyle(
                padding=10,
                shape=ft.RoundedRectangleBorder(radius=8),
                overlay_color="#3C3C3C" if dark_mode else "#CCCCCC",
            ),
            on_click=lambda _: mudar_tela(rota) if mudar_tela else None,
        ),
    )
