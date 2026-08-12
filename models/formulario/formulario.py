from typing import Callable
import flet as ft

from components.layout.responsive.responsive import ResponsiveLayout
from models.formulario.core.form_controller import FormularioController

def ViewFormulario(page: ft.Page, mudar_tela: Callable[[str], None]) -> ft.View:
    """
    Constrói a tela de Avaliação Institucional (Formulário).
        Delega a lógica de transição das perguntas e validação dos dados para o FormularioController.
    """
    layout = ResponsiveLayout(
        page, titulo_pagina="Avaliação Institucional", subtitulo="Preencha o formulário abaixo para contribuir com a melhoria contínua.", mudar_tela=mudar_tela,
    )

    # Área dinâmica que sofrerá as animações de fade in/out entre as perguntas.
    area_dinamica_conteudo = ft.Column(
        expand=True, spacing=25,
        animate_opacity=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
    )

    area_central = ft.Container(
        expand=True, padding=ft.Padding.only(top=10, bottom=30, right=20), content=area_dinamica_conteudo,
    )

    # Instancia o cérebro do formulário, que orquestrará a injeção do conteúdo na tela
    controller = FormularioController(
        page=page, mudar_tela=mudar_tela, area_dinamica=area_dinamica_conteudo, area_central=area_central,
    )

    # Engatilha a construção da primeira pergunta
    controller.atualizar_renderizacao()

    layout.add_content(area_central)
    return layout.criar_view("/formulario")