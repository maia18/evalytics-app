import flet as ft
from typing import Callable
from components.layout.responsive.responsive import ResponsiveLayout
from components.core.constants.constants import (
    TEXTO_PRINCIPAL, 
    CARD,
)
from models.configuracoes.widgets.estado_indicadores import EstadoIndicadores
from models.configuracoes.modals.modal_criterios import criar_modal_criterios
from models.configuracoes.modals.modal_exclusao import criar_modal_exclusao
from models.configuracoes.modals.modal_edicao import criar_modal_edicao
from models.configuracoes.modals.modal_novo import criar_modal_novo
from models.configuracoes.core.painel_seguranca import criar_painel_seguranca
from models.configuracoes.core.painel_banco import criar_painel_banco
from models.configuracoes.core.pastas import criar_layout_pastas
from models.configuracoes.core.abas import criar_abas

def ViewConfiguracoes(page: ft.Page, mudar_tela: Callable[[str], None]) -> ft.View:
    """Constrói a tela de configurações, unindo layout responsivo, pastas e controle de dados"""
    
    layout = ResponsiveLayout(
        page, 
        titulo_pagina="Configurações", 
        subtitulo="Gerencie indicadores e critérios de avaliação.", 
        mudar_tela=mudar_tela,
    )

    # Inicia o gerenciador de estado
    estado = EstadoIndicadores() 

    def ir_para_pasta(titulo: str) -> None:
        """Injetada nos modais para forçar a atualização visual da pasta atual após salvar/deletar dados"""
        
        from models.configuracoes.core.pastas import abrir_pasta
        abrir_pasta(page, titulo, estado)

    ''' === Inicialização dos Modais === '''
    modal_edicao, campo_titulo, campo_descricao, estado.abrir_modal_edicao = criar_modal_edicao(page, estado, ir_para_pasta)
    modal_criterios, _, estado.abrir_modal_criterios = criar_modal_criterios(page, estado)
    modal_exclusao, estado.preparar_exclusao = criar_modal_exclusao(page, estado, ir_para_pasta)
    modal_novo, campo_titulo_novo, campo_desc_novo, estado.abrir_modal_novo = criar_modal_novo(page, estado, ir_para_pasta)

    # Área dinâmica que renderiza as pastas ou a lista de indicadores
    area_dinamica_indicadores = ft.Container(expand=True)
    area_dinamica_indicadores.content = criar_layout_pastas(page, estado, callback_abrir=ir_para_pasta)
    
    # Inicializa as outras telas de configurações
    painel_seguranca = criar_painel_seguranca()
    painel_banco = criar_painel_banco()

    # Agrupa os painéis sob o controle de Abas e salva a área de conteúdo no estado
    menu_abas, area_conteudo_aba = criar_abas(page, area_dinamica_indicadores, painel_seguranca, painel_banco)
    estado.area_conteudo_aba = area_conteudo_aba

    '''Montagem da hierarquia visual final da página'''
    conteudo = ft.Column(
        expand=True,
        controls=[
            ft.Text("Configurações do Sistema", size=28, weight="bold", color=layout.cores[TEXTO_PRINCIPAL]),
            ft.Text("Gerencie indicadores, acessos e manutenção de dados.", size=16, color=ft.Colors.GREY),
            ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
            
            # Card master que abriga o conteúdo das abas
            ft.Container(
                expand=True, bgcolor=layout.cores[CARD], border_radius=10, padding=20,
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