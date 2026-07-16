import flet as ft

def criar_opcoes_extras(COR_TEXTO_SECUNDARIO, COR_PRIMARIA):
    return ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        controls=[
            ft.Checkbox(
                label="Lembrar-me",
                label_style=ft.TextStyle(color=COR_TEXTO_SECUNDARIO, size=14),
                fill_color=COR_PRIMARIA
            ),
            ft.TextButton("Esqueceu a senha?", style=ft.ButtonStyle(color=COR_PRIMARIA))
        ]
    )
