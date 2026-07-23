import flet as ft
# Importa as cores e configurações padronizadas do sistema
from components.core.constants.constants import *

# 1. CORREÇÃO DO IMPORT: Traz a função unificada e poderosa que criamos no arquivo anterior
# Substituindo o antigo "gerar_pdf" que causava o ImportError.
from models.relatorios.core.export_pdf import gerar_pdf_completo 
from models.avaliacoes.core.export_csv import exportar_csv

def criar_secao_filtros(layout, borda_container, page):
    """
    Constrói a barra superior da tela de relatórios, contendo os menus suspensos (Dropdowns) 
    para filtragem de dados e os botões de ação para exportação (CSV/PDF).
    
    Args:
        layout: A instância do layout atual (usada para extrair a cor de fundo adaptativa do cartão).
        borda_container (ft.Border): O objeto de estilo da borda, reaproveitado para manter consistência visual.
        page (ft.Page): A página atual, repassada para as funções de exportação (necessária para exibir SnackBar/alertas).
    """
    
    # === Campos de Filtro ===
    
    # Filtro por Semestre Letivo
    dropdown_semestre = ft.Dropdown(
        label="Semestre", # Título que flutua sobre o campo
        options=[
            ft.dropdown.Option("2026.1"), 
            ft.dropdown.Option("2025.2")
        ],
        value="2026.1", # Valor padrão selecionado ao abrir a tela
        width=200, # Largura fixa para manter um alinhamento organizado
        dense=True # Torna o componente ligeiramente mais compacto verticalmente
    )

    # Filtro por Eixo da Avaliação Institucional
    dropdown_eixo = ft.Dropdown(
        label="Eixo Avaliativo",
        options=[
            ft.dropdown.Option("Infraestrutura"),
            ft.dropdown.Option("Didática"),
            ft.dropdown.Option("Atendimento")
        ],
        width=200,
        dense=True
    )

    # === MOCK DATA (Dados de Teste Temporários) ===
    # Como a nova função gerar_pdf_completo exige dados matemáticos para desenhar o gráfico,
    # injetamos este dicionário fictício apenas para o botão funcionar perfeitamente 
    # até que a consulta real ao banco de dados seja implementada.
    medias_mock = {1: 4.8, 2: 4.5, 3: 4.7}
    nomes_eixos_mock = {1: "Infraestrutura", 2: "Didática", 3: "Atendimento"}

    # === Montagem do Painel ===
    
    # Retorna o painel englobando todos os controles
    return ft.Container(
        bgcolor=layout.cores[CARD], # Cor de fundo que respeita o tema Claro/Escuro
        padding=20, # Margem interna generosa
        border_radius=8, # Bordas levemente arredondadas
        border=borda_container, # Aplica a borda padronizada recebida
        
        # A linha principal organiza os filtros à esquerda e os botões à direita
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                # Bloco Esquerdo: Agrupa os Dropdowns com um pequeno espaçamento
                ft.Row([dropdown_semestre, dropdown_eixo], spacing=10),
                
                # Bloco Direito: Agrupa as ações de exportação
                ft.Row(
                    spacing=10,
                    controls=[
                        # Botão de exportação CSV
                        ft.ElevatedButton(
                            "Exportar CSV", 
                            icon=ft.Icons.TABLE_VIEW, 
                            bgcolor="green700", 
                            color="white",
                            on_click=lambda e: exportar_csv(page)
                        ),
                        # Botão de exportação PDF
                        ft.ElevatedButton(
                            "Gerar Documento (PDF)", 
                            icon=ft.Icons.PICTURE_AS_PDF, 
                            bgcolor="red700", 
                            color="white",
                            
                            # 2. CORREÇÃO DA CHAMADA: Invoca a nova função repassando os parâmetros 
                            # exigidos pelo Plotly e a string do semestre selecionada dinamicamente no Dropdown.
                            on_click=lambda e: gerar_pdf_completo(
                                page, 
                                medias=medias_mock, 
                                nomes_eixos=nomes_eixos_mock, 
                                semestre=dropdown_semestre.value
                            )
                        )
                    ]
                )
            ]
        )
    )