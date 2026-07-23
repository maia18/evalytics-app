import flet as ft
# Importa o layout base que garante a responsividade (Sidebar, Topbar, etc.)
from components.layout.responsive.responsive import ResponsiveLayout
# Importa as paletas de cores e espaçamentos padrão do sistema
from components.core.constants.constants import *

# Importa os subcomponentes isolados que compõem esta tela
from models.relatorios.widgets.filtros_relatorios import criar_secao_filtros
from models.relatorios.widgets.tabela_resultados import criar_tabela_resultados

def ViewRelatorios(page: ft.Page, mudar_tela):
    """
    Renderiza a tela principal de 'Relatórios e Exportações'.
    Atua como a View orquestradora que agrupa os painéis de filtro de dados 
    e a tabela de exibição/exportação dos resultados institucionais.
    """
    
    # Inicializa o contêiner responsivo passando o título e subtítulo para a Topbar
    layout = ResponsiveLayout(
        page,
        titulo_pagina="Relatórios e Exportações",
        subtitulo="Gere visualizações dinâmicas e exporte resultados.",
        mudar_tela=mudar_tela
    )

    # Criação de um objeto de borda reutilizável.
    # Como tanto o painel de filtros quanto a tabela usarão o mesmo estilo de caixa,
    # centralizamos a borda aqui usando a cor dinâmica do tema e repassamos como argumento.
    borda_container = ft.Border(
        top=ft.BorderSide(1, layout.cores[BORDA]),
        bottom=ft.BorderSide(1, layout.cores[BORDA]),
        left=ft.BorderSide(1, layout.cores[BORDA]),
        right=ft.BorderSide(1, layout.cores[BORDA]),
    )

    # === Instanciação dos Componentes ===
    # Delega a construção do formulário de filtros para a função externa
    secao_filtros = criar_secao_filtros(layout, borda_container, page)
    
    # Delega a construção do painel de dados (DataGrid/DataTable) para a função externa
    tabela_resultados = criar_tabela_resultados(page, layout, borda_container)

    # === Montagem do Layout Principal ===
    conteudo = ft.Column(
        expand=True, # Garante que a coluna ocupe todo o espaço da tela em altura
        controls=[
            # Cabeçalho interno da página
            ft.Text("Relatórios e Exportações", size=28, weight="bold", color=layout.cores[TEXTO_PRINCIPAL]),
            ft.Text("Gere visualizações dinâmicas, analise os critérios e exporte os resultados.", size=16, color="grey"),
            
            # Divisor transparente atuando como margem (respiro) entre o cabeçalho e os filtros
            ft.Divider(height=30, color="transparent"),
            
            # Painel superior contendo os Dropdowns de busca e filtros
            secao_filtros,
            
            # Outro respiro antes da exibição dos dados
            ft.Divider(height=20, color="transparent"),
            
            # Painel inferior exibindo a tabela e os botões de exportação (PDF/Excel)
            tabela_resultados
        ]
    )

    # Injeta a estrutura montada dentro do contêiner flexível do ResponsiveLayout
    layout.add_content(conteudo)
    
    # Retorna a View devidamente registrada com sua rota oficial para o sistema de navegação
    return layout.criar_view("/relatorios")