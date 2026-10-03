import flet as ft

from utils.services.relatorio_service import (
    calcular_medias_eixos,
)


LIMIAR_DESEMPENHO_BOM = 3.5
LIMIAR_DESEMPENHO_ALERTA = 2.5


NOMES_EIXOS: dict[int, str] = {
    1: "Organização Didático-Pedagógica",
    2: "Corpo Docente e Tutorial",
    3: "Infraestrutura",
}


def _cor_desempenho(nota: float) -> str:

    if nota >= LIMIAR_DESEMPENHO_BOM:
        return ft.Colors.GREEN

    if nota >= LIMIAR_DESEMPENHO_ALERTA:
        return ft.Colors.ORANGE

    return ft.Colors.RED


def _criar_card_eixo(
    eixo_id: int,
    nota: float | None,
) -> ft.Card:

    # ------------------------------------------------------
    # SEM DADOS
    # ------------------------------------------------------

    if nota is None:

        return ft.Card(
            elevation=2,
            content=ft.Container(
                padding=20,
                content=ft.Column(
                    spacing=10,
                    controls=[
                        ft.Text(
                            NOMES_EIXOS.get(
                                eixo_id,
                                f"Eixo {eixo_id}",
                            ),
                            weight="bold",
                            size=16,
                        ),
                        ft.Text(
                            "Sem dados disponíveis",
                            size=14,
                            color=ft.Colors.GREY_600,
                        ),
                        ft.Text(
                            "Não existem respostas para "
                            "este eixo nos filtros selecionados.",
                            size=12,
                            color=ft.Colors.GREY_500,
                        ),
                    ],
                ),
            ),
        )

    # ------------------------------------------------------
    # COM DADOS
    # ------------------------------------------------------

    cor_barra = _cor_desempenho(nota)

    return ft.Card(
        elevation=2,
        content=ft.Container(
            padding=20,
            content=ft.Column(
                spacing=10,
                controls=[
                    ft.Text(
                        NOMES_EIXOS.get(
                            eixo_id,
                            f"Eixo {eixo_id}",
                        ),
                        weight="bold",
                        size=16,
                    ),
                    ft.Row(
                        [
                            ft.Text(
                                "Desempenho",
                                size=12,
                                color=ft.Colors.GREY,
                            ),
                            ft.Text(
                                f"{nota:.1f} / 5.0",
                                weight="bold",
                                size=14,
                                color=cor_barra,
                            ),
                        ],
                        alignment=(
                            ft.MainAxisAlignment
                            .SPACE_BETWEEN
                        ),
                    ),
                    ft.ProgressBar(
                        value=nota / 5,
                        color=cor_barra,
                        height=10,
                        border_radius=5,
                    ),
                ],
            ),
        ),
    )


def TelaResultados(
    page: ft.Page,
) -> ft.Container:

    # ======================================================
    # ÁREA DOS CARDS
    # ======================================================

    cards_resultados = ft.Column(
        expand=True,
        spacing=15,
    )

    # ======================================================
    # ATUALIZA DASHBOARD
    # ======================================================

    def atualizar_dashboard(
        semestre: str | None = None,
        eixo: int | None = None,
    ) -> None:

        medias = calcular_medias_eixos(
            semestre=semestre,
            eixo=eixo,
        )

        cards_resultados.controls.clear()

        # --------------------------------------------------
        # Se um eixo específico foi selecionado,
        # mostramos somente esse eixo.
        # --------------------------------------------------

        if eixo is not None:

            cards_resultados.controls.append(
                _criar_card_eixo(
                    eixo,
                    medias.get(eixo),
                )
            )

        # --------------------------------------------------
        # Sem filtro de eixo:
        # mostramos os três eixos.
        # --------------------------------------------------

        else:

            for eixo_id in (1, 2, 3):

                cards_resultados.controls.append(
                    _criar_card_eixo(
                        eixo_id,
                        medias.get(eixo_id),
                    )
                )

        page.update()

    # ======================================================
    # CABEÇALHO
    # ======================================================

    cabecalho = ft.Column(
        spacing=5,
        controls=[
            ft.Text(
                "Dashboard de Resultados",
                size=28,
                weight="bold",
            ),
            ft.Text(
                "Acompanhe o desempenho institucional "
                "através dos eixos avaliados.",
                size=14,
                color=ft.Colors.GREY,
            ),
        ],
    )

    # ======================================================
    # CONTAINER PRINCIPAL
    # ======================================================

    dashboard = ft.Container(
        padding=30,
        expand=True,
        content=ft.Column(
            expand=True,
            controls=[
                cabecalho,
                ft.Divider(
                    height=20,
                    color=ft.Colors.TRANSPARENT,
                ),
                cards_resultados,
            ],
        ),
    )

    # ======================================================
    # PRIMEIRA CARGA
    # ======================================================

    atualizar_dashboard()

    # Permite que o orquestrador atualize o dashboard.
    dashboard.atualizar = atualizar_dashboard

    return dashboard