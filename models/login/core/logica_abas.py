from typing import Callable
import flet as ft

from models.login.core.tab_style import criar_estilo_aba

def obter_funcao_alternar(
    btn_aba_signin: ft.TextButton, btn_aba_signup: ft.TextButton, campo_nome: ft.Column,
    opcoes_extras: ft.Row, btn_login: ft.ElevatedButton, cor_texto_titulo: str, cor_primaria: str,
) -> Callable[[ft.ControlEvent], None]:
    """Fábrica de closure que retorna o callback que alterna visualmente os inputs entre modos 'Sign In' e 'Sign Up'."""

    def alternar_modo(e: ft.ControlEvent) -> None:
        is_signup = e.control.data == "signup"

        btn_aba_signin.style = criar_estilo_aba(not is_signup, cor_primaria, cor_texto_titulo)
        btn_aba_signup.style = criar_estilo_aba(is_signup, cor_primaria, cor_texto_titulo)

        campo_nome.visible = is_signup  # Só faz sentido solicitar o nome ao criar uma conta
        opcoes_extras.visible = not is_signup  # "Esqueci a senha" só faz sentido no login

        btn_login.text = "Create account" if is_signup else "Sign In"

        e.page.update()

    return alternar_modo