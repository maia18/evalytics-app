# import flet as ft
# from utils.services.indicadores_service import listar_indicadores, atualizar_indicador

# def TelaIndicadores(page: ft.Page):
#     # Container mestre que será atualizado conforme o nível da navegação
#     container_mestre = ft.Container(expand=True)

#     # --- NÍVEL 1: Dashboard de Eixos ---
#     def TelaListaEixos():
#         # Carrega todos os indicadores e agrupa por categoria (eixo)
#         dados = listar_indicadores()
#         eixos_agrupados = {}
#         for ind in dados:
#             cat = ind.get("categoria", "Outros")
#             if cat not in eixos_agrupados:
#                 eixos_agrupados[cat] = []
#             eixos_agrupados[cat].append(ind)

#         # Lista de cards que representam cada eixo
#         lista_cards = [ft.Text("Gerenciar Indicadores", size=24, weight="bold")]
        
#         for nome, lista in eixos_agrupados.items():
#             lista_cards.append(
#                 ft.Container(
#                     content=ft.Card(
#                         content=ft.Container(
#                             padding=20,
#                             content=ft.ListTile(
#                                 leading=ft.Icon(ft.Icons.FOLDER, color="blue700"),
#                                 title=ft.Text(nome, weight="bold"),
#                                 subtitle=ft.Text(f"{len(lista)} indicadores"),
#                                 # Ao clicar, carrega os indicadores do eixo selecionado
#                                 on_click=lambda e, n=nome, l=lista: carregar_indicadores_do_eixo(n, l)
#                             )
#                         )
#                     ),
#                     width=800  # Mantém alinhamento e largura fixa
#                 )
#             )
#         return ft.Container(padding=20, content=ft.Column(lista_cards))

#     # --- NÍVEL 2: Lista de Indicadores dentro de um eixo ---
#     def carregar_indicadores_do_eixo(eixo_nome, indicadores):
#         lista = ft.Column([
#             ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: voltar_lista()),  # Voltar para lista de eixos
#             ft.Text(eixo_nome, size=24, weight="bold"),
#             # Cria um card para cada indicador
#             *[
#                 ft.Card(
#                     content=ft.ListTile(
#                         title=ft.Text(ind.get("nome", "Sem título")),
#                         trailing=ft.Icon(ft.Icons.EDIT),
#                         # Ao clicar, abre o editor do indicador
#                         on_click=lambda e, i=ind: carregar_editor(i, eixo_nome, indicadores)
#                     )
#                 )
#                 for ind in indicadores
#             ]
#         ], scroll=ft.ScrollMode.AUTO)

#         container_mestre.content = ft.Container(padding=20, content=lista)
#         container_mestre.update()

#     # --- NÍVEL 3: Editor de Indicador ---
#     def carregar_editor(ind, eixo_nome, indicadores_originais):
#         # Campos de edição
#         nome_f = ft.TextField(value=ind.get("nome", ""), label="Título do Indicador")
#         desc_f = ft.TextField(value=ind.get("descricao", ""), label="Descrição", multiline=True)
        
#         # Cria campos para os 5 critérios
#         crit_inputs = []
#         criterios = ind.get("criterios", {})
#         for i in range(1, 6):
#             crit_inputs.append(
#                 ft.TextField(
#                     value=criterios.get(str(i), ""), 
#                     label=f"Critério {i}", 
#                     multiline=True
#                 )
#             )

#         # Função de salvar alterações
#         def salvar(e):
#             # Aqui você pode chamar a função atualizar_indicador do seu service
#             # Exemplo: atualizar_indicador(ind['id'], nome_f.value, desc_f.value, {...})
#             page.snack_bar = ft.SnackBar(ft.Text("Alterações salvas!"))
#             page.snack_bar.open = True
#             page.update()

#         # Layout do editor
#         container_mestre.content = ft.Container(
#             padding=20,
#             content=ft.Column([
#                 ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: carregar_indicadores_do_eixo(eixo_nome, indicadores_originais)),
#                 ft.Text("Editando Indicador", size=20, weight="bold"),
#                 nome_f, desc_f, *crit_inputs,
#                 ft.ElevatedButton("Salvar Alterações", icon=ft.Icons.SAVE, on_click=salvar)
#             ], scroll=ft.ScrollMode.AUTO)
#         )
#         container_mestre.update()

#     # Função para voltar à lista de eixos
#     def voltar_lista():
#         container_mestre.content = TelaListaEixos()
#         container_mestre.update()

#     # Inicializa com a lista de eixos
#     container_mestre.content = TelaListaEixos()
#     return container_mestre