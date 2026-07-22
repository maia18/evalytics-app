import flet as ft
from components.layout.responsive.responsive import ResponsiveLayout
from components.core.constants.constants import *
from models.avaliacoes.layout.card_controle_ciclo import criar_card_controle_ciclo
from models.avaliacoes.layout.card_tabela_dados import criar_card_tabela_dados

def ViewAvaliacoes(page: ft.Page, mudar_tela):
    layout = ResponsiveLayout(
        page,
        titulo_pagina="Avaliações",
        subtitulo="Acompanhe respostas e métricas em tempo real.",
        mudar_tela=mudar_tela
    )

    card_controle_ciclo = criar_card_controle_ciclo(layout, mudar_tela, page)
    card_tabela_dados = criar_card_tabela_dados(layout, page)

    conteudo = ft.Column(
        expand=True,
        spacing=20,
        controls=[
            ft.Column(
                spacing=5,
                controls=[
                    ft.Text("Gestão de Ciclos e Respostas", size=28, weight="bold", color=layout.cores[TEXTO_PRINCIPAL]),
                    ft.Text("Monitore campanhas ativas e extraia os dados brutos das avaliações.", size=16, color="grey"),
                ]
            ),
            card_controle_ciclo,
            card_tabela_dados
        ]
    )

    layout.add_content(conteudo)
    return layout.criar_view("/avaliacoes")