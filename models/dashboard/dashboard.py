import flet as ft 
from components.layout.responsive.responsive import ResponsiveLayout 

from models.dashboard.widgets.kpi_cards import criar_kpi_card 
from models.dashboard.widgets.grafico_eixos import criar_grafico_eixos 

from components.core.constants.constants import * 

def ViewDashboard(page: ft.Page, mudar_tela): 
    """
    Renderiza a tela principal do Dashboard, exibindo métricas chave e gráficos de desempenho institucional.
    """
    
    # Inicializa o layout responsivo com a topbar e sidebar
    layout = ResponsiveLayout( 
        page, 
        titulo_pagina="Dashboard", 
        subtitulo="Indicadores de avaliação institucional", 
        mudar_tela=mudar_tela 
    ) 

    # === Dados simulados (Mock data) ===
    # Dicionário contendo os valores que alimentarão os cartões superiores
    dados_kpi = { 
        "avaliacoes_ativas": "4", 
        "respostas_coletadas": "1.248", 
        "professores_avaliados": "82", 
        "participacao": "74%" 
    } 
    
    # Dados que alimentarão o gráfico de barras
    medias_eixos = {1: 4.5, 2: 4.1, 3: 3.4} # Notas de 0 a 5 por eixo
    nomes_eixos = {1: "Didático", 2: "Docente", 3: "Infra."} # Rótulos dos eixos
    cores_barras = [COR_PRIMARIA, "#34D399", "#F87171"] # Paleta de cores para diferenciar as barras

    # === Montagem dos KPIs ===
    linha_kpis = ft.Row( 
        wrap=True, # Permite que os cartões "quebrem" de linha se a tela for muito estreita
        spacing=20, # Espaço horizontal entre os cartões
        run_spacing=20, # Espaço vertical caso ocorra a quebra de linha (wrap)
        controls=[ 
            criar_kpi_card(layout, "Avaliações ativas", dados_kpi["avaliacoes_ativas"], ft.Icons.ASSIGNMENT_OUTLINED, COR_PRIMARIA), 
            criar_kpi_card(layout, "Respostas coletadas", dados_kpi["respostas_coletadas"], ft.Icons.TRENDING_UP, COR_PRIMARIA), 
            criar_kpi_card(layout, "Professores avaliados", dados_kpi["professores_avaliados"], ft.Icons.SCHOOL_OUTLINED, COR_PRIMARIA), 
            criar_kpi_card(layout, "Participação", dados_kpi["participacao"], ft.Icons.PEOPLE_OUTLINE, COR_PRIMARIA) 
        ] 
    ) 

    # === Montagem do Gráfico ===
    # Delega a construção do bloco do gráfico para a função externa passando os dados mockados
    area_graficos = criar_grafico_eixos(layout, medias_eixos, nomes_eixos, cores_barras) 

    # === Layout final da página ===
    conteudo = ft.Column( 
        expand=True, 
        spacing=25, 
        scroll=ft.ScrollMode.AUTO, # Habilita rolagem na página inteira se os gráficos passarem da altura da tela
        controls=[linha_kpis, area_graficos] # Empilha os KPIs em cima e o gráfico embaixo
    ) 

    layout.add_content(conteudo) 
    return layout.criar_view("/dashboard") 