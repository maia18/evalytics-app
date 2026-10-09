import flet as ft
from components.core.constants.constants import CARD
from utils.services.relatorio.relatorio_service import (
    listar_semestres_disponiveis,
)

NOMES_EIXOS = {
    1: "Organização Didático-Pedagógica",
    2: "Corpo Docente e Tutorial",
    3: "Infraestrutura",
}

def criar_secao_filtros(
    layout,
    borda_container: ft.Border,
    page: ft.Page,
    ao_filtrar,
    ao_exportar_csv=None,
    ao_exportar_pdf=None,
) -> ft.Container:
    """
    Cria a seção de filtros dos relatórios.
        Os semestres são carregados diretamente das avaliações existentes no Firestore.
    """

    # ======================================================
    # SEMESTRES REAIS
    # ======================================================

    semestres = listar_semestres_disponiveis()

    opcoes_semestre = [
        ft.dropdown.Option(
            key="TODOS",
            text="Todos os semestres",
        )
    ]

    opcoes_semestre.extend(
        ft.dropdown.Option(
            key=semestre,
            text=semestre,
        )
        for semestre in semestres
    )

    dropdown_semestre = ft.Dropdown(
        label="Semestre",
        options=opcoes_semestre,
        value="TODOS",
        width=220,
        dense=True,
    )

    # ======================================================
    # EIXOS REAIS
    # ======================================================

    opcoes_eixo = [
        ft.dropdown.Option(
            key="TODOS",
            text="Todos os eixos",
        )
    ]

    opcoes_eixo.extend(
        ft.dropdown.Option(
            key=str(eixo_id),
            text=nome,
        )
        for eixo_id, nome in NOMES_EIXOS.items()
    )

    dropdown_eixo = ft.Dropdown(
        label="Eixo Avaliativo",
        options=opcoes_eixo,
        value="TODOS",
        width=280,
        dense=True,
    )

    # ======================================================
    # APLICAR FILTROS
    # ======================================================

    def aplicar_filtros(e=None):
        semestre = dropdown_semestre.value
        eixo = dropdown_eixo.value

        semestre_filtro = (
            None
            if semestre in (None, "", "TODOS")
            else semestre
        )

        eixo_filtro = (
            None
            if eixo in (None, "", "TODOS")
            else int(eixo)
        )

        ao_filtrar(
            semestre_filtro,
            eixo_filtro,
        )

    # ======================================================
    # LIMPAR FILTROS
    # ======================================================

    def limpar_filtros(e):
        dropdown_semestre.value = "TODOS"
        dropdown_eixo.value = "TODOS"

        ao_filtrar(
            None,
            None,
        )

        page.update()

    # ======================================================
    # BOTÕES
    # ======================================================

    botao_filtrar = ft.ElevatedButton(
        "Aplicar filtros",
        icon=ft.Icons.FILTER_ALT,
        bgcolor=ft.Colors.BLUE_700,
        color=ft.Colors.WHITE,
        on_click=aplicar_filtros,
    )

    botao_limpar = ft.OutlinedButton(
        "Limpar",
        icon=ft.Icons.CLEAR,
        on_click=limpar_filtros,
    )

    # ======================================================
    # LAYOUT
    # ======================================================

    return ft.Container(
        bgcolor=layout.cores[CARD],
        padding=20,
        border_radius=8,
        border=borda_container,
        content=ft.Column(
            spacing=15,
            controls=[
                ft.Row(
                    wrap=True,
                    spacing=10,
                    run_spacing=10,
                    controls=[
                        dropdown_semestre,
                        dropdown_eixo,
                        botao_filtrar,
                        botao_limpar,
                    ],
                ),
            ],
        ),
    )