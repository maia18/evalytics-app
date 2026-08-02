import flet as ft

def criar_stats_card(titulo: str, valor: str, cor_texto: str) -> ft.Container:
    """Renderiza um bloco que exibe um título cinza com um valor numérico em destaque abaixo."""
    return ft.Container(
        expand=1,  # Faz os três cards dividirem o espaço horizontal da Row igualmente (1/3 cada)
        padding=15,
        border_radius=8,
        bgcolor=ft.Colors.WHITE,
        content=ft.Column(
            spacing=5,
            controls=[
                ft.Text(titulo, size=12, color=ft.Colors.GREY),
                ft.Text(str(valor), size=20, weight="bold", color=cor_texto),
            ],
        ),
    )