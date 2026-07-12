import flet as ft
from utils.services.professores_service import listar_professores, criar_professor

def TelaProfessores(page: ft.Page):
    
    # 1. Tabela de Professores
    tabela = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Nome")),
            ft.DataColumn(ft.Text("Departamento")),
            ft.DataColumn(ft.Text("Status")),
        ],
        rows=[]
    )

    # Função que carrega os dados dos professores e popula a tabela
    def carregar_dados():
        tabela.rows.clear()  # Limpa a tabela antes de recarregar
        for prof in listar_professores():
            tabela.rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Text(prof.get("nome"))),          # Nome do professor
                ft.DataCell(ft.Text(prof.get("departamento"))), # Departamento
                ft.DataCell(ft.Text("Ativo"))                   # Status fixo (pode ser adaptado)
            ]))
        page.update()  # Atualiza a página para refletir os dados

    # 2. Modal personalizado para cadastro de professor
    nome_input = ft.TextField(label="Nome")
    dep_input = ft.TextField(label="Departamento")

    # Função para salvar novo professor
    def salvar(e):
        criar_professor(nome_input.value, dep_input.value)  # Chama service para criar professor
        container_modal.visible = False  # Fecha modal
        container_modal.update()
        carregar_dados()  # Recarrega tabela

    # Estrutura do modal
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
        visible=False,  # Inicialmente invisível
        bgcolor=ft.Colors.BLACK54,  # Fundo escurecido para simular modal
        expand=True
    )

    # Função para abrir modal
    def abrir_modal(e):
        container_modal.visible = True
        container_modal.update()

    # 3. Layout Final usando Stack (permite sobreposição do modal)
    layout = ft.Stack(
        controls=[
            ft.Column([
                ft.ElevatedButton("Novo Professor", on_click=abrir_modal),  # Botão para abrir modal
                tabela  # Tabela de professores
            ]),
            container_modal  # Modal sobreposto
        ],
        expand=True
    )

    # Carrega dados iniciais
    carregar_dados()
    return layout