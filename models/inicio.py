import flet as ft
from datetime import datetime

def ViewInicio(page: ft.Page, mudar_tela):
    
    # Saudação baseada na hora do dia
    hora_atual = datetime.now().hour
    if hora_atual < 12:
        saudacao = "Bom dia"
    elif hora_atual < 18:
        saudacao = "Boa tarde"
    else:
        saudacao = "Boa noite"

    # === 1. COMPONENTE: ATALHOS RÁPIDOS ===
    def criar_card_atalho(titulo, descricao, icone, cor, rota):
        return ft.Container(
            width=280, 
            bgcolor="white",
            padding=25,
            border_radius=10,
            # Retornamos para a sombra que é 100% compatível com sua versão
            shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color="black12"), 
            content=ft.Column(
                spacing=15,
                controls=[
                    ft.Container(
                        padding=15,
                        bgcolor=f"{cor}50",
                        border_radius=8,
                        content=ft.Icon(icone, color=cor, size=32)
                    ),
                    ft.Text(titulo, size=18, weight="bold", color="black87"),
                    ft.Text(descricao, size=14, color="grey600"),
                    ft.Container(height=10), # Espaçador
                    ft.ElevatedButton(
                        "Acessar",
                        icon=ft.Icons.ARROW_FORWARD,
                        bgcolor=cor,
                        color="white",
                        on_click=lambda _: mudar_tela(rota)
                    )
                ]
            )
        )

    linha_atalhos = ft.Row(
        spacing=20,
        wrap=True, # Garante que os cards não sejam esmagados em telas menores
        run_spacing=20,
        controls=[
            criar_card_atalho("Dashboard", "Visão geral e gráficos de desempenho.", ft.Icons.PIE_CHART, "blue700", "/dashboard"),
            criar_card_atalho("Avaliações", "Gerencie os ciclos de coleta ativos.", ft.Icons.ASSIGNMENT, "green700", "/avaliacoes"),
            criar_card_atalho("Configurações", "Ajuste os indicadores e o sistema.", ft.Icons.SETTINGS, "orange700", "/configuracoes")
        ]
    )

    # === 2. COMPONENTE: STATUS DO SISTEMA ===
    card_status = ft.Container(
        width=400,
        bgcolor="white",
        padding=25,
        border_radius=10,
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color="black12"),
        content=ft.Column(
            spacing=15,
            controls=[
                ft.Text("Status do Sistema", size=18, weight="bold", color="black87"),
                ft.Divider(color="grey200", height=5),
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Row([ft.Icon(ft.Icons.CLOUD_DONE, color="green700", size=20), ft.Text("Banco de Dados", size=14)]),
                        ft.Text("Conectado", color="green700", weight="bold", size=14)
                    ]
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Row([ft.Icon(ft.Icons.SYNC, color="blue700", size=20), ft.Text("Ciclo Atual", size=14)]),
                        ft.Text("2026.1 (Ativo)", color="blue700", weight="bold", size=14)
                    ]
                )
            ]
        )
    )

    # === 3. SIDEBAR PADRÃO ===
    estilo_botao_menu = ft.ButtonStyle(
        color={"":"white70", "hovered":"white"},
        bgcolor={"":"transparent", "hovered":"white10"},
        shape=ft.RoundedRectangleBorder(radius=8),
        padding=15,
        alignment=ft.Alignment(-1, 0) 
    )
    
    def sair(e):
        mudar_tela("/")

    sidebar = ft.Container(
        width=260,
        bgcolor="blue900",
        padding=20,
        content=ft.Column(
            expand=True,
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.ANALYTICS, color="white", size=32),
                        ft.Text("Evalytics", size=24, weight="bold", color="white"),
                    ],
                    alignment=ft.MainAxisAlignment.START
                ),
                ft.Divider(color="white24", height=30),
                ft.TextButton("Dashboard", icon=ft.Icons.DASHBOARD, on_click=lambda _: mudar_tela("/dashboard"), style=estilo_botao_menu),
                ft.TextButton("Avaliações", icon=ft.Icons.ASSIGNMENT, on_click=lambda _: mudar_tela("/avaliacoes"), style=estilo_botao_menu),
                ft.TextButton("Relatórios", icon=ft.Icons.PIE_CHART, on_click=lambda _: mudar_tela("/relatorios"), style=estilo_botao_menu),
                ft.TextButton("Cursos", icon=ft.Icons.BOOK, on_click=lambda _: mudar_tela("/cursos"), style=estilo_botao_menu),
                ft.TextButton("Configurações", icon=ft.Icons.SETTINGS, on_click=lambda _: mudar_tela("/configuracoes"), style=estilo_botao_menu),
                
                ft.Container(expand=True), 
                ft.TextButton("Sair do Sistema", icon=ft.Icons.LOGOUT, style=estilo_botao_menu, on_click=sair)
            ]
        )
    )

    # Lógica de Responsividade (Padrão)
    def alternar_sidebar(e=None):
        sidebar.visible = not sidebar.visible
        page.update()

    btn_menu = ft.IconButton(icon=ft.Icons.MENU, icon_size=30, icon_color="black87", on_click=alternar_sidebar, visible=False)

    def verificar_tamanho_tela(e=None):
        try:
            _ = sidebar.page
        except Exception:
            return 
        
        if page.width < 900:
            sidebar.visible = False
            btn_menu.visible = True
        else:
            sidebar.visible = True
            btn_menu.visible = False
            
        try:
            page.update()
        except Exception:
            pass

    page.on_resize = verificar_tamanho_tela

    # === 4. ÁREA DE CONTEÚDO PRINCIPAL ===
    area_conteudo = ft.Container(
        expand=True,
        padding=40,
        bgcolor="#F4F6F9",
        content=ft.Column(
            expand=True,
            spacing=30,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Row(
                    spacing=10,
                    controls=[
                        btn_menu,
                        ft.Column(
                            spacing=5,
                            controls=[
                                ft.Text(f"{saudacao}, Administrador!", size=32, weight="bold", color="black87"),
                                ft.Text("Selecione uma ação abaixo para começar a gerenciar o Evalytics.", size=16, color="black54"),
                            ]
                        )
                    ]
                ),
                ft.Divider(color="transparent", height=10),
                # Agora os elementos estão na raiz da Coluna, organizados corretamente
                linha_atalhos,
                card_status
            ]
        )
    )

    if page.width:
        if page.width < 900:
            sidebar.visible = False
            btn_menu.visible = True
        else:
            sidebar.visible = True
            btn_menu.visible = False

    return ft.View(
        route="/inicio",
        padding=0,
        bgcolor="white",
        controls=[ft.Row(expand=True, spacing=0, controls=[sidebar, area_conteudo])]
    )