import flet as ft

def ViewLogin(page: ft.Page, mudar_tela):
    email_input = ft.TextField(label="E-mail", width=300, prefix_icon=ft.Icons.EMAIL)
    senha_input = ft.TextField(label="Senha", width=300, password=True, can_reveal_password=True, prefix_icon=ft.Icons.LOCK)
    
    btn_login = ft.ElevatedButton(
        "Entrar", 
        width=300, 
        style=ft.ButtonStyle(bgcolor="blue700", color="white", padding=15),
        # Usa a função que será repassada pelo main.py
        on_click=lambda _: mudar_tela("/dashboard")
    )

    cartao_login = ft.Card(
        elevation=5,
        width=450,
        content=ft.Container(
            padding=40,
            content=ft.Column(
                controls=[
                    ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=80, color="blue700"),
                    ft.Text("Acesso ao Sistema", size=24, weight=ft.FontWeight.BOLD),
                    ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                    email_input,
                    senha_input,
                    ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                    btn_login
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )
    )

    # Retorna a View (a tela inteira) montada
    return ft.View(
        route="/",
        appbar=ft.AppBar(title=ft.Text("Evalytics", color="white"), bgcolor="blue700", center_title=True),
        controls=[cartao_login],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )