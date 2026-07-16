import flet as ft
from components.layout.responsive.responsive import ResponsiveLayout
from components.core.theme.theme import AppColors
from database.services.firestore_courses import obter_cursos_db

from models.cursos.widgets.tabela_cursos import criar_linha_curso
from models.cursos.widgets.stats_cards import criar_stats_card
from models.cursos.modals.modal_add import criar_modal_add
from models.cursos.modals.modal_edit import criar_modal_edit

from components.core.constants import *

def ViewCursos(page: ft.Page, mudar_tela):
    layout = ResponsiveLayout(
        page,
        titulo_pagina="Gestão de Cursos",
        subtitulo="Adicione, edite ou remova os cursos da instituição.",
        mudar_tela=mudar_tela
    )

    # === Campos de formulário ===
    campos_add = {
        "nome": ft.TextField(label="Nome do Curso", border_color="blue200", dense=True),
        "departamento": ft.TextField(label="Departamento", border_color="blue200", dense=True),
        "coordenador": ft.TextField(label="Coordenador Responsável", border_color="blue200", dense=True),
    }
    campos_edit = {
        "nome": ft.TextField(label="Nome do Curso", border_color="blue200", dense=True),
        "departamento": ft.TextField(label="Departamento", border_color="blue200", dense=True),
        "coordenador": ft.TextField(label="Coordenador Responsável", border_color="blue200", dense=True),
    }
    estado = {"linha_atual": None, "id_firebase": None}

    # === Tabela de cursos ===
    tabela_cursos = ft.DataTable(
        heading_row_color="blue50",
        columns=[
            ft.DataColumn(ft.Text("Código", weight="bold")),
            ft.DataColumn(ft.Text("Nome do Curso", weight="bold")),
            ft.DataColumn(ft.Text("Departamento", weight="bold")),
            ft.DataColumn(ft.Text("Coordenador", weight="bold")),
            ft.DataColumn(ft.Text("Ações", weight="bold")),
        ],
        rows=[]
    )

    linha_stats = ft.Row(
        spacing=20,
        controls=[
            criar_stats_card("Total de Cursos", "0", layout.cores["TEXTO_PRINCIPAL"]),
            criar_stats_card("Cursos Ativos", "0", layout.cores["TEXTO_PRINCIPAL"]),
            criar_stats_card("Departamentos", "0", layout.cores["TEXTO_PRINCIPAL"]),
        ]
    )

    def atualizar_interface():
        total_cursos = str(len(tabela_cursos.rows))
        
        departamentos_unicos = {
            linha.cells[2].content.value.strip()
            for linha in tabela_cursos.rows
            if hasattr(linha.cells[2].content, 'value') and linha.cells[2].content.value.strip()
        }
        total_deptos = str(len(departamentos_unicos))

        linha_stats.controls = [
            criar_stats_card("Total de Cursos", total_cursos, layout.cores["TEXTO_PRINCIPAL"]),
            criar_stats_card("Cursos Ativos", "0", layout.cores["TEXTO_PRINCIPAL"]),
            criar_stats_card("Departamentos", total_deptos, layout.cores["TEXTO_PRINCIPAL"]),
        ]
        
        page.update()

    # === Modais ===
    abrir_modal_add = criar_modal_add(page, tabela_cursos, criar_linha_curso, atualizar_interface, campos_add)
    modal_edit = criar_modal_edit(page, estado, campos_edit, atualizar_interface)

    # === Carregar cursos iniciais ===
    def carregar_cursos_iniciais():
        cursos = obter_cursos_db()
        tabela_cursos.rows.clear()
        for c in cursos:
            linha = criar_linha_curso(
                page,
                tabela_cursos,
                atualizar_interface,
                modal_edit,
                campos_edit,
                estado,
                c.get("id"),
                c.get("codigo", "S/C"),
                c.get("nome", ""),
                c.get("departamento", ""),
                c.get("coordenador", "")
            )
            tabela_cursos.rows.append(linha)
        atualizar_interface()

    carregar_cursos_iniciais()

    # === Conteúdo principal ===
    conteudo = ft.Column(
        expand=True,
        spacing=25,
        scroll=ft.ScrollMode.AUTO,
        controls=[
            ft.Row(
                alignment=ft.MainAxisAlignment.END,
                controls=[
                    ft.ElevatedButton(
                        "Novo curso",
                        icon=ft.Icons.ADD,
                        bgcolor=PRIMARIA,
                        color="white",
                        on_click=abrir_modal_add
                    )
                ]
            ),
            linha_stats,
            ft.Container(
                bgcolor=layout.cores["CARD"],
                padding=30,
                border_radius=8,
                content=ft.Column(
                    spacing=20,
                    controls=[
                        ft.Text("Lista de Cursos", size=16, weight="bold", color=layout.cores["TEXTO_PRINCIPAL"]),
                        tabela_cursos if tabela_cursos.rows else ft.Text("Nenhum curso cadastrado ainda.", color="grey", size=14)
                    ]
                )
            )
        ]
    )

    layout.add_content(conteudo)
    return layout.criar_view("/cursos")
