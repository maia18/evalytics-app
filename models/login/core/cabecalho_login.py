import flet as ft


def criar_cabecalho(cor_texto_titulo: str, cor_texto_secundario: str) -> ft.Column:
    """Cria o cabeçalho da tela de login: logotipo e mensagens de boas-vindas.

    Args:
        cor_texto_titulo: cor principal usada para o título de destaque.
        cor_texto_secundario: cor mais suave (geralmente cinza) usada para o subtítulo.
    """
    return ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10,
        controls=[
            ft.Container(
                content=ft.Image(src="imgs/logo.png", width=60, height=60, fit="CONTAIN")
            ),
            ft.Text("Bem-vindo ao Evalytics", size=28, weight="bold", color=cor_texto_titulo),
            ft.Text(
                "Faça login para gerenciar as avaliações institucionais.",
                size=16,
                color=cor_texto_secundario,
                text_align=ft.TextAlign.CENTER,
            ),
        ],
    )