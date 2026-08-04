from typing import Optional

import flet as ft


def _criar_campo_texto(
    label: str,
    hint_text: str,
    cor_titulo: str,
    cor_secundario: str,
    cor_borda: str,
    **kwargs,
) -> ft.Column:
    """Casca compartilhada dos campos de texto do formulário de login/cadastro.

    `**kwargs` repassa particularidades de cada campo (ex.: password=True na senha).
    """
    return ft.Column(
        spacing=5,
        controls=[
            ft.Text(label, size=14, weight="w500", color=cor_titulo),
            ft.TextField(
                hint_text=hint_text,
                hint_style=ft.TextStyle(color=cor_secundario),
                border_color=cor_borda,
                border_radius=8,
                content_padding=15,
                cursor_color=cor_titulo,
                text_style=ft.TextStyle(color=cor_titulo),
                **kwargs,
            ),
        ],
    )


def criar_campo_nome(cor_texto_titulo: str, cor_texto_secundario: str, cor_borda: str) -> ft.Column:
    """Campo de 'Nome', exclusivo da etapa de cadastro (Sign Up). Inicia oculto."""
    campo = _criar_campo_texto("Nome", "John Doe", cor_texto_titulo, cor_texto_secundario, cor_borda)
    campo.visible = False  # A tela abre por padrão em modo "Sign In"
    return campo


def criar_campo_email(cor_texto_titulo: str, cor_texto_secundario: str, cor_borda: str) -> ft.Column:
    """Campo de 'Email', usado tanto no Login quanto no Cadastro."""
    return _criar_campo_texto(
        "Email", "voce@instituicao.com", cor_texto_titulo, cor_texto_secundario, cor_borda
    )


def criar_campo_senha(cor_texto_titulo: str, cor_texto_secundario: str, cor_borda: str) -> ft.Column:
    """Campo de 'Senha', com mascaramento e ícone de exibir/ocultar."""
    return _criar_campo_texto(
        "Senha", "Digite sua senha", cor_texto_titulo, cor_texto_secundario, cor_borda,
        password=True, can_reveal_password=True,
    )