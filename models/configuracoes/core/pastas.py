import flet as ft
from models.configuracoes.widgets.estado_indicadores import EstadoIndicadores
from models.configuracoes.widgets.layout_pastas import criar_layout_pastas, MAPA_EIXOS
from models.configuracoes.widgets.layout_lista import criar_layout_lista

def abrir_pasta(page: ft.Page, titulo_pasta: str, estado: EstadoIndicadores) -> None:
    """Substitui dinamicamente a visualização inicial de Pastas pela listagem de indicadores de um eixo"""
    
    eixo_id = MAPA_EIXOS.get(titulo_pasta)
    estado.definir_pasta_aberta(titulo_pasta, eixo_id)

    # Delega a montagem da interface para a View externa
    novo_layout = criar_layout_lista(page, estado, titulo_pasta, eixo_id, callback_voltar=lambda: voltar_para_pastas(page, estado))

    # Substitui o conteúdo do container principal e atualiza a tela
    estado.area_conteudo_aba.content = novo_layout
    page.update()

def voltar_para_pastas(page: ft.Page, estado: EstadoIndicadores) -> None:
    """Desfaz a visualização interna da lista e reconstrói as pastas principais."""
    
    # Reconstrói a grade inicial injetando a função de abrir pasta como callback
    layout_inicial = criar_layout_pastas(page, estado, callback_abrir=lambda titulo: abrir_pasta(page, titulo, estado))
    
    estado.area_conteudo_aba.content = layout_inicial
    page.update()