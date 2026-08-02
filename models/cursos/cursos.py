from typing import Callable

import flet as ft

from components.layout.responsive.responsive import ResponsiveLayout
from database.services.firestore_courses import obter_cursos_db

from models.cursos.widgets.tabela_cursos import ContextoTabelaCursos, criar_linha_curso
from models.cursos.widgets.stats_cards import criar_stats_card
from models.cursos.modals.modal_add import criar_modal_add
from models.cursos.modals.modal_edit import criar_modal_edit

from components.core.constants.constants import (
    COR_PRIMARIA, 
    TEXTO_PRINCIPAL, 
    CARD,
)

def _criar_campos_formulario_curso() -> dict[str, ft.TextField]:
    """Cria um novo conjunto de campos de formulário para cadastro/edição de curso.

    NOTA ARQUITETURAL: Uma função separada garante instâncias próprias de TextField por chamada: 
        compartilhar os mesmos widgets entre os formulários de adicionar e editar faria o texto digitado em um vazar para o outro.
    """
    return {
        # 'dense=True' diminui a altura interna do campo, deixando o formulário mais compacto
        "nome": ft.TextField(label="Nome do Curso", border_color=ft.Colors.BLUE_200, dense=True),
        "departamento": ft.TextField(label="Departamento", border_color=ft.Colors.BLUE_200, dense=True),
        "coordenador": ft.TextField(label="Coordenador Responsável", border_color=ft.Colors.BLUE_200, dense=True),
    }

def ViewCursos(page: ft.Page, mudar_tela: Callable[[str], None]) -> ft.View:
    """Renderiza a tela completa de Gestão de Cursos, instanciando layouts, formulários e tabela de dados."""
    layout = ResponsiveLayout(
        page,
        titulo_pagina="Gestão de Cursos",
        subtitulo="Adicione, edite ou remova os cursos da instituição.",
        mudar_tela=mudar_tela,
    )

    # Cria dois conjuntos independentes de campos para não haver conflito de estado entre adicionar e editar
    campos_add = _criar_campos_formulario_curso()
    campos_edit = _criar_campos_formulario_curso()

    # Estado compartilhado (Ponteiro mutável): aponta para a linha visual e o ID do banco atualmente em edição
    estado = {"linha_atual": None, "id_firebase": None}

    # Tabela principal
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

    # Linha dos três indicadores numéricos na parte superior da tela
    linha_stats = ft.Row(
        spacing=20,
        controls=[
            criar_stats_card("Total de Cursos", "0", layout.cores[TEXTO_PRINCIPAL]),
            criar_stats_card("Cursos Ativos", "0", layout.cores[TEXTO_PRINCIPAL]),
            criar_stats_card("Departamentos", "0", layout.cores[TEXTO_PRINCIPAL]),
        ],
    )

    def atualizar_interface() -> None:
        """Recalcula e atualiza as métricas dos cartões superiores varrendo os dados visíveis na tabela."""
        
        # A quantidade de cursos é o número total de linhas
        total_cursos = str(len(tabela_cursos.rows))

        # Set Comprehension para pegar departamentos únicos direto da UI, ignorando valores em branco
        departamentos_unicos = {
            linha.cells[2].content.value.strip()
            for linha in tabela_cursos.rows
            if hasattr(linha.cells[2].content, "value") and linha.cells[2].content.value.strip()
        }
        total_deptos = str(len(departamentos_unicos))

        cor_texto = layout.cores[TEXTO_PRINCIPAL]  # Mantém a cor coerente com o tema em qualquer atualização
        
        # Sobrescreve a linha de cards com os novos valores calculados
        linha_stats.controls = [
            criar_stats_card("Total de Cursos", total_cursos, cor_texto),
            criar_stats_card("Cursos Ativos", "0", cor_texto),  # Fixo em 0, aguardando implementação futura
            criar_stats_card("Departamentos", total_deptos, cor_texto),
        ]

        page.update()

    # === Inicialização dos Modais e Contextos ===
    modal_edit = criar_modal_edit(page, estado, campos_edit, atualizar_interface)

    # Empacota todas as dependências em um Dataclass para evitar passar 6 parâmetros longos toda hora
    contexto_tabela = ContextoTabelaCursos(
        page=page,
        tabela_cursos=tabela_cursos,
        atualizar_interface=atualizar_interface,
        modal_editar=modal_edit,
        campos_edit=campos_edit,
        estado=estado,
    )

    abrir_modal_add = criar_modal_add(contexto_tabela, campos_add)

    # === Carregar cursos iniciais (Integração Firestore) ===
    def carregar_cursos_iniciais() -> None:
        """Faz a requisição inicial ao Firestore e popula a interface."""
        cursos = obter_cursos_db()
        tabela_cursos.rows.clear()

        for c in cursos:
            # O .get() possui um fallback seguro ("" ou "S/C") para evitar travamentos caso os dados estejam incompletos no banco
            linha = criar_linha_curso(
                contexto_tabela,
                c.get("id"),
                c.get("codigo", "S/C"),
                c.get("nome", ""),
                c.get("departamento", ""),
                c.get("coordenador", ""),
            )
            tabela_cursos.rows.append(linha)
            
        atualizar_interface()

    # Executa a carga antes da tela terminar de ser desenhada
    carregar_cursos_iniciais()

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
                        
                        # Operador ternário elegante: mostra a tabela se ela tiver linhas, ou exibe um aviso amigável se estiver vazia
                        tabela_cursos if tabela_cursos.rows else ft.Text("Nenhum curso cadastrado ainda.", color=ft.Colors.GREY, size=14),
                    ],
                ),
            ),
        ],
    )

    layout.add_content(conteudo)
    return layout.criar_view("/cursos")