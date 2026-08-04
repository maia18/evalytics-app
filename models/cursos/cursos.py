from typing import Callable

import flet as ft

from components.layout.responsive.responsive import ResponsiveLayout
from components.core.constants.constants import COR_PRIMARIA, TEXTO_PRINCIPAL, CARD

from models.cursos.widgets.tabela_cursos import ContextoTabelaCursos
from models.cursos.widgets.stats_cards import criar_stats_card
from models.cursos.modals.modal_add import criar_modal_add
from models.cursos.modals.modal_edit import criar_modal_edit

# Novas importações das lógicas e componentes extraídos
from models.cursos.widgets.campos_curso import criar_campos_formulario_curso
from models.cursos.core.cursos_controller import atualizar_estatisticas, carregar_cursos_iniciais

def ViewCursos(page: ft.Page, mudar_tela: Callable[[str], None]) -> ft.View:
    """Renderiza a tela completa de Gestão de Cursos, instanciando layouts, formulários e tabela de dados."""
    layout = ResponsiveLayout(
        page,
        titulo_pagina="Gestão de Cursos",
        subtitulo="Adicione, edite ou remova os cursos da instituição.",
        mudar_tela=mudar_tela,
    )

    # Cria dois conjuntos independentes de campos via factory externa
    campos_add = criar_campos_formulario_curso()
    campos_edit = criar_campos_formulario_curso()

    # Estado compartilhado
    estado = {"linha_atual": None, "id_firebase": None}

    # Estrutura da Tabela principal
    tabela_cursos = ft.DataTable(
        heading_row_color=ft.Colors.BLUE_50,
        columns=[
            ft.DataColumn(ft.Text("Código", weight="bold", color=ft.Colors.BLACK)),
            ft.DataColumn(ft.Text("Nome do Curso", weight="bold", color=ft.Colors.BLACK)),
            ft.DataColumn(ft.Text("Departamento", weight="bold", color=ft.Colors.BLACK)),
            ft.DataColumn(ft.Text("Coordenador", weight="bold", color=ft.Colors.BLACK)),
            ft.DataColumn(ft.Text("Ações", weight="bold", color=ft.Colors.BLACK)),
        ],
        rows=[],
    )

    # Linha dos três indicadores numéricos
    linha_stats = ft.Row(
        spacing=20,
        controls=[
            criar_stats_card("Total de Cursos", "0", layout.cores[TEXTO_PRINCIPAL]),
            criar_stats_card("Cursos Ativos", "0", layout.cores[TEXTO_PRINCIPAL]),
            criar_stats_card("Departamentos", "0", layout.cores[TEXTO_PRINCIPAL]),
        ],
    )

    # Wrapper que envelopa os parâmetros necessários para repassar a função de forma limpa como callback
    def wrapper_atualizar_interface() -> None:
        atualizar_estatisticas(page, tabela_cursos, linha_stats, layout.cores)

    # === Inicialização dos Modais e Contextos ===
    modal_edit = criar_modal_edit(page, estado, campos_edit, wrapper_atualizar_interface)

    contexto_tabela = ContextoTabelaCursos(
        page=page,
        tabela_cursos=tabela_cursos,
        atualizar_interface=wrapper_atualizar_interface,
        modal_editar=modal_edit,
        campos_edit=campos_edit,
        estado=estado,
    )

    abrir_modal_add = criar_modal_add(contexto_tabela, campos_add)

    # Executa a carga antes da tela terminar de ser desenhada delegando ao Controller
    carregar_cursos_iniciais(contexto_tabela, tabela_cursos, wrapper_atualizar_interface)

    # Estrutura visual final
    conteudo = ft.Column(
        expand=True,
        spacing=25,
        scroll=ft.ScrollMode.AUTO,
        controls=[
            ft.Row(
                alignment=ft.MainAxisAlignment.END,
                controls=[
                    ft.ElevatedButton(
                        "Novo curso", icon=ft.Icons.ADD, bgcolor=COR_PRIMARIA, color=ft.Colors.WHITE,
                        on_click=abrir_modal_add,
                    )
                ],
            ),
            linha_stats,
            ft.Container(
                bgcolor=layout.cores[CARD], padding=30, border_radius=8,
                content=ft.Column(
                    spacing=20,
                    controls=[
                        ft.Text("Lista de Cursos", size=16, weight="bold", color=ft.Colors.BLACK),
                        tabela_cursos if tabela_cursos.rows else ft.Text("Nenhum curso cadastrado ainda.", color=ft.Colors.GREY, size=14),
                    ],
                ),
            ),
        ],
    )

    layout.add_content(conteudo)
    return layout.criar_view("/cursos")