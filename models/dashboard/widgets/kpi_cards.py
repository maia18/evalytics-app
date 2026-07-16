import flet as ft

def criar_kpi_card(layout, titulo, valor, icone, cor_icone):
    borda_card = ft.Border(
        top=ft.BorderSide(1, layout.cores["BORDA"]),
        bottom=ft.BorderSide(1, layout.cores["BORDA"]),
        left=ft.BorderSide(1, layout.cores["BORDA"]),
        right=ft.BorderSide(1, layout.cores["BORDA"])
    )
    
    return ft.Container(
        width=240,
        bgcolor=layout.cores["CARD"],
        padding=20, 
        border_radius=8,
        border=borda_card,
        content=ft.Column(
            spacing=15,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text(titulo, size=14, color="grey600", weight="w500"),
                        ft.Icon(icone, color=cor_icone, size=18)
                    ]
                ),
                ft.Text(valor, size=28, weight="bold", color=layout.cores["TEXTO_PRINCIPAL"]),
            ]
        )
    )
