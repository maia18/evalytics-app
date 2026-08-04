import flet as ft

def criar_opcoes_extras(cor_texto_secundario: str, cor_primaria: str) -> ft.Row:
    """Linha auxiliar com o checkbox 'Lembrar-me' e o link de recuperação de senha."""
    return ft.Row(
        # SPACE_BETWEEN empurra o checkbox para a esquerda e o botão para a direita, preenchendo a linha.
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        controls=[
            # Checkbox nativo do Flet com estilização customizada de cores
            ft.Checkbox(
                label="Lembrar-me",
                label_style=ft.TextStyle(color=cor_texto_secundario, size=14),
                fill_color=cor_primaria,
            ),
            # Botão de texto simples sem fundo para simular um hiperlink
            ft.TextButton("Esqueceu a senha?", style=ft.ButtonStyle(color=cor_primaria)),
        ],
    )