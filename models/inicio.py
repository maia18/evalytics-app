import flet as ft

def ViewInicio(page: ft.Page, mudar_tela):
    dark_mode = False

    COR_FUNDO = "#F9FAFB"
    COR_BORDA = "#E5E7EB"
    COR_PRIMARIA = "#F59E0B"

    def aplicar_tema():
        nonlocal COR_FUNDO, COR_BORDA, COR_PRIMARIA
        if dark_mode:
            COR_FUNDO = "#1E1E1E"
            COR_BORDA = "#3C3C3C"
            COR_PRIMARIA = "#F59E0B"
        else:
            COR_FUNDO = "#F9FAFB"
            COR_BORDA = "#E5E7EB"
            COR_PRIMARIA = "#F59E0B"

    aplicar_tema()

    def toggle_dark_mode(e):
        nonlocal dark_mode
        dark_mode = not dark_mode
        aplicar_tema()
        page.bgcolor = COR_FUNDO
        page.update()

    # === OVERLAY ===
    overlay = ft.Container(
        visible=False,
        expand=True,
        bgcolor="#00000088",
        on_click=lambda e: fechar_sidebar(),
    )

    # === SIDEBAR MOBILE ===
    sidebar_mobile_aberta = False
    sidebar = ft.Container(
        left=-270,
        top=0,
        bottom=0,
        width=250,
        bgcolor="white" if not dark_mode else "#2C2C2C",
        animate_position=ft.Animation(300, ft.AnimationCurve.EASE_OUT),
        border=ft.Border(right=ft.BorderSide(1, COR_BORDA)),
        padding=20,
        shadow=ft.BoxShadow(blur_radius=25, spread_radius=2, color="#33000000"),
        content=ft.Column([
            ft.Row([ft.Icon(ft.Icons.ANALYTICS, color=COR_PRIMARIA), ft.Text("Evalytics", size=20, weight="bold")]),
            ft.Divider(),
            ft.Text("Início", size=14, weight="bold"),
            ft.Text("Nova Avaliação", size=14),
            ft.Text("Dashboard", size=14),
            ft.Text("Professores", size=14),
            ft.Text("Cursos", size=14),
            ft.Text("Relatórios", size=14),
            ft.Text("Configurações", size=14),
        ])
    )

    def abrir_sidebar():
        nonlocal sidebar_mobile_aberta
        sidebar_mobile_aberta = True
        sidebar.left = 0
        overlay.visible = True
        page.update()

    def fechar_sidebar():
        nonlocal sidebar_mobile_aberta
        sidebar_mobile_aberta = False
        sidebar.left = -270
        overlay.visible = False
        page.update()

    def toggle_sidebar(e):
        if page.width >= 900:
            return
        if sidebar_mobile_aberta:
            fechar_sidebar()
        else:
            abrir_sidebar()

    menu_button = ft.IconButton(icon=ft.Icons.MENU, on_click=toggle_sidebar)

    # === TOPBAR ===
    topbar = ft.Container(
        padding=20,
        bgcolor="white" if not dark_mode else "#2C2C2C",
        border=ft.Border(bottom=ft.BorderSide(1, COR_BORDA)),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Row(
                    spacing=10,
                    controls=[
                        menu_button,
                        ft.Column(
                            spacing=0,
                            controls=[
                                ft.Text("Início", size=20, weight="bold", color="white" if dark_mode else "black"),
                                ft.Text("Bem-vindo ao Evalytics", size=12, color="grey"),
                            ],
                        ),
                    ],
                ),
                ft.Row(
                    controls=[
                        ft.Dropdown(width=200, height=40, value="San Francisco HQ",
                                    options=[ft.dropdown.Option("San Francisco HQ")]),
                        ft.IconButton(ft.Icons.DARK_MODE_OUTLINED, on_click=toggle_dark_mode),
                        ft.IconButton(ft.Icons.NOTIFICATIONS_NONE),
                        ft.CircleAvatar(content=ft.Text("AC"), bgcolor=COR_PRIMARIA, radius=18),
                    ]
                ),
            ],
        ),
    )

    # === CONTEÚDO PRINCIPAL ===
    def criar_card(titulo, descricao, icone):
        return ft.Container(
            width=300,
            bgcolor="white" if not dark_mode else "#2C2C2C",
            padding=20,
            border_radius=12,
            border=ft.Border(
                left=ft.BorderSide(width=1, color=COR_BORDA),
                top=ft.BorderSide(width=1, color=COR_BORDA),
                right=ft.BorderSide(width=1, color=COR_BORDA),
                bottom=ft.BorderSide(width=1, color=COR_BORDA),
            ),
            content=ft.Column([
                ft.Icon(icone, color=COR_PRIMARIA, size=30),
                ft.Text(titulo, weight="bold", color="white" if dark_mode else "black"),
                ft.Text(descricao, size=12, color="grey")
            ])
        )

    conteudo = ft.Container(
        padding=20,
        content=ft.Column(
            expand=True,
            controls=[
                ft.Container(
                    bgcolor="white" if not dark_mode else "#2C2C2C",
                    padding=25,
                    border_radius=12,
                    border=ft.Border(
                        left=ft.BorderSide(1, COR_BORDA),
                        top=ft.BorderSide(1, COR_BORDA),
                        right=ft.BorderSide(1, COR_BORDA),
                        bottom=ft.BorderSide(1, COR_BORDA)
                    ),
                    content=ft.Column([
                        ft.Text("Sistema de Avaliação Institucional", weight="bold", size=20,
                                color="white" if dark_mode else "black"),
                        ft.ElevatedButton("Iniciar nova avaliação", bgcolor=COR_PRIMARIA, color="white")
                    ])
                ),
                ft.Container(height=20),
                ft.Row(
                    wrap=True,
                    spacing=20,
                    run_spacing=20,
                    controls=[
                        criar_card("Nova Avaliação", "Criar um novo instrumento.", ft.Icons.ADD),
                        criar_card("Dashboard", "Visão geral dos indicadores.", ft.Icons.GRID_VIEW),
                        criar_card("Professores", "Gerenciar corpo docente.", ft.Icons.SCHOOL),
                        criar_card("Cursos", "Consultar e organizar cursos.", ft.Icons.MENU_BOOK),
                        criar_card("Relatórios", "Gerar relatórios.", ft.Icons.PIE_CHART),
                    ]
                )
            ]
        )
    )

    # === SIDEBAR DESKTOP ===
    sidebar_desktop = ft.Container(
        bgcolor="white" if not dark_mode else "#2C2C2C",
        border=ft.Border(right=ft.BorderSide(1, COR_BORDA)),
        padding=20,
        content=ft.Column([
            ft.Row([
                ft.Icon(ft.Icons.ANALYTICS, color=COR_PRIMARIA), 
                ft.Text("Evalytics", size=20, weight="bold")
            ]),
            ft.Divider(),
            ft.Text("Início", size=14, overflow=ft.TextOverflow.ELLIPSIS, max_lines=1),
            ft.Text("Nova Avaliação", size=14, overflow=ft.TextOverflow.ELLIPSIS, max_lines=1),
            ft.Text("Dashboard", size=14, overflow=ft.TextOverflow.ELLIPSIS, max_lines=1),
            ft.Text("Professores", size=14, overflow=ft.TextOverflow.ELLIPSIS, max_lines=1),
            ft.Text("Cursos", size=14, overflow=ft.TextOverflow.ELLIPSIS, max_lines=1),
            ft.Text("Relatórios", size=14, overflow=ft.TextOverflow.ELLIPSIS, max_lines=1),
            ft.Text("Configurações", size=14, overflow=ft.TextOverflow.ELLIPSIS, max_lines=1),
        ])
    )

    # === RESPONSIVIDADE ===
    def on_resize(e=None):
        # Lógica de visibilidade do menu (Mobile)
        if page.width < 700:
            sidebar_desktop.visible = False
            sidebar_desktop.width = 0
            menu_button.visible = True
        else:
            sidebar_desktop.visible = True
            menu_button.visible = False
            fechar_sidebar() # Garante que a mobile feche ao expandir
            
            # Lógica de largura (Desktop/Tablet)
            if page.width >= 1100:
                sidebar_desktop.width = 250
            else: # Entre 700 e 1100
                sidebar_desktop.width = 72

        page.update()

    page.on_resize = on_resize
    on_resize()

    # === LAYOUT FINAL COM STACK ===
    return ft.View(
        route="/inicio",
        padding=0,
        bgcolor=COR_FUNDO,
        controls=[
            ft.Stack(
                expand=True,
                controls=[
                    ft.Row(
                        expand=True,
                        spacing=0,
                        controls=[
                            sidebar_desktop, # A sidebar já altera seu próprio width via on_resize
                            ft.Container(
                                expand=True,
                                padding=20,
                                content=ft.Column([topbar, conteudo], expand=True, scroll=ft.ScrollMode.AUTO)
                            )
                        ]
                    ),
                    overlay,
                    sidebar # Esta é a sidebar mobile flutuante
                ]
            )
        ]
    )