import flet as ft

def criar_tela_sucesso(mudar_tela):
    return ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20,
        controls=[
            ft.Container(height=50),
            ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE, color="green700", size=80),
            ft.Text("Avaliação Enviada!", size=28, weight="bold", color="black87"),
            ft.Text(
                "Muito obrigado pelo seu tempo e contribuição.\nSuas respostas foram registradas com sucesso.",
                text_align=ft.TextAlign.CENTER,
                color="grey600"
            ),
            ft.Container(height=20),
            ft.ElevatedButton("Voltar para o Painel", on_click=lambda _: mudar_tela("/inicio"))
        ]
    )
