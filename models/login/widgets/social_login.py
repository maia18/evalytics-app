import flet as ft

from components.core.constants.constants import COR_TEXTO_TITULO


def criar_login_social(cor_texto_secundario: str, cor_borda: str) -> ft.Column:
    """Seção de autenticação por terceiros: divisor 'OU CONTINUE COM' + botões sociais.

    Args:
        cor_texto_secundario: cor do texto do divisor.
        cor_borda: cor das linhas do divisor e do contorno dos botões sociais.
    """
    divisor = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            ft.Container(height=1, bgcolor=cor_borda, expand=True),
            ft.Text("OU CONTINUE COM", size=12, color=cor_texto_secundario, weight=ft.FontWeight.W_500),
            ft.Container(height=1, bgcolor=cor_borda, expand=True),
        ],
    )

    estilo_botao_social = ft.ButtonStyle(
        shape=ft.RoundedRectangleBorder(radius=4),
        side=ft.BorderSide(1, cor_borda),
        padding=ft.Padding.symmetric(vertical=15),
    )

    botoes = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        spacing=10,  # Substitui os Containers manuais de espaçamento, mesmo resultado visual
        controls=[
            ft.OutlinedButton(
                content=ft.Text("G", color=COR_TEXTO_TITULO, weight=ft.FontWeight.BOLD),
                style=estilo_botao_social, expand=True,
            ),
            ft.OutlinedButton(
                content=ft.Icon(ft.Icons.WINDOW, color=COR_TEXTO_TITULO),
                style=estilo_botao_social, expand=True,
            ),
            ft.OutlinedButton(
                content=ft.Icon(ft.Icons.APPLE, color=COR_TEXTO_TITULO),
                style=estilo_botao_social, expand=True,
            ),
        ],
    )

    return ft.Column(
        spacing=20,
        controls=[ft.Container(height=10), divisor, botoes],
    )