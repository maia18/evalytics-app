import flet as ft


def criar_card_login(
    cabecalho_abas: ft.Row,
    campo_nome: ft.Column,
    campo_email: ft.Column,
    campo_senha: ft.Column,
    opcoes_extras: ft.Row,
    btn_login: ft.ElevatedButton,
    secao_social: ft.Column,
    cor_card: str,
) -> ft.Container:
    """Painel central (Card) que agrupa todos os elementos do formulário de autenticação.

    Args:
        cabecalho_abas: seletor de abas (Sign In / Sign Up).
        campo_nome, campo_email, campo_senha: inputs de texto do usuário.
        opcoes_extras: elementos auxiliares (Lembrar de mim, Esqueci a senha).
        btn_login: botão principal de submissão do formulário.
        secao_social: área com botões de login via redes sociais/terceiros.
        cor_card: cor de fundo do cartão, adaptável ao tema claro/escuro.
    """
    return ft.Container(
        width=420,
        bgcolor=cor_card,
        padding=40,
        border_radius=12,
        shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.BLACK12),
        content=ft.Column(
            spacing=20,
            controls=[cabecalho_abas, campo_nome, campo_email, campo_senha, opcoes_extras, btn_login, secao_social],
        ),
    )