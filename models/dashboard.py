""" Importações """  
import flet as ft

def ViewDashboard(page: ft.Page, mudar_tela):
    
    """
    Tela de Dashboard do sistema Evalytics.
    Mostra KPIs, gráficos de desempenho e participação, com sidebar responsiva.
    """
    
    # === 1. COMPONENTE: CARDS DE KPI ===
    def criar_kpi_card(titulo, valor, icone, cor_icone, subtitulo):
        """
        Cria um card de KPI com título, valor, subtítulo e ícone.
        """
        return ft.Container(
            width=260,
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

    # Linha de KPIs com wrap para responsividade
    linha_kpis = ft.Row(
        wrap=True,
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
        """
        Cria uma barra de progresso horizontal representando a nota média de um eixo.
        """
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
        width=600,
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
        """
        Cria uma linha de demografia com porcentagem de participação por área.
        """
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
        width=300,
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
        wrap=True,
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
    
    def sair(e):
        mudar_tela("/")  # Redireciona para tela inicial

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
                ft.TextButton("Visão Geral", icon=ft.Icons.DASHBOARD, on_click=lambda _: mudar_tela("/inicio"), style=estilo_botao_menu),
                ft.TextButton("Avaliações", icon=ft.Icons.ASSIGNMENT, on_click=lambda _: mudar_tela("/avaliacoes"), style=estilo_botao_menu),
                ft.TextButton("Relatórios", icon=ft.Icons.PIE_CHART, on_click=lambda _: mudar_tela("/relatorios"), style=estilo_botao_menu),
                ft.TextButton("Cursos", icon=ft.Icons.BOOK, on_click=lambda _: mudar_tela("/cursos"), style=estilo_botao_menu),
                ft.TextButton("Configurações", icon=ft.Icons.SETTINGS, on_click=lambda _: mudar_tela("/configuracoes"), style=estilo_botao_menu),
                
                ft.Container(expand=True), 
                ft.TextButton("Sair do Sistema", icon=ft.Icons.LOGOUT, style=estilo_botao_menu, on_click=sair)
            ]
        )
    )

    # Botão de menu para telas pequenas
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

    # Função de responsividade
    def verificar_tamanho_tela(e=None):
        """
        Ajusta visibilidade da sidebar e largura dos gráficos conforme tamanho da tela.
        """
        try:
            """ 
            Tenta acessar a página. Se o componente ainda não estiver na tela,
            # ele cai no except silenciosamente sem quebrar o sistema.
            """
            _ = sidebar.page
        except Exception:
            return 
        
        largura = page.width 
        
        # Sidebar responsiva
        if largura < 900:
            sidebar.visible = False
            btn_menu.visible = True
        else:
            sidebar.visible = True
            btn_menu.visible = False
            
        # Ajuste do gráfico de barras
        largura_util = largura - 80
        if sidebar.visible:
            largura_util -= 260
            
        card_grafico_barras.width = largura_util if largura_util < 600 else 600
            
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
            scroll=ft.ScrollMode.AUTO, # permite rolagem caso o conteúdo ultrapasse a altura
            controls=[
                ft.Row(
                    spacing=10,
                    controls=[
                        btn_menu, # botão de menu aparece em telas pequenas
                        ft.Column(
                            spacing=5,
                            controls=[
                                ft.Text("Dashboard do Sistema", size=28, weight="bold", color="black87"),
                                ft.Text("Acompanhe o engajamento e os resultados.", size=16, color="black54"),
                            ]
                        )
                    ]
                ),
                ft.Divider(color="transparent", height=5),
                linha_kpis, # cards de KPI
                linha_graficos # gráficos de barras e demografia
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
            
        largura_util = page.width - 80 # desconta padding lateral
        if sidebar.visible:
            largura_util -= 260  # desconta largura da sidebar
            
        # Ajusta largura do gráfico de barras conforme espaço disponível
        if largura_util < 600:
            card_grafico_barras.width = largura_util
        else:
            card_grafico_barras.width = 600

    # === RETORNO FINAL DA VIEW ===
    return ft.View(
        route="/dashboard",
        padding=0,
        bgcolor="white",
        controls=[ft.Row(expand=True, spacing=0, controls=[sidebar, area_conteudo])]
    )