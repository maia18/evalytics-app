from typing import Callable

import flet as ft

from components.layout.responsive.responsive import ResponsiveLayout
from database.services.firestore_courses import obter_cursos_db
from models.formulario.core.form_controller import FormularioController


def ViewFormulario(
    page: ft.Page,
    mudar_tela: Callable[[str], None],
) -> ft.View:
    """
    Constrói a tela de Avaliação Institucional.

    Fluxo:
        1. Seleção do curso;
        2. Definição do curso no controller;
        3. Exibição das perguntas;
        4. Finalização e persistência da avaliação.
    """

    layout = ResponsiveLayout(
        page,
        titulo_pagina="Avaliação Institucional",
        subtitulo=(
            "Preencha o formulário abaixo para contribuir "
            "com a melhoria contínua."
        ),
        mudar_tela=mudar_tela,
    )

    # ==========================================================
    # ÁREA DINÂMICA
    # ==========================================================

    area_dinamica_conteudo = ft.Column(
        expand=True,
        spacing=25,
        animate_opacity=ft.Animation(
            300,
            ft.AnimationCurve.EASE_IN_OUT,
        ),
    )

    area_central = ft.Container(
        expand=True,
        padding=ft.Padding.only(
            top=10,
            bottom=30,
            right=20,
        ),
        content=area_dinamica_conteudo,
    )

    # ==========================================================
    # CONTROLLER
    # ==========================================================

    controller = FormularioController(
        page=page,
        mudar_tela=mudar_tela,
        area_dinamica=area_dinamica_conteudo,
        area_central=area_central,
    )

    # ==========================================================
    # SELEÇÃO DO CURSO
    # ==========================================================

    def iniciar_avaliacao(e: ft.ControlEvent) -> None:
        curso_id = dropdown_curso.value

        if not curso_id:
            page.show_dialog(
                ft.SnackBar(
                    content=ft.Text(
                        "Selecione um curso para iniciar a avaliação."
                    ),
                    bgcolor=ft.Colors.RED_700,
                )
            )
            return

        curso_selecionado = next(
            (
                curso
                for curso in cursos
                if curso.get("id") == curso_id
            ),
            None,
        )

        if curso_selecionado is None:
            page.show_dialog(
                ft.SnackBar(
                    content=ft.Text(
                        "Não foi possível localizar o curso selecionado."
                    ),
                    bgcolor=ft.Colors.RED_700,
                )
            )
            return

        curso_nome = curso_selecionado.get("nome", "")

        controller.definir_curso(
            curso_id=curso_id,
            curso_nome=curso_nome,
        )

        controller.atualizar_renderizacao()

    try:
        cursos = obter_cursos_db()
    except Exception:
        cursos = []

    # ==========================================================
    # DROPDOWN DE CURSOS
    # ==========================================================

    dropdown_curso = ft.Dropdown(
        label="Curso",
        hint_text="Selecione o curso que será avaliado",
        options=[
            ft.DropdownOption(
                key=curso["id"],
                text=curso.get("nome", "Curso sem nome"),
            )
            for curso in cursos
            if curso.get("id")
        ],
        width=500,
    )

    # ==========================================================
    # TELA INICIAL DO FORMULÁRIO
    # ==========================================================

    if cursos:
        conteudo_selecao = ft.Container(
            expand=True,
            padding=30,
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            border=ft.Border.all(
                1,
                ft.Colors.GREY_200,
            ),
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.Colors.BLACK12,
                offset=ft.Offset(0, 4),
            ),
            content=ft.Column(
                spacing=20,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Icon(
                        ft.Icons.SCHOOL_OUTLINED,
                        size=60,
                        color=ft.Colors.BLUE_700,
                    ),
                    ft.Text(
                        "Iniciar Avaliação",
                        size=24,
                        weight="bold",
                        color=ft.Colors.BLACK87,
                    ),
                    ft.Text(
                        "Selecione o curso que será avaliado.",
                        size=14,
                        color=ft.Colors.BLACK54,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Container(height=5),
                    dropdown_curso,
                    ft.ElevatedButton(
                        "Iniciar avaliação",
                        icon=ft.Icons.ARROW_FORWARD,
                        on_click=iniciar_avaliacao,
                    ),
                ],
            ),
        )

        area_dinamica_conteudo.controls = [
            conteudo_selecao
        ]

    else:
        area_dinamica_conteudo.controls = [
            ft.Container(
                padding=30,
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=15,
                    controls=[
                        ft.Icon(
                            ft.Icons.INFO_OUTLINE,
                            size=50,
                            color=ft.Colors.ORANGE_700,
                        ),
                        ft.Text(
                            "Nenhum curso cadastrado",
                            size=22,
                            weight="bold",
                            color=ft.Colors.BLACK87,
                        ),
                        ft.Text(
                            "Cadastre pelo menos um curso antes "
                            "de iniciar uma avaliação.",
                            size=14,
                            color=ft.Colors.BLACK54,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.ElevatedButton(
                            "Ir para Cursos",
                            icon=ft.Icons.ARROW_FORWARD,
                            on_click=lambda _: mudar_tela("/cursos"),
                        ),
                    ],
                ),
            )
        ]

    # ==========================================================
    # FINALIZAÇÃO DA VIEW
    # ==========================================================

    layout.add_content(area_central)

    return layout.criar_view("/formulario")