import flet as ft
from components.core.constants.constants import *
from components.layout.responsive.responsive import ResponsiveLayout

# Reutilização de Módulos: Importa o "miolo" da tela de avaliações que criamos anteriormente.
from models.avaliacoes.avaliacoes import criar_conteudo_avaliacoes
from models.dashboard.widgets.kpi_cards import criar_kpi_card
from models.dashboard.widgets.grafico_eixos import criar_grafico_eixos

# Importa o card de desempenho que consome os dados em tempo real do Firestore.
from models.dashboard.layout.card_grafico_desempenho import criar_card_grafico_desempenho

def ViewDashboard(page: ft.Page, mudar_tela):
    """Constrói a página principal do Dashboard com navegação por abas."""
    
    # Inicializa o gerenciador de layout base (Topbar, Sidebar, Responsividade e Tema).
    layout = ResponsiveLayout(
        page,
        titulo_pagina="Dashboard",
        subtitulo="Indicadores de avaliação institucional",
        mudar_tela=mudar_tela
    )

    # === Dados simulados (Mock data) ===
    # TODO: Assim como fizemos com a tabela e com o gráfico de desempenho, estes dados 
    # dos KPIs e do gráfico de eixos poderão ser substituídos por funções do Firestore futuramente.
    dados_kpi = {
        "avaliacoes_ativas": "4",
        "respostas_coletadas": "1.248",
        "professores_avaliados": "82",
        "participacao": "74%"
    }
    
    medias_eixos = {1: 4.5, 2: 4.1, 3: 3.4}
    nomes_eixos = {1: "Didático", 2: "Docente", 3: "Infra."}
    cores_barras = [COR_PRIMARIA, "#34D399", "#F87171"]

    # === Montagem dos KPIs ===
    linha_kpis = ft.Row(
        # wrap=True é essencial para responsividade: se a tela encolher, 
        # os cards descem para a próxima linha automaticamente sem espremer ou quebrar a tela.
        wrap=True,
        spacing=20,
        run_spacing=20,
        controls=[
            criar_kpi_card(layout, "Avaliações ativas", dados_kpi["avaliacoes_ativas"], ft.Icons.ASSIGNMENT_OUTLINED, COR_PRIMARIA),
            criar_kpi_card(layout, "Respostas coletadas", dados_kpi["respostas_coletadas"], ft.Icons.TRENDING_UP, COR_PRIMARIA),
            criar_kpi_card(layout, "Professores avaliados", dados_kpi["professores_avaliados"], ft.Icons.SCHOOL_OUTLINED, COR_PRIMARIA),
            criar_kpi_card(layout, "Participação", dados_kpi["participacao"], ft.Icons.PEOPLE_OUTLINE, COR_PRIMARIA)
        ]
    )

    # === Montagem dos Gráficos ===
    # Gráfico de barras horizontais usando os dados de mock.
    area_graficos = criar_grafico_eixos(layout, medias_eixos, nomes_eixos, cores_barras)
    
    # INJEÇÃO DO NOVO CARD: Instancia o componente que busca os dados reais do Firestore.
    # Passamos o 'layout' para que o card herde automaticamente as cores (modo claro/escuro).
    card_desempenho = criar_card_grafico_desempenho(layout)

    # === Conteúdo de cada aba ===
    # IMPORTANTE ARQUITETURAL: expand=True fica no Container (dá o limite de altura vindo do TabBarView),
    # e scroll=AUTO fica isolado na Column interna, SEM expand=True nela mesma.
    # Isso evita o bug do Flet de espaço em branco + scroll fantasma quando
    # expand e scroll são combinados na mesma Column (github.com/flet-dev/flet/issues/6087).
    conteudo_dashboard_executivo = ft.Container(
        expand=True, # Ancora o container no TabBarView, dando altura limitada
        content=ft.Column(
            spacing=16, # Mantém 16px de respiro entre os blocos (KPIs -> Eixos -> Desempenho)
            scroll=ft.ScrollMode.AUTO, # Habilita rolagem suave caso os 3 blocos juntos ultrapassem a altura do monitor
            controls=[
                ft.Container(height=8), # Spacer invisível para desgrudar o primeiro KPI do topo da aba
                linha_kpis,             # Renderiza a linha de 4 blocos quadrados
                area_graficos,          # Renderiza o card do gráfico de eixos de avaliação
                card_desempenho         # ADICIONADO AQUI: Renderiza o novo card com as notas do Firestore no final da página!
            ]
        )
    )
    
    # === Abas (Tabs) ===
    # Configura a barra de navegação superior interna da página.
    barra_abas = ft.TabBar(
        tabs=[
            ft.Tab(label="Dashboard", icon=ft.Icons.GRID_VIEW_ROUNDED),
            ft.Tab(label="Gestão de Ciclos e Respostas", icon=ft.Icons.TABLE_ROWS_ROUNDED),
        ],
        label_color=COR_PRIMARIA,
        unselected_label_color="grey600",
        indicator_color=COR_PRIMARIA,
        divider_color=layout.cores[BORDA],
    )

    # O TabBarView é o contêiner dinâmico que alterna as telas quando o usuário clica em uma aba.
    conteudo_abas = ft.TabBarView(
        expand=True,
        controls=[
            # Índice 0: Conteúdo construído acima contendo KPIs e Gráficos.
            conteudo_dashboard_executivo,
            
            # Índice 1: O poder da componentização! A tela inteira de avaliações é injetada aqui.
            # Isso significa que a tabela que criamos em `avaliacoes.py` vai renderizar dentro desta aba.
            criar_conteudo_avaliacoes(layout, mudar_tela, page)
        ],
    )

    # Agrupa a barra de botões com as views visuais que elas controlam.
    abas = ft.Tabs(
        length=2,
        expand=True,
        content=ft.Column(
            expand=True,
            controls=[barra_abas, conteudo_abas],
        ),
    )

    # === Layout final da página ===
    # Envelopa tudo em uma coluna mestre final para enviar ao ResponsiveLayout.
    conteudo = ft.Column(
        expand=True,
        controls=[abas]
    )

    # Passa o conteúdo finalizado para o gerenciador central renderizar a interface base + conteúdo.
    layout.add_content(conteudo)
    
    # Devolve a estrutura pronta do Flet para o Roteador.
    return layout.criar_view("/dashboard")