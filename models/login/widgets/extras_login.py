import flet as ft

def criar_opcoes_extras(
    cor_texto_secundario: str,
    cor_primaria: str,
) -> tuple[ft.Row, ft.Checkbox]:

    checkbox_lembrar = ft.Checkbox(
        label="Lembrar-me",
        label_style=ft.TextStyle(
            color=cor_texto_secundario,
            size=14,
        ),
        fill_color=cor_primaria,
    )

    opcoes = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        controls=[
            checkbox_lembrar,
            ft.TextButton(
                "Esqueceu a senha?",
                style=ft.ButtonStyle(
                    color=cor_primaria,
                ),
            ),
        ],
    )

    return opcoes, checkbox_lembrar