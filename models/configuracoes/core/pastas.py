import flet as ft

# Importações das Views (Componentes visuais) e do Estado (State Management)
from models.configuracoes.widgets.layout_pastas import (
    criar_layout_pastas,
    MAPA_EIXOS,
)
from models.configuracoes.widgets.layout_lista import criar_layout_lista
from models.configuracoes.widgets.estado_indicadores import EstadoIndicadores

def abrir_pasta(page: ft.Page, titulo_pasta: str, estado: EstadoIndicadores) -> None:
    """
    Substitui dinamicamente a visualização inicial de Pastas pela listagem de indicadores de um eixo.
        Atua como um 'Controller' de rotas internas da aba.
    """
    
    eixo_id = MAPA_EIXOS.get(titulo_pasta) # Traduz o nome legível da pasta clicada para o ID numérico correspondente mapeado no dicionário
    estado.definir_pasta_aberta(titulo_pasta, eixo_id) # Atualiza a classe de estado compartilhada para que os modais de edição saibam exatamente onde salvar novos itens

    '''
    Delega a montagem estrutural da interface para a View externa
        Passa a função de retorno (voltar_para_pastas) envelopada em uma função anônima (lambda) como callback
    '''
    novo_layout = criar_layout_lista(
        page, 
        estado, 
        titulo_pasta, 
        eixo_id,
        callback_voltar=lambda: voltar_para_pastas(page, estado)
    )

    # Substitui o conteúdo do container dinâmico principal (apagando as pastas da tela) e comanda o redesenho da interface
    estado.area_conteudo_aba.content = novo_layout
    page.update()

def voltar_para_pastas(page: ft.Page, estado: EstadoIndicadores) -> None:
    """Desfaz a visualização interna da lista e reconstrói as pastas principais."""
    
    '''
    Reconstrói a grade inicial injetando a função de abrir pasta como callback.
        Esta injeção de dependência via parâmetro evita a necessidade de importar 'abrir_pasta' dentro do arquivo de layout
    '''
    layout_inicial = criar_layout_pastas(
        page, estado,
        callback_abrir=lambda titulo: abrir_pasta(page, titulo, estado)
    )
    
    # Injeta novamente a grade de pastas no container dinâmico e atualiza a tela
    estado.area_conteudo_aba.content = layout_inicial
    page.update()