import flet as ft

def criar_opcoes_extras(
    cor_texto_secundario: str,
    cor_primaria: str,
) -> tuple[ft.Row, ft.Checkbox]:
    """
    Cria a linha de opções extras do formulário de login.
        Padrão de Retorno (Tupla):
            Retorna a `Row` (para ser desenhada na tela) E a instância do `Checkbox` (para que a função `ViewLogin` pai consiga ler `checkbox_lembrar.value` na hora de autenticar).
    """

    # 1. Instancia o Checkbox guardando sua referência
    checkbox_lembrar = ft.Checkbox(
        label="Lembrar-me",
        label_style=ft.TextStyle(
            color=cor_texto_secundario,
            size=14,
        ),
        fill_color=cor_primaria, # A cor de preenchimento quando marcado
    )

    # 2. Agrupa o Checkbox e o Link em uma linha
    opcoes = ft.Row(
        # SPACE_BETWEEN é essencial aqui: empurra o Checkbox para a extrema esquerda e o botão "Esqueceu a senha?" para a extrema direita.
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        controls=[
            checkbox_lembrar,
            
            # Botão de texto simples sem fundo, ideal para links
            ft.TextButton(
                "Esqueceu a senha?",
                style=ft.ButtonStyle(
                    color=cor_primaria,
                ),
            ),
        ],
    )

    return opcoes, checkbox_lembrar # Devolve a interface (opcoes) e a referência de estado (checkbox)