import flet as ft
from services.avaliacoes_service import listar_avaliacoes
from datetime import datetime

def TelaResultados(page: ft.Page):
    
    # Estrutura da Tabela de Resultados
    tabela = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Curso Avaliado", weight="bold")),
            ft.DataColumn(ft.Text("Data da Avaliação", weight="bold")),
            ft.DataColumn(ft.Text("Média Geral", weight="bold")),
            ft.DataColumn(ft.Text("Critérios Avaliados", weight="bold")),
        ],
        rows=[]
    )

    def carregar_dados():
        avaliacoes = listar_avaliacoes()
        
        for av in avaliacoes:
            # 1. Formatar a Data
            try:
                data_obj = datetime.fromisoformat(av.get("data_avaliacao", ""))
                data_formatada = data_obj.strftime("%d/%m/%Y às %H:%M")
            except:
                data_formatada = "Data desconhecida"

            # 2. Calcular a Média
            respostas = av.get("respostas", {})
            # Filtra apenas as notas numéricas (1 a 5) ignorando o "NSA"
            notas = [int(v) for v in respostas.values() if v in ["1", "2", "3", "4", "5"]]
            
            media = sum(notas) / len(notas) if len(notas) > 0 else 0
            qtd_avaliada = len(notas)

            # 3. Adicionar na Tabela
            tabela.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(av.get("curso_nome", "Desconhecido"))),
                    ft.DataCell(ft.Text(data_formatada)),
                    ft.DataCell(
                        ft.Text(
                            f"{media:.2f} / 5.0", 
                            weight="bold", 
                            # Pinta de vermelho se a média for baixa, verde se for alta
                            color="red700" if media < 3 else "green700" 
                        )
                    ),
                    ft.DataCell(ft.Text(f"{qtd_avaliada} indicadores")),
                ])
            )
        page.update()

    # Layout Final
    layout = ft.Column(
        controls=[
            ft.Text("Relatório de Avaliações Institucionais", size=24, weight="bold"),
            ft.Divider(height=20, color="transparent"),
            tabela
        ],
        expand=True
    )

    carregar_dados()
    return layout