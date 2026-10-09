import flet as ft
from components.core.auth.auth_state import auth_state

def criar_botao_logout(
    page: ft.Page,
    dark_mode: bool,
    cor_texto: str,
    mudar_tela,
    compact: bool = False,
) -> ft.Control:

    async def fazer_logout(e):
        # Encerra a sessão atual e remove o refresh token persistido
        await auth_state.encerrar_sessao(page)

        # Redireciona para o login
        mudar_tela("/login")

    if compact:
        # Sidebar compacta: somente o ícone
        conteudo = ft.Icon(
            ft.Icons.LOGOUT,
            color=cor_texto,
        )
    else:
        # Sidebar expandida: ícone + texto
        conteudo = ft.Row(
            controls=[
                ft.Icon(
                    ft.Icons.LOGOUT,
                    color=cor_texto,
                ),
                ft.Text(
                    "Sair",
                    color=cor_texto,
                ),
            ],
            spacing=10,
        )

    return ft.Container(
        content=ft.TextButton(
            content=conteudo,
            on_click=fazer_logout,
        ),
        padding=ft.Padding.symmetric(
            horizontal=10,
            vertical=8,
        ),
        alignment=ft.Alignment.CENTER,
    )
    