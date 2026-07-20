import flet as ft

def criar_campo_nome(COR_TEXTO_TITULO, COR_TEXTO_SECUNDARIO, COR_BORDA):
    return ft.Column(
        spacing=5,
        visible=False, # Inicia oculto no modo "Sign In"
        controls=[
            ft.Text("Nome", size=14, weight="w500", color=COR_TEXTO_TITULO),
            ft.TextField(
                hint_text="John Doe",
                hint_style=ft.TextStyle(color=COR_TEXTO_SECUNDARIO),
                border_color=COR_BORDA,
                border_radius=8,
                content_padding=15,
                cursor_color=COR_TEXTO_TITULO,
                text_style=ft.TextStyle(color=COR_TEXTO_TITULO)
            )
        ]
    )

def criar_campo_email(COR_TEXTO_TITULO, COR_TEXTO_SECUNDARIO, COR_BORDA):
    return ft.Column(
        spacing=5,
        controls=[
            ft.Text("Email", size=14, weight="w500", color=COR_TEXTO_TITULO),
            ft.TextField(
                hint_text="voce@instituicao.com",
                hint_style=ft.TextStyle(color=COR_TEXTO_SECUNDARIO),
                border_color=COR_BORDA,
                border_radius=8,
                content_padding=15,
                cursor_color=COR_TEXTO_TITULO,
                text_style=ft.TextStyle(color=COR_TEXTO_TITULO)
            )
        ]
    )

def criar_campo_senha(COR_TEXTO_TITULO, COR_TEXTO_SECUNDARIO, COR_BORDA):
    return ft.Column(
        spacing=5,
        controls=[
            ft.Text("Senha", size=14, weight="w500", color=COR_TEXTO_TITULO),
            ft.TextField(
                hint_text="Digite sua senha",
                hint_style=ft.TextStyle(color=COR_TEXTO_SECUNDARIO),
                password=True,
                can_reveal_password=True,
                border_color=COR_BORDA,
                border_radius=8,
                content_padding=15,
                cursor_color=COR_TEXTO_TITULO,
                text_style=ft.TextStyle(color=COR_TEXTO_TITULO)
            )
        ]
    )
