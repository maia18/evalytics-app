import flet as ft

from utils.services.relatorio_service import calcular_medias_eixos
from models.relatorios.core.export_pdf import gerar_pdf_completo

# Limiares de classificação visual do desempenho (escala 0-5) para o semáforo de cores
LIMIAR_DESEMPENHO_BOM = 3.5
LIMIAR_DESEMPENHO_ALERTA = 2.5

NOMES_EIXOS: dict[int, str] = {1: "Organização Didático-Pedagógica", 2: "Corpo Docente e Tutorial", 3: "Infraestrutura"}

def _cor_desempenho(nota: float) -> str:
    """Classifica a nota em verde (bom), laranja (alerta) ou vermelho (crítico)."""
    if nota >= LIMIAR_DESEMPENHO_BOM: return ft.Colors.GREEN
    if nota >= LIMIAR_DESEMPENHO_ALERTA: return ft.Colors.ORANGE
    return ft.Colors.RED


def TelaResultados(page: ft.Page) -> ft.Container:
    """Dashboard Executivo de Resultados: indicadores semafóricos e exportação de dados.

    NOTA ARQUITETURAL: a exportação de PDF (`exportar_pdf`) roda de forma síncrona e pode
    bloquear a interface (congelar o Flet temporariamente) durante a geração do gráfico.
    """
    medias = calcular_medias_eixos()

    def exportar_pdf(e: ft.ControlEvent) -> None:
        """Aciona a geração do PDF, com feedback visual de carregamento no botão."""
        # Desabilita o botão para evitar cliques múltiplos acidentais
        e.control.text = "Gerando Relatório..."
        e.control.disabled = True
        page.update()

        # Executa o script de geração (que chama Plotly + FPDF)
        gerar_pdf_completo(page, medias, NOMES_EIXOS, semestre="2026.1")

        # Restaura o botão original após a geração concluir
        e.control.text = "Exportar Relatório PDF"
        e.control.disabled = False
        page.update()

    # Gera um Card contendo uma barra de progresso para cada Eixo dinamicamente
    cards_resultados = []
    for eixo_id, nota in medias.items():
        cor_barra = _cor_desempenho(nota)
        cards_resultados.append(
            ft.Card(
                elevation=2,
                content=ft.Container(
                    padding=20,
                    content=ft.Column(spacing=10, controls=[
                        ft.Text(NOMES_EIXOS.get(eixo_id, f"Eixo {eixo_id}"), weight="bold", size=16),
                        ft.Row([
                            ft.Text("Desempenho", size=12, color=ft.Colors.GREY),
                            ft.Text(f"{nota:.1f} / 5.0", weight="bold", size=14, color=cor_barra),
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ft.ProgressBar(value=nota / 5, color=cor_barra, height=10, border_radius=5),
                    ]),
                ),
            )
        )

    cabecalho = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.START,
        controls=[
            ft.Column(spacing=5, controls=[
                ft.Text("Dashboard de Resultados", size=28, weight="bold"),
                ft.Text("Acompanhe o desempenho institucional através dos eixos avaliados.", size=14, color=ft.Colors.GREY),
            ]),
            ft.ElevatedButton(
                "Exportar Relatório PDF", icon=ft.Icons.PICTURE_AS_PDF,
                bgcolor=ft.Colors.RED_700, color=ft.Colors.WHITE, height=45,
                on_click=exportar_pdf,
            ),
        ],
    )

    return ft.Container(padding=30, expand=True, content=ft.Column(expand=True, controls=[cabecalho, ft.Divider(height=20, color=ft.Colors.TRANSPARENT), ft.Column(expand=True, controls=cards_resultados)]))