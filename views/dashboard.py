import flet as ft
from database.conexao import obter_medias_dashboard

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
                ft.TextButton("Avaliações", icon=ft.Icons.ASSIGNMENT, on_click=lambda _: mudar_tela("/avaliacoes"), style=estilo_botao_menu),
                ft.TextButton("Relatórios", icon=ft.Icons.PIE_CHART, style=estilo_botao_menu),
                ft.TextButton("Cursos", icon=ft.Icons.BOOK, style=estilo_botao_menu),
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
        
    # 1º: BUSCAMOS OS DADOS PRIMEIRO!
    # === BUSCANDO DADOS DO FIREBASE ===
    dados_nuvem = obter_medias_dashboard()
    if not dados_nuvem:
        infra_atual, didatica_atual, atend_atual, mat_atual, inov_atual = 0, 0, 0, 0, 0
        media_geral = 0.0
    else:
        infra_atual = dados_nuvem.get("infraestrutura", 0)
        didatica_atual = dados_nuvem.get("didatica", 0)
        atend_atual = dados_nuvem.get("atendimento", 0)
        mat_atual = dados_nuvem.get("material", 0)
        inov_atual = dados_nuvem.get("inovacao", 0)
        
        media_geral = round((infra_atual + didatica_atual + atend_atual + mat_atual + inov_atual) / 5, 1)
    
    # 2º: AGORA SIM, DESENHAMOS A TELA COM AS VARIÁVEIS PRONTAS
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
            criar_card_kpi("Taxa de Resposta", "85%", ft.Icons.TRENDING_UP, "green700", "green50"),
            criar_card_kpi("Média Geral", f"{media_geral}/5", ft.Icons.STAR, "amber700", "amber50"), 
            criar_card_kpi("Avaliações Pendentes", "12", ft.Icons.PENDING_ACTIONS, "red700", "red50"),
            criar_card_kpi("Departamentos", "8", ft.Icons.ACCOUNT_BALANCE, "blue700", "blue50"),
        ]
    )

    # === CRIAÇÃO DE UM GRÁFICO CUSTOMIZADO ===
    def criar_coluna_comparativa(titulo, nota_atual, nota_anterior):
        altura_maxima = 150 
        
        alt_atual = (nota_atual / 5.0) * altura_maxima
        alt_anterior = (nota_anterior / 5.0) * altura_maxima

        return ft.Column(
            horizontal_alignment="center", # Simplificado para string
            spacing=10,
            controls=[
                ft.Row(
                    alignment="center", # Simplificado
                    vertical_alignment="end", # <--- CORRIGIDO AQUI
                    spacing=6,
                    height=altura_maxima, 
                    controls=[
                        # Barra do Semestre Anterior
                        ft.Container(
                            width=25,
                            height=alt_anterior,
                            bgcolor="blue200",
                            border_radius=6,
                            animate=ft.Animation(500, "easeOut") 
                        ),
                        # Barra do Semestre Atual
                        ft.Container(
                            width=25,
                            height=alt_atual,
                            bgcolor="blue700",
                            border_radius=6,
                            animate=ft.Animation(500, "easeOut")
                        )
                    ]
                ),
                # Rótulo da Categoria
                ft.Text(titulo, size=13, color="black54", weight="bold")
            ]
        )
        
    # === BUSCANDO DADOS DO FIREBASE ===
    dados_nuvem = obter_medias_dashboard()
    
    # Tratamento caso o banco esteja vazio
    if not dados_nuvem:
        infra_atual, didatica_atual, atend_atual, mat_atual, inov_atual = 0, 0, 0, 0, 0
        media_geral = 0.0
    else:
        infra_atual = dados_nuvem.get("infraestrutura", 0)
        didatica_atual = dados_nuvem.get("didatica", 0)
        atend_atual = dados_nuvem.get("atendimento", 0)
        mat_atual = dados_nuvem.get("material", 0)
        inov_atual = dados_nuvem.get("inovacao", 0)
        
        # Calcula a média geral do semestre atual
        media_geral = round((infra_atual + didatica_atual + atend_atual + mat_atual + inov_atual) / 5, 1)

    # Agrupando as colunas no nosso "Gráfico"
    grafico_customizado = ft.Container(
        expand=True,
        content=ft.Row(
            alignment="spaceAround",
            vertical_alignment="end",
            controls=[
                # Passamos a variável do Firebase para a barra forte, e mantemos a clara fixa
                criar_coluna_comparativa("Infraestrutura", infra_atual, 3.9),
                criar_coluna_comparativa("Didática", didatica_atual, 4.1),
                criar_coluna_comparativa("Atendimento", atend_atual, 3.5),
                criar_coluna_comparativa("Material", mat_atual, 3.8),
                criar_coluna_comparativa("Inovação", inov_atual, 3.9),
            ]
        )
    )
    
    # Área reservada para o Gráfico (Atualizada)
    area_grafico = ft.Container(
        expand=True,
        width=float("inf"),
        bgcolor="white",
        border_radius=12,
        padding=30,
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color="black12"),
        content=ft.Column(
            controls=[
                ft.Text("Desempenho por Categoria", size=18, weight="bold", color="black87"),
                ft.Text("Comparativo: Semestre Atual (Azul Escuro) vs Anterior (Azul Claro)", size=14, color="black54"),
                ft.Container(height=15), # Espaçador
                grafico_customizado 
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
