import flet as ft
from utils.services.professores_service import listar_professores, criar_professor

def TelaProfessores(page: ft.Page):
    
    # 1. Tabela
    tabela = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Nome")),
            ft.DataColumn(ft.Text("Departamento")),
            ft.DataColumn(ft.Text("Status")),
        ],
        rows=[]
    )

    def carregar_dados():
        tabela.rows.clear()
        for prof in listar_professores():
            tabela.rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Text(prof.get("nome"))),
                ft.DataCell(ft.Text(prof.get("departamento"))),
                ft.DataCell(ft.Text("Ativo"))
            ]))
        page.update()

    # 2. O Nosso "Modal" personalizado
    nome_input = ft.TextField(label="Nome")
    dep_input = ft.TextField(label="Departamento")

    def salvar(e):
        criar_professor(nome_input.value, dep_input.value)
        container_modal.visible = False
        container_modal.update()
        carregar_dados()

    # REMOVEMOS O 'alignment=ft.alignment.center'
    container_modal = ft.Container(
        content=ft.Card(
            content=ft.Container(
                padding=20,
                content=ft.Column([
                    ft.Text("Novo Professor", size=20, weight="bold"),
                    nome_input, dep_input,
                    ft.ElevatedButton("Salvar", on_click=salvar)
                ])
            )
        ),
        visible=False,
        bgcolor=ft.Colors.BLACK54, # Adiciona um fundo escurecido para parecer um modal real
        expand=True
    )

    def abrir_modal(e):
        container_modal.visible = True
        container_modal.update()

    # 3. Layout Final (Stack)
    layout = ft.Stack(
        controls=[
            ft.Column([
                ft.ElevatedButton("Novo Professor", on_click=abrir_modal),
                tabela
            ]),
            container_modal 
        ],
        expand=True
    )

    carregar_dados()
    return layout