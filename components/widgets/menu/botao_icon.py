import flet as ft

def criar_botao_icon(icone: str, tooltip_text: str, rota: str, dark_mode: bool, cor_texto: str, mudar_tela) -> ft.Container:
    """Cria um botão apenas com ícone"""
    return ft.Container(
        height=45,
        alignment=ft.Alignment(0, 0),
        content=ft.TextButton(
            expand=True,
            content=ft.Icon(
                icone,
                color=cor_texto,
                size=24,
                tooltip=tooltip_text,
            ),
            style=ft.ButtonStyle(
                padding=10,
                shape=ft.RoundedRectangleBorder(radius=8),
                overlay_color="#3C3C3C" if dark_mode else "#CCCCCC",
            ),
            on_click=lambda _: mudar_tela(rota) if mudar_tela else None,
        ),
    )
