import flet as ft
from components.layout.responsive import ResponsiveLayout

def ViewDashboard(page: ft.Page, mudar_tela):
    """
    Tela de Dashboard do sistema Evalytics.
    """
    
    layout = ResponsiveLayout(
        page, 
        titulo_pagina="Dashboard", 
        subtitulo="Indicadores de avaliação institucional", 
        mudar_tela=mudar_tela
    )
    
    # ==========================================
    # 1. DADOS REAIS
    # ==========================================
    dados_kpi = {
        "avaliacoes_ativas": "4",
        "respostas_coletadas": "1.248",
        "professores_avaliados": "82",
        "participacao": "74%"
    }
    
    medias_eixos = {
        1: 4.5,
        2: 4.1,
        3: 3.4
    }
    
    nomes_eixos = {
        1: "Didático",
        2: "Docente",
        3: "Infra."
    }
    
    # ==========================================
    # 2. COMPONENTE: CARDS DE KPI 
    # ==========================================
    def criar_kpi_card(titulo, valor, icone, cor_icone):
        borda_card = ft.Border(
            top=ft.BorderSide(1, layout.COR_BORDA),
            bottom=ft.BorderSide(1, layout.COR_BORDA),
            left=ft.BorderSide(1, layout.COR_BORDA),
            right=ft.BorderSide(1, layout.COR_BORDA)
        )
        
        return ft.Container(
            width=240,
            bgcolor=layout.COR_CARD,
            padding=20, 
            border_radius=8,
            border=borda_card,
            content=ft.Column(
                spacing=15,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text(titulo, size=14, color="grey600", weight="w500"),
                            ft.Icon(icone, color=cor_icone, size=18)
                        ]
                    ),
                    ft.Text(valor, size=28, weight="bold", color=layout.COR_TEXTO_PRINCIPAL),
                ]
            )
        )

    linha_kpis = ft.Row(
        wrap=True,
        spacing=20,
        run_spacing=20,
        controls=[
            criar_kpi_card("Avaliações ativas", dados_kpi["avaliacoes_ativas"], ft.Icons.ASSIGNMENT_OUTLINED, layout.COR_PRIMARIA),
            criar_kpi_card("Respostas coletadas", dados_kpi["respostas_coletadas"], ft.Icons.TRENDING_UP, layout.COR_PRIMARIA),
            criar_kpi_card("Professores avaliados", dados_kpi["professores_avaliados"], ft.Icons.SCHOOL_OUTLINED, layout.COR_PRIMARIA),
            criar_kpi_card("Participação", dados_kpi["participacao"], ft.Icons.PEOPLE_OUTLINE, layout.COR_PRIMARIA)
        ]
    )

    # ==========================================
    # 3. GRÁFICO CUSTOMIZADO (À Prova de Falhas)
    # ==========================================
    cores_barras = [layout.COR_PRIMARIA, "#34D399", "#F87171"] 
    
    def criar_coluna_grafico(nome, nota, cor):
        # A altura máxima da barra será 200 pixels (equivalente à nota 5.0)
        altura_max = 200
        altura_barra = (nota / 5.0) * altura_max
        
        return ft.Column(
            alignment=ft.MainAxisAlignment.END, # Alinha os itens pelo fundo
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=8,
            controls=[
                # Valor numérico em cima da barra
                ft.Text(f"{nota:.1f}", size=12, weight="bold", color="grey"),
                # A barra visual construída com Container
                ft.Container(
                    width=40,
                    height=altura_barra,
                    bgcolor=cor,
                    border_radius=4,
                    tooltip=f"{nome}: {nota:.1f} / 5.0" # Mantém a interatividade
                ),
                # Nome do eixo na base
                ft.Text(nome, size=12, weight="w500", color=layout.COR_TEXTO_PRINCIPAL)
            ]
        )

    # Monta a lista de colunas dinamicamente
    barras_grafico = []
    for i, (eixo_id, nota) in enumerate(medias_eixos.items()):
        nome = nomes_eixos.get(eixo_id, f"Eixo {eixo_id}")
        cor = cores_barras[i % len(cores_barras)]
        barras_grafico.append(criar_coluna_grafico(nome, nota, cor))

    # Agrupa todas as colunas numa Row para simular o gráfico de barras
    grafico_desempenho = ft.Container(
        height=260,
        padding=20,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            # Corrigido: 'vertical_alignment' é o nome correto para Row na sua versão
            vertical_alignment=ft.CrossAxisAlignment.END, 
            controls=barras_grafico
        )
    )

    borda_grafico = ft.Border(
        top=ft.BorderSide(1, layout.COR_BORDA),
        bottom=ft.BorderSide(1, layout.COR_BORDA),
        left=ft.BorderSide(1, layout.COR_BORDA),
        right=ft.BorderSide(1, layout.COR_BORDA)
    )

    area_graficos = ft.Container(
        bgcolor=layout.COR_CARD,
        padding=30,
        border_radius=8,
        border=borda_grafico,
        content=ft.Column(
            spacing=20,
            controls=[
                ft.Column(
                    spacing=5,
                    controls=[
                        ft.Text("Desempenho Médio por Eixo", size=18, weight="bold", color=layout.COR_TEXTO_PRINCIPAL),
                        ft.Text("Médias das avaliações separadas por categoria (Escala 5.0).", size=14, color="grey"),
                    ]
                ),
                # Insere o nosso gráfico desenhado à mão
                grafico_desempenho
            ]
        )
    )

    # ==========================================
    # 4. MONTAGEM FINAL DO LAYOUT
    # ==========================================
    conteudo = ft.Column(
        expand=True,
        spacing=25,
        scroll=ft.ScrollMode.AUTO,
        controls=[
            linha_kpis,
            area_graficos
        ]
    )
    
    layout.add_content(conteudo)
    return layout.criar_view("/dashboard")