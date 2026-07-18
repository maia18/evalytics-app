import flet as ft
from database.indicadores import INDICADORES
from components.layout.responsive.responsive import ResponsiveLayout
from components.core.constants.constants import *

from models.configuracoes.modals.modal_edicao import criar_modal_edicao
from models.configuracoes.modals.modal_criterios import criar_modal_criterios
from models.configuracoes.modals.modal_exclusao import criar_modal_exclusao
from models.configuracoes.modals.modal_novo import criar_modal_novo
from models.configuracoes.core.indicadores_ui import criar_pasta_indicador
from models.configuracoes.core.painel_seguranca import criar_painel_seguranca
from models.configuracoes.core.painel_banco import criar_painel_banco
from models.configuracoes.core.pastas import abrir_pasta, voltar_para_pastas
from models.configuracoes.core.abas import criar_abas


def ViewConfiguracoes(page: ft.Page, mudar_tela):
    layout = ResponsiveLayout(
        page,
        titulo_pagina="Configurações",
        subtitulo="Gerencie indicadores e critérios de avaliação.",
        mudar_tela=mudar_tela
    )

    pasta_aberta_atualmente = {"titulo": "", "eixo": 0}
    item_alvo_acao = {}

    # === Modais ===
    modal_edicao, campo_titulo, campo_descricao, abrir_modal_edicao = criar_modal_edicao(
        page, item_alvo_acao, lambda t: abrir_pasta(page, t, pasta_aberta_atualmente, area_conteudo_aba,
                                                    abrir_modal_novo, abrir_modal_criterios, abrir_modal_edicao, preparar_exclusao),
        pasta_aberta_atualmente
    )
    modal_criterios, _, abrir_modal_criterios = criar_modal_criterios(page, item_alvo_acao)
    modal_exclusao, preparar_exclusao = criar_modal_exclusao(
        page, item_alvo_acao, lambda t: abrir_pasta(page, t, pasta_aberta_atualmente, area_conteudo_aba,
                                                    abrir_modal_novo, abrir_modal_criterios, abrir_modal_edicao, preparar_exclusao),
        pasta_aberta_atualmente
    )
    modal_novo, campo_titulo_novo, campo_desc_novo, abrir_modal_novo = criar_modal_novo(
        page, pasta_aberta_atualmente,
        lambda t: abrir_pasta(page, t, pasta_aberta_atualmente, area_conteudo_aba,
                              abrir_modal_novo, abrir_modal_criterios, abrir_modal_edicao, preparar_exclusao)
    )

    # Área dinâmica
    area_dinamica_indicadores = ft.Container(expand=True)

    # Layout inicial de pastas
    qtd_eixo_1 = sum(1 for item in INDICADORES if item.get("eixo") == 1)
    qtd_eixo_2 = sum(1 for item in INDICADORES if item.get("eixo") == 2)
    qtd_eixo_3 = sum(1 for item in INDICADORES if item.get("eixo") == 3)

    layout_pastas = ft.Column(
        expand=True,
        spacing=25,
        controls=[
            ft.Text("Gerenciar Indicadores", size=22, weight="bold", color="black87"),
            ft.Column(
                spacing=15,
                controls=[
                    criar_pasta_indicador("Organização Didático-Pedagógica", qtd_eixo_1,
                                          lambda t: abrir_pasta(page, t, pasta_aberta_atualmente, area_conteudo_aba,
                                                                abrir_modal_novo, abrir_modal_criterios, abrir_modal_edicao, preparar_exclusao)),
                    criar_pasta_indicador("Corpo Docente e Tutorial", qtd_eixo_2,
                                          lambda t: abrir_pasta(page, t, pasta_aberta_atualmente, area_conteudo_aba,
                                                                abrir_modal_novo, abrir_modal_criterios, abrir_modal_edicao, preparar_exclusao)),
                    criar_pasta_indicador("Infraestrutura", qtd_eixo_3,
                                          lambda t: abrir_pasta(page, t, pasta_aberta_atualmente, area_conteudo_aba,
                                                                abrir_modal_novo, abrir_modal_criterios, abrir_modal_edicao, preparar_exclusao)),
                ]
            )
        ]
    )

    area_dinamica_indicadores.content = layout_pastas

    # Painéis
    painel_seguranca = criar_painel_seguranca()
    painel_banco = criar_painel_banco()

    # Abas
    menu_abas, area_conteudo_aba = criar_abas(page, area_dinamica_indicadores, painel_seguranca, painel_banco)

    # Conteúdo principal
    conteudo = ft.Column(
        expand=True,
        controls=[
            ft.Text("Configurações do Sistema", size=28, weight="bold", color=layout.cores[TEXTO_PRINCIPAL]),
            ft.Text("Gerencie indicadores, acessos e manutenção de dados.", size=16, color="grey"),
            ft.Divider(height=20, color="transparent"),
            ft.Container(
                expand=True,
                bgcolor=layout.cores[CARD],
                border_radius=10,
                padding=20,
                shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color="black12"),
                content=ft.Column(
                    expand=True,
                    controls=[
                        menu_abas,
                        ft.Divider(height=20, color="grey200"),
                        ft.Container(expand=True, padding=10, content=area_conteudo_aba)
                    ]
                )
            )
        ]
    )

    layout.add_content(conteudo)
    return layout.criar_view("/configuracoes")