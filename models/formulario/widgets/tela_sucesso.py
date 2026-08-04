from typing import Callable

import flet as ft


def criar_tela_sucesso(mudar_tela: Callable[[str], None]) -> ft.Column:
    """Renderiza a tela final de agradecimento exibida após o formulário ser concluído."""
    return ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20,
        controls=[
            ft.Container(height=50),
            ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE, color=ft.Colors.GREEN, size=80),
            ft.Text("Avaliação Enviada!", size=28, weight="bold", color="onSurface"),
            ft.Text(
                "Muito obrigado pelo seu tempo e contribuição.\nSuas respostas foram registradas com sucesso.",
                text_align=ft.TextAlign.CENTER,
                color="onSurfaceVariant",
            ),
            ft.Container(height=20),
            ft.ElevatedButton("Voltar para o Painel", on_click=lambda _: mudar_tela("/inicio")),
        ],
    )