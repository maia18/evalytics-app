import flet as ft

def ViewDashboard(page: ft.Page, mudar_tela):
    
    # === ESTILOS BASE ===
    estilo_botao_menu = ft.ButtonStyle(
        color={"":"white70", "hovered":"white"},
        bgcolor={"":"transparent", "hovered":"white10"},
        shape=ft.RoundedRectangleBorder(radius=8),
        padding=15,
        # O Flet lê -1 como totalmente à esquerda e 0 como centro vertical
        alignment=ft.alignment.Alignment(-1, 0) 
    )

    # === FUNÇÕES DE AÇÃO ===
    def sair(e):
        # Limpa o histórico ou qualquer variável de sessão necessária aqui
        mudar_tela("/")

    # === MENU LATERAL (SIDEBAR) ===
    sidebar = ft.Container(
        width=260,
        bgcolor="blue900", # Mantendo a identidade do login
        padding=20,
        content=ft.Column(
            expand=True,
            controls=[
                # Logo e Título
                ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.ANALYTICS, color="white", size=32),
                        ft.Text("Evalytics", size=24, weight="bold", color="white"),
                    ],
                    alignment=ft.MainAxisAlignment.START
                ),
                ft.Divider(color="white24", height=30),
                
                # Links de Navegação
                ft.TextButton("Visão Geral", icon=ft.Icons.DASHBOARD, style=estilo_botao_menu),
                ft.TextButton("Avaliações", icon=ft.Icons.ASSIGNMENT, style=estilo_botao_menu),
                ft.TextButton("Relatórios", icon=ft.Icons.PIE_CHART, style=estilo_botao_menu),
                ft.TextButton("Alunos e Turmas", icon=ft.Icons.PEOPLE, style=estilo_botao_menu),
                ft.TextButton("Configurações", icon=ft.Icons.SETTINGS, style=estilo_botao_menu),
                
                # Empurra o botão de sair para o final da tela
                ft.Container(expand=True), 
                
                # Botão de Logout
                ft.TextButton(
                    "Sair do Sistema", 
                    icon=ft.Icons.LOGOUT, 
                    style=estilo_botao_menu,
                    on_click=sair
                )
            ]
        )
    )

    # === COMPONENTES DO CONTEÚDO CENTRAL ===
    # Adicionamos 'cor_fundo' aos parâmetros
    def criar_card_kpi(titulo, valor, icone, cor_icone, cor_fundo):
        return ft.Container(
            expand=1,
            bgcolor="white",
            border_radius=12,
            padding=20,
            shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color="black12"),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Column(
                        spacing=5,
                        controls=[
                            ft.Text(titulo, size=14, color="black54", weight="w500"),
                            ft.Text(valor, size=28, color="black87", weight="bold"),
                        ]
                    ),
                    ft.Container(
                        padding=15,
                        bgcolor=cor_fundo, # <-- Usamos a string da cor clara diretamente
                        border_radius=50,
                        content=ft.Icon(icone, color=cor_icone, size=30)
                    )
                ]
            )
        )

    # Topo (Boas-vindas)
    cabecalho = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        controls=[
            ft.Column(
                spacing=0,
                controls=[
                    ft.Text("Olá, Administrador 👋", size=28, weight="bold", color="black87"),
                    ft.Text("Aqui está o panorama atual da instituição.", size=16, color="black54"),
                ]
            ),
            # Avatar do Usuário
            ft.CircleAvatar(
                content=ft.Icon(ft.Icons.PERSON),
                color="white",
                bgcolor="blue700",
                radius=25
            )
        ]
    )

    # Linha de Cards de Resumo (KPIs)
    cards_kpi = ft.Row(
        spacing=20,
        controls=[
            # Passamos a cor forte para o ícone, e o tom '50' (super claro) para o fundo
            criar_card_kpi("Taxa de Resposta", "85%", ft.Icons.TRENDING_UP, "green700", "green50"),
            criar_card_kpi("Média Geral", "4.2/5", ft.Icons.STAR, "amber700", "amber50"),
            criar_card_kpi("Avaliações Pendentes", "12", ft.Icons.PENDING_ACTIONS, "red700", "red50"),
            criar_card_kpi("Departamentos", "8", ft.Icons.ACCOUNT_BALANCE, "blue700", "blue50"),
        ]
    )

    # Área reservada para o Gráfico de Radar
    area_grafico = ft.Container(
        expand=True,
        bgcolor="white",
        border_radius=12,
        padding=30,
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color="black12"),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Icon(ft.Icons.RADAR, size=80, color="blue200"),
                ft.Text("Área reservada para o Gráfico de Radar", size=18, color="black54"),
                ft.Text("Mapeamento de Competências e Indicadores", size=14, color="black38"),
            ]
        )
    )

    # === MONTAGEM DO CONTEÚDO CENTRAL ===
    conteudo_central = ft.Container(
        expand=True,
        bgcolor="#F4F6F9", # Um cinza bem claro para contrastar com os cards brancos
        padding=30,
        content=ft.Column(
            spacing=30,
            controls=[
                cabecalho,
                cards_kpi,
                area_grafico
            ]
        )
    )

    # === RETORNO DA VIEW ===
    return ft.View(
        route="/dashboard",
        padding=0,
        bgcolor="white",
        controls=[
            ft.Row(
                expand=True,
                spacing=0,
                controls=[
                    sidebar,
                    conteudo_central
                ]
            )
        ]
    )
