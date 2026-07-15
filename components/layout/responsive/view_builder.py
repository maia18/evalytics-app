import flet as ft

def criar_view(route, cores, sidebar_desktop, topbar, conteudo_principal, overlay, sidebar_mobile, ajustar_responsividade, page):
    page.on_resize = ajustar_responsividade
    ajustar_responsividade()

    return ft.View(
        route=route,
        padding=0,
        bgcolor=cores["FUNDO"],
        controls=[
            ft.Stack(
                expand=True,
                controls=[
                    ft.Row(
                        expand=True,
                        spacing=0,
                        controls=[
                            sidebar_desktop,
                            ft.Column(
                                expand=True,
                                spacing=0,
                                controls=[
                                    topbar,
                                    ft.Container(
                                        expand=True,
                                        padding=20,
                                        content=conteudo_principal
                                    )
                                ],
                                scroll=ft.ScrollMode.AUTO
                            )
                        ]
                    ),
                    overlay,
                    sidebar_mobile
                ]
            )
        ]
    )
