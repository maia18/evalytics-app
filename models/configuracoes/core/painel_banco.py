import flet as ft

# Constrói a interface visual para manutenção e gestão de backups do banco (Mockup)
def criar_painel_banco() -> ft.Container:
    return ft.Container(
        padding=20,
        content=ft.Column(
            spacing=20,
            controls=[
                ft.Text("Gerenciamento de Dados", size=18, weight="bold"),
                ft.Divider(color=ft.Colors.GREY_300),
                ft.Text("Ferramentas para manutenção periódica do sistema.", color=ft.Colors.GREY_700),

                ft.Row(
                    controls=[
                        ft.ElevatedButton("Backup Completo", icon=ft.Icons.DOWNLOAD, bgcolor=ft.Colors.GREEN_700, color=ft.Colors.WHITE),
                        ft.ElevatedButton("Otimizar Índices", icon=ft.Icons.SPEED, bgcolor=ft.Colors.BLUE_700, color=ft.Colors.WHITE),
                    ]
                ),

                ft.Text("Zona de Risco", size=16, color=ft.Colors.RED_700, weight="bold"),
                # Container vermelho para destacar funções de alto risco/destrutivas
                ft.Container(
                    padding=15, bgcolor=ft.Colors.RED_50, border_radius=8,
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text("Excluir avaliações com mais de 5 anos.", color=ft.Colors.RED_900),
                            ft.ElevatedButton("Limpar Dados Antigos", icon=ft.Icons.DELETE_FOREVER, bgcolor=ft.Colors.RED_700, color=ft.Colors.WHITE),
                        ],
                    ),
                ),
            ],
        ),
    )