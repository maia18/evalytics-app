import flet as ft
# Importa as constantes globais do projeto (ex: cores, margens padrão)
from components.core.constants.constants import *

def criar_tabela_resultados(page, layout, borda_container):
    """
    Constrói a tabela de dados (DataTable) responsável por exibir o consolidado
    das avaliações institucionais divididas por eixo e semestre.
    
    Args:
        page (ft.Page): A página atual do Flet (necessária para verificar o tema ativo).
        layout: A instância do layout atual para buscar as cores adaptativas do fundo.
        borda_container (ft.Border): Estilo de borda padronizado passado pelo componente pai.
    """
    
    # Retorna o container principal que envelopa a tabela
    return ft.Container(
        expand=True, # Permite que a tabela cresça para preencher o espaço vertical restante da tela
        bgcolor=layout.cores[CARD], # Cor de fundo dinâmica do painel
        padding=25, # Margem interna para o conteúdo respirar
        border=borda_container, # Reaproveita a mesma borda usada nos filtros para manter coerência visual
        border_radius=10, # Arredonda levemente as quinas
        
        # O conteúdo é empilhado em uma coluna: Título em cima, Tabela embaixo
        content=ft.Column(
            controls=[
                # Título da seção
                ft.Text("Resultados Consolidados", size=18, weight="bold", color=layout.cores[TEXTO_PRINCIPAL]),
                
                # Componente nativo de tabela de dados do Material Design
                ft.DataTable(
                    # Lógica de cor dinâmica: 
                    # Se o modo escuro estiver ativado, usa um cinza azulado bem escuro. 
                    # Caso contrário, usa um azul bem claro ("blue50").
                    heading_row_color=ft.Colors.BLUE_GREY_900 if page.theme_mode == ft.ThemeMode.DARK else "blue50",
                    
                    # === Definição das Colunas (Cabeçalhos) ===
                    # Utiliza ft.Colors.ON_SURFACE para garantir que o texto sempre tenha contraste contra o fundo
                    columns=[
                        ft.DataColumn(ft.Text("Semestre", weight="bold", color=ft.Colors.ON_SURFACE)),
                        ft.DataColumn(ft.Text("Infraestrutura", weight="bold", color=ft.Colors.ON_SURFACE)),
                        ft.DataColumn(ft.Text("Didática", weight="bold", color=ft.Colors.ON_SURFACE)),
                        ft.DataColumn(ft.Text("Atendimento", weight="bold", color=ft.Colors.ON_SURFACE)),
                        ft.DataColumn(ft.Text("Material", weight="bold", color=ft.Colors.ON_SURFACE)),
                        ft.DataColumn(ft.Text("Inovação", weight="bold", color=ft.Colors.ON_SURFACE)),
                    ],
                    
                    # === Inserção das Linhas de Dados (Mock Data) ===
                    rows=[
                        # Primeira linha: Resultados consolidados do semestre 2025.2
                        ft.DataRow(cells=[
                            ft.DataCell(ft.Text("2025.2", color=ft.Colors.ON_SURFACE)),
                            ft.DataCell(ft.Text("4.8", color=ft.Colors.ON_SURFACE)),
                            ft.DataCell(ft.Text("4.5", color=ft.Colors.ON_SURFACE)),
                            ft.DataCell(ft.Text("4.0", color=ft.Colors.ON_SURFACE)),
                            ft.DataCell(ft.Text("4.2", color=ft.Colors.ON_SURFACE)),
                            ft.DataCell(ft.Text("4.7", color=ft.Colors.ON_SURFACE)),
                        ]),
                        
                        # Segunda linha: Semestre em andamento (2026.1), sem dados fechados ainda
                        ft.DataRow(cells=[
                            ft.DataCell(ft.Text("2026.1", color=ft.Colors.ON_SURFACE)),
                            ft.DataCell(ft.Text("Aguardando", color=ft.Colors.ON_SURFACE)), # Feedback descritivo para o usuário
                            ft.DataCell(ft.Text("-", color=ft.Colors.ON_SURFACE)),          # Traços indicando ausência de dados
                            ft.DataCell(ft.Text("-", color=ft.Colors.ON_SURFACE)),
                            ft.DataCell(ft.Text("-", color=ft.Colors.ON_SURFACE)),
                            ft.DataCell(ft.Text("-", color=ft.Colors.ON_SURFACE)),          # Preenchido o espaço vazio com "-" para manter o padrão visual
                        ]),
                    ],
                )
            ]
        )
    )