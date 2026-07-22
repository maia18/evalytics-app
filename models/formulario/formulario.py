import flet as ft
from components.layout.responsive.responsive import ResponsiveLayout 
from models.formulario.core.form_controller import FormularioController

def ViewFormulario(page: ft.Page, mudar_tela):
    
    layout = ResponsiveLayout(
        page, 
        titulo_pagina="Avaliação Institucional", 
        subtitulo="Preencha o formulário abaixo para contribuir com a melhoria contínua.", 
        mudar_tela=mudar_tela
    )
    
    area_dinamica_conteudo = ft.Column(
        expand=True,
        spacing=25,
        animate_opacity=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT)
    )

    area_central = ft.Container(
        expand=True, 
        padding=ft.Padding.only(top=10, bottom=30, right=20), 
        content=area_dinamica_conteudo
    )

    controller = FormularioController(
        page=page, 
        mudar_tela=mudar_tela, 
        area_dinamica=area_dinamica_conteudo, 
        area_central=area_central
    )
    
    controller.atualizar_renderizacao()

    layout.add_content(area_central)
    return layout.criar_view("/formulario")