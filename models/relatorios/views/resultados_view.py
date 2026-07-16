# import flet as ft
# from utils.services.relatorio_service import calcular_medias_eixos
# from utils.services.pdf_service import gerar_pdf_resultados

# def TelaResultados(page: ft.Page):
#     # Calcula as médias de cada eixo usando o service
#     medias = calcular_medias_eixos()
    
#     # Dicionário para mapear IDs dos eixos para nomes legíveis
#     nomes_eixos = {
#         1: "Organização Didático-Pedagógica",
#         2: "Corpo Docente e Tutorial",
#         3: "Infraestrutura"
#     }

#     # Função para exportar resultados em PDF
#     def exportar_pdf(e):
#         try:
#             caminho = gerar_pdf_resultados(medias, nomes_eixos)  # Gera PDF via service
#             page.snack_bar = ft.SnackBar(ft.Text(f"Sucesso! Relatório salvo como: {caminho}"))
#             page.snack_bar.open = True
#         except Exception as err:
#             # Caso ocorra erro na geração
#             page.snack_bar = ft.SnackBar(ft.Text(f"Erro ao gerar PDF: {err}"))
#             page.snack_bar.open = True
#         page.update()

#     # Lista de cards para exibir resultados de cada eixo
#     cards_resultados = []
#     for eixo_id, nota in medias.items():
#         # Define cor da barra de progresso conforme desempenho
#         cor_barra = "green" if nota >= 3.5 else "orange" if nota >= 2.5 else "red"
        
#         # Cria card com título, nota e barra de progresso
#         cards_resultados.append(
#             ft.Card(
#                 content=ft.Container(
#                     padding=20,
#                     content=ft.Column([
#                         ft.Text(nomes_eixos.get(eixo_id, f"Eixo {eixo_id}"), weight="bold", size=16),
#                         ft.Row([
#                             ft.Text("Desempenho", size=12),
#                             ft.Text(f"{nota:.1f} / 5.0", weight="bold", size=12),
#                         ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
#                         ft.ProgressBar(value=nota/5, color=cor_barra, height=10, border_radius=5),
#                     ])
#                 )
#             )
#         )

#     # Layout final da tela
#     return ft.Container(
#         padding=20,
#         content=ft.Column([
#             ft.Text("Dashboard de Resultados", size=24, weight="bold"),
#             ft.Divider(height=20),
#             *cards_resultados,  # Insere todos os cards de resultados
#             ft.Divider(height=20, color="transparent"),
#             ft.ElevatedButton(
#                 "Exportar Relatório PDF", 
#                 icon=ft.Icons.PICTURE_AS_PDF,
#                 on_click=exportar_pdf
#             )
#         ], scroll=ft.ScrollMode.AUTO)
#     )