import flet as ft
from utils.services.relatorio.relatorio_service import calcular_medias_eixos

# Importação dos componentes visuais isolados
from .dashboard_cards import criar_card_eixo

def TelaResultados(page: ft.Page) -> ft.Container:
    """Renderiza a interface principal do dashboard de resultados."""

    # ======================================================
    # ÁREA DOS CARDS
    # ======================================================
    cards_resultados = ft.Column(
        expand=True,
        spacing=15,
    )

    # ======================================================
    # ATUALIZA DASHBOARD (CONTROLLER LOGIC)
    # ======================================================
    def atualizar_dashboard(semestre: str | None = None, eixo: int | None = None) -> None:
        medias = calcular_medias_eixos(semestre=semestre, eixo=eixo)
        cards_resultados.controls.clear()

        # Renderiza apenas o eixo selecionado ou todos se não houver filtro
        if eixo is not None:
            cards_resultados.controls.append(criar_card_eixo(eixo, medias.get(eixo)))
        else:
            for eixo_id in (1, 2, 3):
                cards_resultados.controls.append(
                    criar_card_eixo(eixo_id, medias.get(eixo_id))
                )

        page.update()

    # ======================================================
    # CABEÇALHO E CONTAINER PRINCIPAL
    # ======================================================
    cabecalho = ft.Column(
        spacing=5,
        controls=[
            ft.Text("Dashboard de Resultados", size=28, weight="bold"),
            ft.Text(
                "Acompanhe o desempenho institucional através dos eixos avaliados.",
                size=14,
                color=ft.Colors.GREY,
            ),
        ],
    )

    dashboard = ft.Container(
        padding=30,
        expand=True,
        content=ft.Column(
            expand=True,
            controls=[
                cabecalho,
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                cards_resultados,
            ],
        ),
    )

    # ======================================================
    # INICIALIZAÇÃO
    # ======================================================
    atualizar_dashboard()
    
    # Permite que um orquestrador pai atualize o dashboard externamente
    dashboard.atualizar = atualizar_dashboard

    return dashboard