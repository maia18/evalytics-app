import flet as ft
from services.indicadores_service import listar_indicadores, criar_indicador

def TelaIndicadores(page: ft.Page):
    
    # 1. Tabela de Indicadores
    tabela = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Critério de Avaliação", weight="bold")),
            ft.DataColumn(ft.Text("Categoria", weight="bold")),
            ft.DataColumn(ft.Text("Status", weight="bold")),
        ],
        rows=[]
    )

    def carregar_dados():
        tabela.rows.clear()
        for ind in listar_indicadores():
            tabela.rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Text(ind.get("nome", "-"))),
                ft.DataCell(ft.Text(ind.get("categoria", "-"))),
                ft.DataCell(ft.Text("Ativo" if ind.get("ativo", True) else "Inativo"))
            ]))
        page.update()

    # 2. O Modal Customizado
    nome_input = ft.TextField(label="Nome do Indicador (Ex: Laboratórios Práticos)", width=400)
    categoria_input = ft.Dropdown(
        label="Categoria",
        width=400,
        options=[
            ft.dropdown.Option("Infraestrutura"),
            ft.dropdown.Option("Corpo Docente"),
            ft.dropdown.Option("Recursos Didáticos"),
            ft.dropdown.Option("Apoio ao Estudante")
        ]
    )

    def fechar_modal(e):
        container_modal.visible = False
        container_modal.update()

    def salvar(e):
        if nome_input.value and categoria_input.value:
            criar_indicador(nome_input.value, categoria_input.value)
            nome_input.value = ""
            categoria_input.value = None
            fechar_modal(e)
            carregar_dados()

    container_modal = ft.Container(
        content=ft.Card(
            content=ft.Container(
                padding=30,
                content=ft.Column([
                    ft.Text("Cadastrar Novo Indicador", size=20, weight="bold"),
                    ft.Divider(height=10, color="transparent"),
                    nome_input, 
                    categoria_input,
                    ft.Divider(height=10, color="transparent"),
                    ft.Row([
                        ft.TextButton("Cancelar", on_click=fechar_modal),
                        ft.ElevatedButton("Salvar", on_click=salvar, style=ft.ButtonStyle(bgcolor="green700", color="white"))
                    ], alignment=ft.MainAxisAlignment.END)
                ], tight=True)
            )
        ),
        visible=False,
        bgcolor=ft.Colors.BLACK54, 
        expand=True
    )

    def abrir_modal(e):
        container_modal.visible = True
        container_modal.update()

    # 3. Montagem do Layout
    layout = ft.Stack(
        controls=[
            ft.Column([
                ft.Row([
                    ft.Text("Gerenciar Indicadores", size=24, weight="bold"),
                    ft.ElevatedButton("Novo Indicador", icon=ft.Icons.ADD, style=ft.ButtonStyle(bgcolor="green700", color="white"), on_click=abrir_modal)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(height=20, color="transparent"),
                tabela
            ]),
            container_modal 
        ],
        expand=True
    )

    carregar_dados()
    return layout
