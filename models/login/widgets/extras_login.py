import flet as ft


def criar_opcoes_extras(cor_texto_secundario: str, cor_primaria: str) -> ft.Row:
    """Linha auxiliar com o checkbox 'Lembrar-me' e o link de recuperação de senha.

    Args:
        cor_texto_secundario: cor do texto do checkbox.
        cor_primaria: cor de destaque usada no checkbox e no link.
    """
    return ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        controls=[
            ft.Checkbox(
                label="Lembrar-me",
                label_style=ft.TextStyle(color=cor_texto_secundario, size=14),
                fill_color=cor_primaria,
            ),
            ft.TextButton("Esqueceu a senha?", style=ft.ButtonStyle(color=cor_primaria)),
        ],
    )