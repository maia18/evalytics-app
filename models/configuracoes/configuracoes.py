from typing import Callable

import flet as ft

from components.layout.responsive.responsive import ResponsiveLayout
from components.core.constants.constants import TEXTO_PRINCIPAL, CARD

from models.configuracoes.modals.modal_edicao import criar_modal_edicao
from models.configuracoes.modals.modal_criterios import criar_modal_criterios
from models.configuracoes.modals.modal_exclusao import criar_modal_exclusao
from models.configuracoes.modals.modal_novo import criar_modal_novo

from models.configuracoes.core.painel_seguranca import criar_painel_seguranca
from models.configuracoes.core.painel_banco import criar_painel_banco
from models.configuracoes.core.pastas import criar_layout_pastas
from models.configuracoes.core.abas import criar_abas
from models.configuracoes.core.estado_indicadores import EstadoIndicadores


def ViewConfiguracoes(page: ft.Page, mudar_tela: Callable[[str], None]) -> ft.View:
    """Constrói a tela de configurações, unindo layout responsivo, pastas de indicadores e controle de dados."""
    layout = ResponsiveLayout(
        page,
        titulo_pagina="Configurações",
        subtitulo="Gerencie indicadores e critérios de avaliação.",
        mudar_tela=mudar_tela,
    )

    # Estado compartilhado entre a listagem de indicadores e os modais de gerenciamento.
    # As referências de callback (abrir_modal_*, area_conteudo_aba) são preenchidas
    # logo abaixo, após a criação dos respectivos componentes — como os consumidores
    # (pastas.py) só acessam essas referências no momento do clique (não na criação),
    # não há risco de usá-las antes de estarem definidas.
    estado = EstadoIndicadores()

    def ir_para_pasta(titulo: str) -> None:
        from models.configuracoes.core.pastas import abrir_pasta
        abrir_pasta(page, titulo, estado)

    # === Modais ===
    modal_edicao, campo_titulo, campo_descricao, estado.abrir_modal_edicao = criar_modal_edicao(page, estado, ir_para_pasta)
    modal_criterios, _, estado.abrir_modal_criterios = criar_modal_criterios(page, estado)
    modal_exclusao, estado.preparar_exclusao = criar_modal_exclusao(page, estado, ir_para_pasta)
    modal_novo, campo_titulo_novo, campo_desc_novo, estado.abrir_modal_novo = criar_modal_novo(page, estado, ir_para_pasta)

    # Área que alternará o conteúdo exibido (Pastas vs. Lista de Indicadores)
    area_dinamica_indicadores = ft.Container(expand=True)
    area_dinamica_indicadores.content = criar_layout_pastas(page, estado)

    # Painéis auxiliares da página de configurações
    painel_seguranca = criar_painel_seguranca()
    painel_banco = criar_painel_banco()

    # Agrupa as áreas geradas em um controle de Abas para navegação superior
    menu_abas, area_conteudo_aba = criar_abas(page, area_dinamica_indicadores, painel_seguranca, painel_banco)
    estado.area_conteudo_aba = area_conteudo_aba

    conteudo = ft.Column(
        expand=True,
        controls=[
            ft.Text("Configurações do Sistema", size=28, weight="bold", color=layout.cores[TEXTO_PRINCIPAL]),
            ft.Text("Gerencie indicadores, acessos e manutenção de dados.", size=16, color=ft.Colors.GREY),
            ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
            ft.Container(
                expand=True,
                bgcolor=layout.cores[CARD],
                border_radius=10,
                padding=20,
                shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color=ft.Colors.BLACK12),
                content=ft.Column(
                    expand=True,
                    controls=[
                        menu_abas,
                        ft.Divider(height=20, color=ft.Colors.GREY_200),
                        ft.Container(expand=True, padding=10, content=area_conteudo_aba),
                    ],
                ),
            ),
        ],
    )

    layout.add_content(conteudo)
    return layout.criar_view("/configuracoes")