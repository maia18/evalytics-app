import flet as ft
from utils.services.relatorio_service import calcular_medias_eixos
from utils.services.pdf_service import gerar_pdf_resultados

def TelaResultados(page: ft.Page):
    medias = calcular_medias_eixos()
    
    nomes_eixos = {
        1: "Organização Didático-Pedagógica",
        2: "Corpo Docente e Tutorial",
        3: "Infraestrutura"
    }

    def exportar_pdf(e):
        try:
            caminho = gerar_pdf_resultados(medias, nomes_eixos)
            page.snack_bar = ft.SnackBar(ft.Text(f"Sucesso! Relatório salvo como: {caminho}"))
            page.snack_bar.open = True
        except Exception as err:
            page.snack_bar = ft.SnackBar(ft.Text(f"Erro ao gerar PDF: {err}"))
            page.snack_bar.open = True
        page.update()

    cards_resultados = []
    for eixo_id, nota in medias.items():
        cor_barra = "green" if nota >= 3.5 else "orange" if nota >= 2.5 else "red"
        
        cards_resultados.append(
            ft.Card(
                content=ft.Container(
                    padding=20,
                    content=ft.Column([
                        ft.Text(nomes_eixos.get(eixo_id, f"Eixo {eixo_id}"), weight="bold", size=16),
                        ft.Row([
                            ft.Text("Desempenho", size=12),
                            ft.Text(f"{nota:.1f} / 5.0", weight="bold", size=12),
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ft.ProgressBar(value=nota/5, color=cor_barra, height=10, border_radius=5),
                    ])
                )
            )
        )

    return ft.Container(
        padding=20,
        content=ft.Column([
            ft.Text("Dashboard de Resultados", size=24, weight="bold"),
            ft.Divider(height=20),
            *cards_resultados,
            ft.Divider(height=20, color="transparent"),
            ft.ElevatedButton(
                "Exportar Relatório PDF", 
                icon=ft.Icons.PICTURE_AS_PDF,
                on_click=exportar_pdf
            )
        ], scroll=ft.ScrollMode.AUTO)
    )