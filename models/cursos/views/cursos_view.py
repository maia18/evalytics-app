# import flet as ft
# from utils.services.cursos_service import listar_cursos, criar_curso

# def TelaCursos(page: ft.Page, on_avaliar):
        
#     # 1. Tabela de Cursos (com coluna de ações)
#     tabela = ft.DataTable(
#         columns=[
#             ft.DataColumn(ft.Text("Nome do Curso", weight="bold")),
#             ft.DataColumn(ft.Text("Modalidade", weight="bold")),
#             ft.DataColumn(ft.Text("Status", weight="bold")),
#             ft.DataColumn(ft.Text("Ações", weight="bold")),  # Nova coluna para botões
#         ],
#         rows=[]
#     )

#     # 2. Função disparada ao clicar em "Avaliar"
#     def iniciar_avaliacao(curso):
#         # Chama a função recebida como parâmetro para iniciar avaliação do curso
#         on_avaliar(curso)

#     # 3. Função que carrega os dados e constrói as linhas da tabela
#     def carregar_dados():
#         tabela.rows.clear()  # Limpa as linhas antes de recarregar
#         for curso in listar_cursos():
#             tabela.rows.append(ft.DataRow(cells=[
#                 ft.DataCell(ft.Text(curso.get("nome", "-"))),  # Nome do curso
#                 ft.DataCell(ft.Text(curso.get("modalidade", "-"))),  # Modalidade
#                 ft.DataCell(ft.Text("Ativo" if curso.get("ativo", True) else "Inativo")),  # Status
                
#                 # Botão de Avaliar dentro da tabela
#                 ft.DataCell(
#                     ft.ElevatedButton(
#                         "Avaliar",
#                         icon=ft.Icons.FACT_CHECK,
#                         style=ft.ButtonStyle(bgcolor="blue700", color="white"),
#                         # Lambda garante que o botão saiba qual curso está associado
#                         on_click=lambda e, c=curso: iniciar_avaliacao(c)
#                     )
#                 )
#             ]))
#         page.update()  # Atualiza a página para refletir os novos dados

#     # 4. Modal de Cadastro de Curso
#     nome_input = ft.TextField(label="Nome do Curso (Ex: Engenharia de Telecomunicações)", width=350)
#     mod_input = ft.Dropdown(
#         label="Modalidade",
#         width=350,
#         options=[
#             ft.dropdown.Option("Presencial"),
#             ft.dropdown.Option("EAD"),
#             ft.dropdown.Option("Híbrido")
#         ]
#     )

#     # Função para fechar o modal
#     def fechar_modal(e):
#         container_modal.visible = False
#         container_modal.update()

#     # Função para salvar novo curso
#     def salvar(e):
#         if nome_input.value and mod_input.value:
#             criar_curso(nome_input.value, mod_input.value)  # Cria curso via serviço
#             nome_input.value = ""  # Limpa campo
#             mod_input.value = None  # Reseta dropdown
#             fechar_modal(e)  # Fecha modal
#             carregar_dados()  # Recarrega tabela

#     # Estrutura do modal
#     container_modal = ft.Container(
#         content=ft.Card(
#             content=ft.Container(
#                 padding=30,
#                 content=ft.Column([
#                     ft.Text("Cadastrar Novo Curso", size=20, weight="bold"),
#                     ft.Divider(height=10, color="transparent"),
#                     nome_input, 
#                     mod_input,
#                     ft.Divider(height=10, color="transparent"),
#                     ft.Row([
#                         ft.TextButton("Cancelar", on_click=fechar_modal),
#                         ft.ElevatedButton("Salvar", on_click=salvar, style=ft.ButtonStyle(bgcolor="green700", color="white"))
#                     ], alignment=ft.MainAxisAlignment.END)
#                 ], tight=True)
#             )
#         ),
#         visible=False,  # Inicialmente invisível
#         bgcolor=ft.Colors.BLACK54,  # Fundo escuro para destacar modal
#         expand=True
#     )

#     # Função para abrir modal
#     def abrir_modal(e):
#         container_modal.visible = True
#         container_modal.update()

#     # 5. Layout final da tela
#     layout = ft.Stack(
#         controls=[
#             ft.Column([
#                 ft.Row([
#                     ft.Text("Gerenciar Cursos", size=24, weight="bold"),
#                     ft.ElevatedButton(
#                         "Novo Curso", 
#                         icon=ft.Icons.ADD, 
#                         style=ft.ButtonStyle(bgcolor="green700", color="white"), 
#                         on_click=abrir_modal
#                     )
#                 ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
#                 ft.Divider(height=20, color="transparent"),
#                 tabela  # Tabela de cursos
#             ]),
#             container_modal  # Modal sobreposto
#         ],
#         expand=True
#     )

#     # Carrega dados iniciais
#     carregar_dados()
#     return layout