import flet as ft

def criar_login_social(cor_texto_secundario, cor_borda):
    # Divisor com a linha e o texto centralizado
    divisor = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            ft.Container(height=1, bgcolor=cor_borda, expand=True),
            ft.Text(
                "OU CONTINUE COM", 
                size=12, 
                color=cor_texto_secundario, 
                weight=ft.FontWeight.W_500
            ),
            ft.Container(height=1, bgcolor=cor_borda, expand=True),
        ]
    )

    # Estilo padronizado para os três botões ficarem iguais à referência
    estilo_botao_social = ft.ButtonStyle(
        shape=ft.RoundedRectangleBorder(radius=4), # Bordas levemente arredondadas
        side=ft.BorderSide(1, cor_borda),          # Borda cinza clara
        padding=ft.Padding.symmetric(vertical=15)
    )

    # Botões corrigidos utilizando 'content' no lugar de 'text' e 'icon'
    botoes = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        controls=[
            ft.OutlinedButton(
                content=ft.Text("G", color="#111827", weight=ft.FontWeight.BOLD), 
                style=estilo_botao_social, 
                expand=True
            ),
            ft.Container(width=10), # Espaçamento entre botões
            ft.OutlinedButton(
                content=ft.Icon(ft.Icons.WINDOW, color="#111827"), 
                style=estilo_botao_social, 
                expand=True
            ),
            ft.Container(width=10), # Espaçamento entre botões
            ft.OutlinedButton(
                content=ft.Icon(ft.Icons.APPLE, color="#111827"),
                style=estilo_botao_social, 
                expand=True
            ),
        ]
    )

    return ft.Column(
        spacing=20, 
        controls=[
            ft.Container(height=10), # Espaçamento extra do botão principal
            divisor, 
            botoes
        ]
    )