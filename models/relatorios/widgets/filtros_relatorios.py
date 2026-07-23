import flet as ft
# Importa as cores e configurações padronizadas do sistema
from components.core.constants.constants import *
# Importa as funções que contêm a lógica de exportação de arquivos
from models.relatorios.core.export_pdf import gerar_pdf
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

    # === Montagem do Painel ===
    
    # Retorna o painel englobando todos os controles
    return ft.Container(
        bgcolor=layout.cores[CARD], # Cor de fundo que respeita o tema Claro/Escuro
        padding=20, # Margem interna para evitar que os elementos toquem nas bordas
        border_radius=8, # Bordas levemente arredondadas
        border=borda_container, # Aplica a borda padronizada recebida como parâmetro
        
        # A linha principal organiza os filtros e botões
        content=ft.Row(
            # Distribui o espaço: Filtros colados à esquerda, Botões colados à direita
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                # Bloco Esquerdo: Agrupa os campos de busca/filtros com um pequeno espaçamento entre eles
                ft.Row([dropdown_semestre, dropdown_eixo], spacing=10),
                
                # Bloco Direito: Agrupa as ações de exportação de dados
                ft.Row(
                    spacing=10,
                    controls=[
                        # Botão de exportação para Excel/Planilha
                        ft.ElevatedButton(
                            "Exportar CSV", 
                            icon=ft.Icons.TABLE_VIEW, # Ícone de tabela
                            bgcolor="green700", # Cor verde padrão para planilhas
                            color="white",
                            # Dispara a função importada repassando a página
                            on_click=lambda e: exportar_csv(page)
                        ),
                        # Botão de exportação para PDF
                        ft.ElevatedButton(
                            "Gerar Documento (PDF)", 
                            icon=ft.Icons.PICTURE_AS_PDF, # Ícone de PDF
                            bgcolor="red700", # Cor vermelha padrão para arquivos PDF
                            color="white",
                            # Dispara a função importada repassando a página
                            on_click=lambda e: gerar_pdf(page)
                        )
                    ]
                )
            ]
        )
    )