import flet as ft

def criar_tabela_resultados(page, layout, borda_container):
    return ft.Container(
        expand=True,
        bgcolor=layout.cores["CARD"],
        padding=25,
        border=borda_container,
        border_radius=10,
        content=ft.Column(
            controls=[
                ft.Text("Resultados Consolidados", size=18, weight="bold", color=layout.cores["TEXTO_PRINCIPAL"]),
                ft.DataTable(
                    heading_row_color=ft.Colors.BLUE_GREY_900 if page.theme_mode == ft.ThemeMode.DARK else "blue50",
                    columns=[
                        ft.DataColumn(ft.Text("Semestre", weight="bold", color=ft.Colors.ON_SURFACE)),
                        ft.DataColumn(ft.Text("Infraestrutura", weight="bold", color=ft.Colors.ON_SURFACE)),
                        ft.DataColumn(ft.Text("Didática", weight="bold", color=ft.Colors.ON_SURFACE)),
                        ft.DataColumn(ft.Text("Atendimento", weight="bold", color=ft.Colors.ON_SURFACE)),
                        ft.DataColumn(ft.Text("Material", weight="bold", color=ft.Colors.ON_SURFACE)),
                        ft.DataColumn(ft.Text("Inovação", weight="bold", color=ft.Colors.ON_SURFACE)),
                    ],
                    rows=[
                        ft.DataRow(cells=[
                            ft.DataCell(ft.Text("2025.2", color=ft.Colors.ON_SURFACE)),
                            ft.DataCell(ft.Text("4.8", color=ft.Colors.ON_SURFACE)),
                            ft.DataCell(ft.Text("4.5", color=ft.Colors.ON_SURFACE)),
                            ft.DataCell(ft.Text("4.0", color=ft.Colors.ON_SURFACE)),
                            ft.DataCell(ft.Text("4.2", color=ft.Colors.ON_SURFACE)),
                            ft.DataCell(ft.Text("4.7", color=ft.Colors.ON_SURFACE)),
                        ]),
                        ft.DataRow(cells=[
                            ft.DataCell(ft.Text("2026.1", color=ft.Colors.ON_SURFACE)),
                            ft.DataCell(ft.Text("Aguardando", color=ft.Colors.ON_SURFACE)),
                            ft.DataCell(ft.Text("-", color=ft.Colors.ON_SURFACE)),
                            ft.DataCell(ft.Text("-", color=ft.Colors.ON_SURFACE)),
                            ft.DataCell(ft.Text("-", color=ft.Colors.ON_SURFACE)),
                            ft.DataCell(ft.Text("", color=ft.Colors.ON_SURFACE)),
                        ]),
                    ],
                )
            ]
        )
    )
