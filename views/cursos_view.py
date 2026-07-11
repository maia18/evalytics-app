import flet as ft
from utils.services.cursos_service import listar_cursos, criar_curso

def TelaCursos(page: ft.Page, on_avaliar):
        
    # 1. Tabela de Cursos (AGORA COM A COLUNA DE AÇÕES)
    tabela = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Nome do Curso", weight="bold")),
            ft.DataColumn(ft.Text("Modalidade", weight="bold")),
            ft.DataColumn(ft.Text("Status", weight="bold")),
            ft.DataColumn(ft.Text("Ações", weight="bold")), # NOVA COLUNA
        ],
        rows=[]
    )

    # 2. Função provisória que será disparada ao clicar em "Avaliar"
    def iniciar_avaliacao(curso):
        on_avaliar(curso)

    # 3. Função que carrega os dados e constrói as linhas
    def carregar_dados():
        tabela.rows.clear()
        for curso in listar_cursos():
            tabela.rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Text(curso.get("nome", "-"))),
                ft.DataCell(ft.Text(curso.get("modalidade", "-"))),
                ft.DataCell(ft.Text("Ativo" if curso.get("ativo", True) else "Inativo")),
                
                # O NOVO BOTÃO DE AVALIAR
                ft.DataCell(
                    ft.ElevatedButton(
                        "Avaliar",
                        icon=ft.Icons.FACT_CHECK,
                        style=ft.ButtonStyle(bgcolor="blue700", color="white"),
                        # O 'lambda' garante que o botão lembre de qual curso ele pertence
                        on_click=lambda e, c=curso: iniciar_avaliacao(c)
                    )
                )
            ]))
        page.update()

    # 4. O Modal Customizado de Cadastro (mantido igual)
    nome_input = ft.TextField(label="Nome do Curso (Ex: Engenharia de Telecomunicações)", width=350)
    mod_input = ft.Dropdown(
        label="Modalidade",
        width=350,
        options=[
            ft.dropdown.Option("Presencial"),
            ft.dropdown.Option("EAD"),
            ft.dropdown.Option("Híbrido")
        ]
    )

    def fechar_modal(e):
        container_modal.visible = False
        container_modal.update()

    def salvar(e):
        if nome_input.value and mod_input.value:
            criar_curso(nome_input.value, mod_input.value)
            nome_input.value = ""
            mod_input.value = None
            fechar_modal(e)
            carregar_dados()

    container_modal = ft.Container(
        content=ft.Card(
            content=ft.Container(
                padding=30,
                content=ft.Column([
                    ft.Text("Cadastrar Novo Curso", size=20, weight="bold"),
                    ft.Divider(height=10, color="transparent"),
                    nome_input, 
                    mod_input,
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

    # 5. Montagem do Layout Final
    layout = ft.Stack(
        controls=[
            ft.Column([
                ft.Row([
                    ft.Text("Gerenciar Cursos", size=24, weight="bold"),
                    ft.ElevatedButton("Novo Curso", icon=ft.Icons.ADD, style=ft.ButtonStyle(bgcolor="green700", color="white"), on_click=abrir_modal)
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