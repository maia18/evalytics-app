import flet as ft
from typing import Callable
from components.layout.responsive.responsive import ResponsiveLayout
from components.core.constants.constants import (
    TEXTO_PRINCIPAL, 
    CARD,
    TEXTO_SECUNDARIO,
    BORDA,
)
from models.configuracoes.widgets.configuracoes_ui import criar_layout_principal
from models.configuracoes.widgets.estado_indicadores import EstadoIndicadores
from models.configuracoes.modals.modal_criterios import criar_modal_criterios
from models.configuracoes.modals.modal_exclusao import criar_modal_exclusao
from models.configuracoes.modals.modal_edicao import criar_modal_edicao
from models.configuracoes.modals.modal_novo import criar_modal_novo
from models.configuracoes.core.painel_seguranca import criar_painel_seguranca
from models.configuracoes.core.painel_banco import criar_painel_banco
from models.configuracoes.core.pastas import criar_layout_pastas, abrir_pasta, voltar_para_pastas
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
    if not hasattr(page, "_estado_indicadores"):
        page._estado_indicadores = EstadoIndicadores()

    estado = page._estado_indicadores
    estado.cores = layout.cores
    
    def ir_para_pasta(titulo: str) -> None:
        """Injetada nos modais para forçar a atualização visual da pasta atual após salvar/deletar dados."""
        abrir_pasta(page, titulo, estado)
        
    def voltar_para_pastas_config() -> None:
        from models.configuracoes.core.pastas import voltar_para_pastas
        voltar_para_pastas(page, estado)
        
    ''' === Inicialização dos Modais === '''
    modal_edicao, campo_titulo, campo_descricao, estado.abrir_modal_edicao = criar_modal_edicao(
        page,
        estado,
        ir_para_pasta,
        layout.cores,
    )

    modal_criterios, _, estado.abrir_modal_criterios = criar_modal_criterios(
        page,
        estado,
        layout.cores,
    )

    modal_exclusao, estado.preparar_exclusao = criar_modal_exclusao(
        page,
        estado,
        ir_para_pasta,
        layout.cores,
    )

    modal_novo, campo_titulo_novo, campo_desc_novo, estado.abrir_modal_novo = criar_modal_novo(
        page,
        estado,
        ir_para_pasta,
        layout.cores,
    )

    # Área dinâmica que renderiza as pastas ou a lista de indicadores
    area_dinamica_indicadores = ft.Container(expand=True)

    if estado.pasta_titulo and estado.pasta_eixo:
        from models.configuracoes.widgets.layout_lista import criar_layout_lista

        area_dinamica_indicadores.content = criar_layout_lista(
            page,
            estado,
            estado.pasta_titulo,
            estado.pasta_eixo,
            callback_voltar=lambda: voltar_para_pastas(page, estado),
            cores=layout.cores,
        )
    else:
        area_dinamica_indicadores.content = criar_layout_pastas(
            page,
            estado,
            callback_abrir=ir_para_pasta,
            cores=layout.cores,
        )
    
    # Inicializa as outras telas de configurações
    painel_seguranca = criar_painel_seguranca(layout.cores)
    painel_banco = criar_painel_banco(layout.cores)

        # Agrupa os painéis sob o controle de Abas
    menu_abas, area_conteudo_aba = criar_abas(
        page,
        area_dinamica_indicadores,
        painel_seguranca,
        painel_banco,
        layout.cores,
    )

    estado.area_conteudo_aba = area_conteudo_aba

    # Montagem da hierarquia visual final da página
    conteudo = criar_layout_principal(
        layout.cores,
        menu_abas,
        area_conteudo_aba,
    )

    layout.add_content(conteudo)

    return layout.criar_view("/configuracoes")