from typing import Callable

import flet as ft

from models.login.core.tab_style import criar_estilo_aba


def obter_funcao_alternar(
    btn_aba_signin: ft.TextButton,
    btn_aba_signup: ft.TextButton,
    campo_nome: ft.Column,
    opcoes_extras: ft.Row,
    btn_login: ft.ElevatedButton,
    cor_texto_titulo: str,
    cor_primaria: str,
) -> Callable[[ft.ControlEvent], None]:
    """Fábrica de closure que retorna o callback de alternância entre 'Sign In' e 'Sign Up'.

    Args:
        btn_aba_signin, btn_aba_signup: referências das abas de login/cadastro.
        campo_nome: campo de texto para o nome do usuário.
        opcoes_extras: bloco com 'Lembrar de mim' e 'Esqueci a senha'.
        btn_login: botão principal de ação do formulário.
        cor_texto_titulo, cor_primaria: cores do tema usadas nos estilos das abas.
    """

    def alternar_modo(e: ft.ControlEvent) -> None:
        is_signup = e.control.data == "signup"

        btn_aba_signin.style = criar_estilo_aba(not is_signup, cor_primaria, cor_texto_titulo)
        btn_aba_signup.style = criar_estilo_aba(is_signup, cor_primaria, cor_texto_titulo)

        campo_nome.visible = is_signup  # Só faz sentido ao criar uma conta
        opcoes_extras.visible = not is_signup  # Só faz sentido no login

        btn_login.text = "Create account" if is_signup else "Sign In"

        e.page.update()

    return alternar_modo