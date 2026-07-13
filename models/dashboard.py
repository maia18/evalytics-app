""" Importações """  
import flet as ft
from components.responsive_layout import ResponsiveLayout

def ViewDashboard(page: ft.Page, mudar_tela):
    
    """
    Tela de Dashboard do sistema Evalytics.
    Mostra KPIs, gráficos de desempenho e participação, com sidebar responsiva.
    """
    
    # Criar o layout responsivo
    layout = ResponsiveLayout(page, "Dashboard", "Acompanhe o engajamento e os resultados.")
    
    # === 1. COMPONENTE: CARDS DE KPI ===
    def criar_kpi_card(titulo, valor, icone, cor_icone, subtitulo):
        """
        Cria um card de KPI com título, valor, subtítulo e ícone.
        """
        return ft.Container(
            width=260,
            bgcolor=layout.COR_CARD,
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
                            ft.Text(valor, size=28, weight="bold", color=layout.COR_TEXTO_PRINCIPAL),
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
                        ft.Text(rotulo, size=14, weight="bold", color=layout.COR_TEXTO_PRINCIPAL),
                        ft.Text(f"{nota} / 5.0", size=14, color="grey700", weight="bold")
                    ]
                ),
                ft.ProgressBar(value=nota/5.0, color=cor, bgcolor="grey200", height=10)
            ]
        )

    card_grafico_barras = ft.Container(
        width=600,
        bgcolor=layout.COR_CARD,
        padding=25,
        border_radius=10,
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color="black12"),
        content=ft.Column(
            spacing=20,
            controls=[
                ft.Text("Desempenho Médio por Eixo", size=18, weight="bold", color=layout.COR_TEXTO_PRINCIPAL),
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
        bgcolor=layout.COR_CARD,
        padding=25,
        border_radius=10,
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color="black12"),
        content=ft.Column(
            spacing=20,
            controls=[
                ft.Text("Participação por Área", size=18, weight="bold", color=layout.COR_TEXTO_PRINCIPAL),
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

    # === CONTEÚDO PRINCIPAL ===
    conteudo = ft.Column(
        expand=True,
        spacing=25,
        scroll=ft.ScrollMode.AUTO,
        controls=[
            ft.Column(
                spacing=5,
                controls=[
                    ft.Text("Dashboard do Sistema", size=28, weight="bold", color=layout.COR_TEXTO_PRINCIPAL),
                    ft.Text("Acompanhe o engajamento e os resultados.", size=16, color="grey"),
                ]
            ),
            ft.Divider(color="transparent", height=5),
            linha_kpis,
            linha_graficos
        ]
    )
    
    # Adicionar conteúdo ao layout
    layout.add_content(conteudo)
    
    # Retornar a view
    return layout.criar_view("/dashboard")