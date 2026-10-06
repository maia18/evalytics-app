from typing import Callable

import flet as ft

from components.core.constants.constants import (
    TEXTO_PRINCIPAL,
    TEXTO_SECUNDARIO,
    COR_PRIMARIA,
    BORDA,
    AVISO,
    CARD,
)
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

    Quando a tela é reconstruída, por exemplo durante a troca
    de tema, o FormularioController existente é reutilizado para
    preservar o estado da avaliação em andamento.
    """

    # ==========================================================
    # VERIFICA SE JÁ EXISTE UM CONTROLLER
    # ==========================================================

    controller_existente = getattr(
        page,
        "_formulario_controller",
        None,
    )

    # ==========================================================
    # LAYOUT
    # ==========================================================

    layout = ResponsiveLayout(
        page,
        titulo_pagina="Avaliação Institucional",
        subtitulo=(
            "Preencha o formulário abaixo para contribuir "
            "com a melhoria contínua."
        ),
        mudar_tela=mudar_tela,
    )

    cores = layout.cores

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

    if controller_existente is None:

        # ------------------------------------------------------
        # PRIMEIRA ENTRADA NO FORMULÁRIO
        # ------------------------------------------------------

        controller = FormularioController(
            page=page,
            mudar_tela=mudar_tela,
            area_dinamica=area_dinamica_conteudo,
            area_central=area_central,
            cores=layout.cores,
        )

        page._formulario_controller = controller

    else:

        # ------------------------------------------------------
        # REUTILIZA O CONTROLLER EXISTENTE
        #
        # Isso é importante quando a rota /formulario é
        # reconstruída durante a troca de tema.
        # ------------------------------------------------------

        controller = controller_existente

        controller.page = page
        controller.mudar_tela = mudar_tela
        controller.area_dinamica = area_dinamica_conteudo
        controller.area_central = area_central
        controller.cores = layout.cores

    # ==========================================================
    # CARREGA OS CURSOS
    # ==========================================================

    try:
        cursos = obter_cursos_db()
    except Exception:
        cursos = []

    # ==========================================================
    # FUNÇÃO — INICIAR AVALIAÇÃO
    # ==========================================================

    def iniciar_avaliacao(
        e: ft.ControlEvent,
    ) -> None:

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

        curso_nome = curso_selecionado.get(
            "nome",
            "",
        )

        # ------------------------------------------------------
        # DEFINE O CURSO NO CONTROLLER
        # ------------------------------------------------------

        controller.definir_curso(
            curso_id=curso_id,
            curso_nome=curso_nome,
        )

        # ------------------------------------------------------
        # MOSTRA A PRIMEIRA PERGUNTA
        # ------------------------------------------------------

        controller.atualizar_renderizacao()

    # ==========================================================
    # DROPDOWN DE CURSOS
    # ==========================================================

    dropdown_curso = ft.Dropdown(
        label="Curso",
        hint_text="Selecione o curso que será avaliado",
        options=[
            ft.DropdownOption(
                key=curso["id"],
                text=curso.get(
                    "nome",
                    "Curso sem nome",
                ),
            )
            for curso in cursos
            if curso.get("id")
        ],
        width=500,
        color=cores[TEXTO_PRINCIPAL],
        border_color=cores[BORDA],
        label_style=ft.TextStyle(
            color=cores[TEXTO_SECUNDARIO],
        ),
        hint_style=ft.TextStyle(
            color=cores[TEXTO_SECUNDARIO],
        ),
    )

    # ==========================================================
    # CASO 1 — JÁ EXISTE UMA AVALIAÇÃO EM ANDAMENTO
    # ==========================================================

    if (
        controller.curso_id
        and controller.curso_nome
    ):

        # ------------------------------------------------------
        # NÃO MOSTRA NOVAMENTE A SELEÇÃO DO CURSO.
        #
        # Isso acontece, por exemplo, quando o usuário troca
        # o tema claro/escuro durante uma avaliação.
        #
        # O controller mantém:
        #
        # - curso_id
        # - curso_nome
        # - índice da pergunta
        # - respostas
        # - justificativas
        # ------------------------------------------------------

        controller.atualizar_renderizacao()

    # ==========================================================
    # CASO 2 — PRIMEIRA ENTRADA E EXISTEM CURSOS
    # ==========================================================

    elif cursos:

        conteudo_selecao = ft.Container(
            expand=True,
            padding=30,
            bgcolor=cores[CARD],
            border_radius=12,
            border=ft.Border.all(
                1,
                cores[BORDA],
            ),
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=(
                    "#00000033"
                    if not layout.dark_mode
                    else "#00000066"
                ),
                offset=ft.Offset(0, 4),
            ),
            content=ft.Column(
                spacing=20,
                horizontal_alignment=(
                    ft.CrossAxisAlignment.CENTER
                ),
                controls=[
                    ft.Icon(
                        ft.Icons.SCHOOL_OUTLINED,
                        size=60,
                        color=cores[COR_PRIMARIA],
                    ),

                    ft.Text(
                        "Iniciar Avaliação",
                        size=24,
                        weight="bold",
                        color=cores[TEXTO_PRINCIPAL],
                    ),

                    ft.Text(
                        "Selecione o curso que será avaliado.",
                        size=14,
                        color=cores[TEXTO_SECUNDARIO],
                        text_align=ft.TextAlign.CENTER,
                    ),

                    ft.Container(
                        height=5,
                    ),

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

    # ==========================================================
    # CASO 3 — NÃO EXISTEM CURSOS
    # ==========================================================

    else:

        area_dinamica_conteudo.controls = [
            ft.Container(
                padding=30,
                content=ft.Column(
                    horizontal_alignment=(
                        ft.CrossAxisAlignment.CENTER
                    ),
                    spacing=15,
                    controls=[
                        ft.Icon(
                            ft.Icons.INFO_OUTLINE,
                            size=50,
                            color=cores[AVISO],
                        ),

                        ft.Text(
                            "Nenhum curso cadastrado",
                            size=22,
                            weight="bold",
                            color=cores[TEXTO_PRINCIPAL],
                        ),

                        ft.Text(
                            "Cadastre pelo menos um curso antes "
                            "de iniciar uma avaliação.",
                            size=14,
                            color=cores[TEXTO_SECUNDARIO],
                            text_align=ft.TextAlign.CENTER,
                        ),

                        ft.ElevatedButton(
                            "Ir para Cursos",
                            icon=ft.Icons.ARROW_FORWARD,
                            on_click=lambda _: mudar_tela(
                                "/cursos"
                            ),
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