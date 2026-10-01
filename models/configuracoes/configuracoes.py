import flet as ft
from typing import Callable

from components.layout.responsive.responsive import ResponsiveLayout
from models.configuracoes.widgets.configuracoes_ui import criar_layout_principal
from models.configuracoes.widgets.estado_indicadores import EstadoIndicadores
from models.configuracoes.modals.modal_criterios import criar_modal_criterios
from models.configuracoes.modals.modal_exclusao import criar_modal_exclusao
from models.configuracoes.modals.modal_edicao import criar_modal_edicao
from models.configuracoes.modals.modal_novo import criar_modal_novo
from models.configuracoes.core.painel_seguranca import criar_painel_seguranca
from models.configuracoes.core.painel_banco import criar_painel_banco
from models.configuracoes.core.pastas import criar_layout_pastas, abrir_pasta
from models.configuracoes.core.abas import criar_abas

def ViewConfiguracoes(
    page: ft.Page, 
    mudar_tela: Callable[[str], None]
) -> ft.View:
    """Constrói a tela de configurações, unindo layout responsivo, pastas e controle de dados"""
    
    layout = ResponsiveLayout(
        page, 
        titulo_pagina="Configurações", 
        subtitulo="Gerencie indicadores e critérios de avaliação.", 
        mudar_tela=mudar_tela,
    )
    
    # =====================================================================
    # INICIA O GERENCIADOR DE ESTADO
    # =====================================================================
    estado = EstadoIndicadores() 
    
    def ir_para_pasta(titulo: str) -> None:
        """Injetada nos modais para forçar a atualização visual da pasta atual após salvar/deletar dados."""
        abrir_pasta(page, titulo, estado)

    ''' === Inicialização dos Modais === '''
    modal_edicao, _, _, estado.abrir_modal_edicao = criar_modal_edicao(page, estado, ir_para_pasta)
    modal_criterios, _, estado.abrir_modal_criterios = criar_modal_criterios(page, estado)
    modal_exclusao, estado.preparar_exclusao = criar_modal_exclusao(page, estado, ir_para_pasta)
    modal_novo, _, _, estado.abrir_modal_novo = criar_modal_novo(page, estado, ir_para_pasta)

    # Área dinâmica que renderiza as pastas ou a lista de indicadores
    area_dinamica_indicadores = ft.Container(expand=True)
    area_dinamica_indicadores.content = criar_layout_pastas(page, estado, callback_abrir=ir_para_pasta)
    
    # Inicializa as outras telas de configurações
    painel_seguranca = criar_painel_seguranca()
    painel_banco = criar_painel_banco()

    # Agrupa os painéis sob o controle de Abas e salva a área de conteúdo no estado
    menu_abas, area_conteudo_aba = criar_abas(page, area_dinamica_indicadores, painel_seguranca, painel_banco)
    estado.area_conteudo_aba = area_conteudo_aba

    # Montagem e renderização
    conteudo = criar_layout_principal(layout.cores, menu_abas, area_conteudo_aba)
    layout.add_content(conteudo)
    
    return layout.criar_view("/configuracoes")