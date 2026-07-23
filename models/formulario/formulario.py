import flet as ft
# Importa o gerenciador central de layout responsivo que engloba a página
from components.layout.responsive.responsive import ResponsiveLayout 
# Importa o controlador do formulário, responsável por ditar as regras de negócio e transições
from models.formulario.core.form_controller import FormularioController

def ViewFormulario(page: ft.Page, mudar_tela):
    """
    Constrói a tela de 'Avaliação Institucional' (Formulário).
    Delega a lógica de transição das perguntas e validação dos dados para o FormularioController.
    """

    # Inicializa a estrutura base da página (Sidebar, Topbar e fundos adaptativos)
    layout = ResponsiveLayout(
        page, 
        titulo_pagina="Avaliação Institucional", 
        subtitulo="Preencha o formulário abaixo para contribuir com a melhoria contínua.", 
        mudar_tela=mudar_tela
    )

    # Container dinâmico responsável por abrigar as etapas do formulário.
    # À medida que o usuário avança, o conteúdo interno desta coluna é substituído.
    area_dinamica_conteudo = ft.Column(
        expand=True, # Permite que a coluna cresça para ocupar o espaço disponível
        spacing=25, # Espaçamento padrão entre os campos de perguntas
        # Adiciona uma transição suave de opacidade (fade in/out) quando o conteúdo desta coluna for alterado
        animate_opacity=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT)
    )

    # "Envelope" estrutural que envolve a área dinâmica para aplicar as margens (padding)
    area_central = ft.Container(
        expand=True, 
        # Garante que o formulário não encoste nas bordas laterais ou inferiores da tela
        padding=ft.padding.only(top=10, bottom=30, right=20), 
        content=area_dinamica_conteudo
    )

    # Instancia o Controlador do formulário repassando as referências cruciais da tela.
    # O controller usará a 'area_dinamica_conteudo' como um "palco" para renderizar 
    # o passo 1, passo 2, ou a tela final de sucesso.
    controller = FormularioController(
        page=page, 
        mudar_tela=mudar_tela, 
        area_dinamica=area_dinamica_conteudo, 
        area_central=area_central
    )

    # Gatilho inicial: Pede ao controlador para desenhar o primeiro bloco de perguntas na tela
    controller.atualizar_renderizacao()

    # Injeta todo o bloco montado na área de conteúdo do ResponsiveLayout
    layout.add_content(area_central)
    
    # Retorna a View finalizada e pronta para ser exibida na rota "/formulario"
    return layout.criar_view("/formulario")
