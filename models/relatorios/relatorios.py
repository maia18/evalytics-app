import flet as ft
from components.layout.responsive.responsive import ResponsiveLayout
from components.core.constants.constants import *

# Importa os subcomponentes isolados (Tabela e Filtros)
from models.relatorios.widgets.filtros_relatorios import criar_secao_filtros
from models.relatorios.widgets.tabela_resultados import criar_tabela_resultados

from models.relatorios.views.resultados_view import TelaResultados  # Importa o Dashboard Executivo recém-criado que está na pasta views


def ViewRelatorios(page: ft.Page, mudar_tela):
    """
    Renderiza a tela principal de 'Relatórios e Exportações'.
    Utiliza um sistema de Abas (Tabs) para organizar a exibição entre o Dashboard Gráfico e a Tabela de Dados Brutos.
    """

    # Cria o layout base responsivo da página (cabeçalho, título, subtítulo, navegação etc.)
    # 'mudar_tela' é repassado para permitir navegação para outras telas a partir daqui.
    layout = ResponsiveLayout(
        page,
        titulo_pagina="Relatórios e Exportações",
        subtitulo="Analise indicadores visuais e exporte resultados consolidados.",
        mudar_tela=mudar_tela
    )

    # Define uma borda reutilizável (linha fina em todos os lados) usando a cor padrão de borda do tema atual (layout.cores[BORDA]). Será aplicada nos containers dos filtros e da tabela para dar um contorno visual consistente.
    borda_container = ft.Border(
        top=ft.BorderSide(1, layout.cores[BORDA]),
        bottom=ft.BorderSide(1, layout.cores[BORDA]),
        left=ft.BorderSide(1, layout.cores[BORDA]),
        right=ft.BorderSide(1, layout.cores[BORDA]),
    )

    # === Instanciação dos Componentes ===

    # Seção de filtros (ex: datas, categorias etc.) usada na aba de Dados Brutos.
    secao_filtros = criar_secao_filtros(layout, borda_container, page)

    # Tabela com os resultados/dados brutos, também usada na aba de Dados Brutos.
    tabela_resultados = criar_tabela_resultados(page, layout, borda_container)

    # Instancia a View do Dashboard Executivo (gráficos/indicadores visuais).
    dashboard_visual = TelaResultados(page) # Esse será o conteúdo exibido na primeira aba (índice 0)

    # Monta o conteúdo da Aba 2 (Dados Brutos): um Container com padding no topo, contendo uma Column que empilha a seção de filtros, um espaçador transparente (Divider "invisível" usado só para dar respiro visual) e a tabela de resultados.
    conteudo_aba_dados = ft.Container(
        padding=ft.Padding.only(top=20),
        content=ft.Column(
            expand=True,
            controls=[
                secao_filtros,
                ft.Divider(height=20, color="transparent"),  # espaçador visual, sem linha visível
                tabela_resultados
            ]
        )
    )

    # Container "casca" que vai segurar o conteúdo dinâmico exibido conforme a aba selecionada. Começa mostrando o dashboard_visual (aba 0, selecionada por padrão).
    container_conteudo = ft.Container(content=dashboard_visual, expand=True)

    def mudar_aba(e):
        """
        Handler do evento on_change das Tabs.
        Como as abas aqui NÃO usam ft.TabBarView (o conteúdo de cada aba já foi construído acima), trocamos manualmente o conteúdo do container_conteudo de acordo com o índice da aba selecionada (e.control.selected_index).
        """
        if e.control.selected_index == 0:
            container_conteudo.content = dashboard_visual
        else:
            container_conteudo.content = conteudo_aba_dados
        container_conteudo.update()  # força o redesenho apenas desse container

    # === Montagem do Layout Principal ===
    conteudo = ft.Column(
        expand=True,
        controls=[
            ft.Tabs(
                length=2,                  # precisa bater com a quantidade de ft.Tab abaixo
                selected_index=0,          # aba inicialmente selecionada (Dashboard Executivo)
                animation_duration=300,    # duração (ms) da animação de troca de aba
                on_change=mudar_aba,       # dispara mudar_aba() sempre que o usuário troca de aba
                content=ft.TabBar(
                    tabs=[
                        ft.Tab(
                            label="Dashboard Executivo",
                            icon=ft.Icons.DASHBOARD,
                        ),
                        ft.Tab(
                            label="Dados Brutos e Exportação",
                            icon=ft.Icons.TABLE_CHART,
                        ),
                    ]
                ),
            ),
            container_conteudo  # área abaixo das abas, onde o conteúdo dinâmico é exibido
        ]
    )

    layout.add_content(conteudo) # Adiciona a Column montada (abas + conteúdo) ao layout responsivo da página.
    return layout.criar_view("/relatorios")