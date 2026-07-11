import flet as ft

def ViewDashboard(page: ft.Page, mudar_tela):
    
    # === 1. COMPONENTE: CARDS DE KPI ===
    def criar_kpi_card(titulo, valor, icone, cor_icone, subtitulo):
        return ft.Container(
            width=260, # SOLUÇÃO: Largura fixa em vez de expand=True impede o esmagamento
            bgcolor="white",
            padding=20, 
            border_radius=10,
            shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color="black12"),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Column(
                        spacing=5,
                        controls=[
                            ft.Text(titulo, size=14, color="grey600", weight="bold"),
                            ft.Text(valor, size=28, weight="bold", color="black87"),
                            ft.Text(subtitulo, size=12, color="green600" if "↑" in subtitulo else "grey500")
                        ]
                    ),
                    ft.Container(
                        padding=15,
                        bgcolor=f"{cor_icone}50",
                        border_radius=50,
                        content=ft.Icon(icone, color=cor_icone, size=28)
                    )
                ]
            )
        )

    linha_kpis = ft.Row(
        wrap=True, # SOLUÇÃO: Quando faltar espaço, joga o card de forma elegante para a linha de baixo
        spacing=20,
        run_spacing=20,
        controls=[
            criar_kpi_card("Total de Respostas", "342", ft.Icons.PEOPLE, "blue700", "↑ 12% este mês"),
            criar_kpi_card("Média Institucional", "4.2", ft.Icons.STAR, "amber600", "Meta: 4.0"),
            criar_kpi_card("Melhor Desempenho", "Eixo 1", ft.Icons.TRENDING_UP, "green700", "Didático-Pedagógica"),
            criar_kpi_card("Atenção Necessária", "Eixo 3", ft.Icons.WARNING, "red700", "Infraestrutura (Nota 3.4)")
        ]
    )

    # === 2. COMPONENTE: DESEMPENHO (BARRAS HORIZONTAIS) ===
    def criar_barra_progresso(rotulo, nota, cor):
        return ft.Column(
            spacing=5,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text(rotulo, size=14, weight="bold", color="black87"),
                        ft.Text(f"{nota} / 5.0", size=14, color="grey700", weight="bold")
                    ]
                ),
                ft.ProgressBar(value=nota/5.0, color=cor, bgcolor="grey200", height=10)
            ]
        )

    card_grafico_barras = ft.Container(
        width=600, # SOLUÇÃO: Largura base estabelecida
        bgcolor="white",
        padding=25,
        border_radius=10,
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color="black12"),
        content=ft.Column(
            spacing=20,
            controls=[
                ft.Text("Desempenho Médio por Eixo", size=18, weight="bold", color="black87"),
                ft.Divider(color="transparent", height=5),
                criar_barra_progresso("Organização Didático-Pedagógica", 4.5, "blue700"),
                criar_barra_progresso("Corpo Docente e Tutorial", 4.1, "blue500"),
                criar_barra_progresso("Infraestrutura", 3.4, "orange700"),
            ]
        )
    )

    # === 3. COMPONENTE: DEMOGRAFIA (LISTA DE PROGRESSO) ===
    def criar_demografia(curso, porcentagem, cor):
        return ft.Column(
            spacing=5,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Row([ft.Icon(ft.Icons.CIRCLE, color=cor, size=12), ft.Text(curso, size=14)]),
                        ft.Text(f"{int(porcentagem*100)}%", size=14, weight="bold")
                    ]
                ),
                ft.ProgressBar(value=porcentagem, color=cor, bgcolor="grey200", height=6)
            ]
        )

    card_grafico_pizza = ft.Container(
        width=300, # SOLUÇÃO: Largura base estabelecida
        bgcolor="white",
        padding=25,
        border_radius=10,
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color="black12"),
        content=ft.Column(
            spacing=20,
            controls=[
                ft.Text("Participação por Área", size=18, weight="bold", color="black87"),
                ft.Divider(color="transparent", height=5),
                criar_demografia("Engenharias", 0.61, "blue700"),
                criar_demografia("Tecnologia", 0.25, "blue400"),
                criar_demografia("Administração", 0.14, "cyan300"),
            ]
        )
    )

    linha_graficos = ft.Row(
        wrap=True, # SOLUÇÃO: Quebra a linha do gráfico de pizza se a tela apertar
        spacing=20,
        run_spacing=20,
        controls=[card_grafico_barras, card_grafico_pizza]
    )

    # === 4. SIDEBAR E RESPONSIVIDADE ===
    estilo_botao_menu = ft.ButtonStyle(
        color={"":"white70", "hovered":"white"},
        bgcolor={"":"transparent", "hovered":"white10"},
        shape=ft.RoundedRectangleBorder(radius=8),
        padding=15,
        alignment=ft.Alignment(-1, 0) 
    )

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
                ft.TextButton("Visão Geral", icon=ft.Icons.DASHBOARD, on_click=lambda _: mudar_tela("/dashboard"), style=estilo_botao_menu),
                ft.TextButton("Avaliações", icon=ft.Icons.ASSIGNMENT, on_click=lambda _: mudar_tela("/avaliacoes"), style=estilo_botao_menu),
                ft.TextButton("Relatórios", icon=ft.Icons.PIE_CHART, on_click=lambda _: mudar_tela("/relatorios"), style=estilo_botao_menu),
                ft.TextButton("Cursos", icon=ft.Icons.BOOK, on_click=lambda _: mudar_tela("/cursos"), style=estilo_botao_menu),
                ft.TextButton("Configurações", icon=ft.Icons.SETTINGS, on_click=lambda _: mudar_tela("/configuracoes"), style=estilo_botao_menu),
            ]
        )
    )

    def alternar_sidebar(e=None):
        sidebar.visible = not sidebar.visible
        page.update()

    btn_menu = ft.IconButton(
        icon=ft.Icons.MENU,
        icon_size=30,
        icon_color="black87",
        on_click=alternar_sidebar,
        visible=False
    )

    # SOLUÇÃO: Controle matemático que atua junto com o Wrap
    def verificar_tamanho_tela(e=None):
        try:
            # Tenta acessar a página. Se o componente ainda não estiver na tela,
            # ele cai no except silenciosamente sem quebrar o sistema.
            _ = sidebar.page
        except Exception:
            return 
        
        largura = page.width 
        
        # 1. Esconde/Mostra a Sidebar
        if largura < 900:
            sidebar.visible = False
            btn_menu.visible = True
        else:
            sidebar.visible = True
            btn_menu.visible = False
            
        # 2. Impede que o gráfico grande vaze da tela em resoluções minúsculas
        largura_util = largura - 80 # Desconta os 40px de padding da área principal
        if sidebar.visible:
            largura_util -= 260 # Desconta o espaço da sidebar se ela estiver aberta
            
        if largura_util < 600:
            card_grafico_barras.width = largura_util
        else:
            card_grafico_barras.width = 600
            
        try:
            page.update()
        except Exception:
            pass

    page.on_resize = verificar_tamanho_tela

    # === 5. ÁREA DE CONTEÚDO PRINCIPAL ===
    area_conteudo = ft.Container(
        expand=True,
        padding=40,
        bgcolor="#F4F6F9",
        content=ft.Column(
            expand=True,
            spacing=25,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Row(
                    spacing=10,
                    controls=[
                        btn_menu,
                        ft.Column(
                            spacing=5,
                            controls=[
                                ft.Text("Visão Geral do Sistema", size=28, weight="bold", color="black87"),
                                ft.Text("Acompanhe o engajamento e os resultados.", size=16, color="black54"),
                            ]
                        )
                    ]
                ),
                ft.Divider(color="transparent", height=5),
                linha_kpis,
                linha_graficos
            ]
        )
    )

    # Força a checagem matemática ao carregar a tela pela primeira vez
    if page.width:
        if page.width < 900:
            sidebar.visible = False
            btn_menu.visible = True
        else:
            sidebar.visible = True
            btn_menu.visible = False
            
        largura_util = page.width - 80
        if sidebar.visible:
            largura_util -= 260
            
        if largura_util < 600:
            card_grafico_barras.width = largura_util
        else:
            card_grafico_barras.width = 600

    return ft.View(
        route="/dashboard",
        padding=0,
        bgcolor="white",
        controls=[ft.Row(expand=True, spacing=0, controls=[sidebar, area_conteudo])]
    )