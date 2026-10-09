import flet as ft
from components.core.auth.auth_state import auth_state

def criar_botao_logout(
    page: ft.Page,
    dark_mode: bool,
    cor_texto: str,
    mudar_tela,
    compact: bool = False,
) -> ft.Control:
    """Botão de saída da aplicação. Renderiza adaptando-se ao estado do menu."""

    '''
    Handler ASSÍNCRONO: O `encerrar_sessao` no auth_state manipula o SharedPreferences (I/O local), por isso exige async/await no callback de clique.
    '''
    async def fazer_logout(e):
        await auth_state.encerrar_sessao(page)
        mudar_tela("/login")

    # Condicional de renderização da interface baseada na prop 'compact'
    if compact:
        conteudo = ft.Icon(
            ft.Icons.LOGOUT,
            color=cor_texto,
        )
    else:
        conteudo = ft.Row(
            controls=[
                ft.Icon(ft.Icons.LOGOUT, color=cor_texto),
                ft.Text("Sair", color=cor_texto),
            ],
            spacing=10,
        )

    # Encapsula o TextButton para ter controle preciso de Padding e Alinhamento
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