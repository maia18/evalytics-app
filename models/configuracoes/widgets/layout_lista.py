import flet as ft
from typing import Callable
from models.configuracoes.widgets.indicadores_ui import criar_linha_indicador
from models.configuracoes.widgets.estado_indicadores import EstadoIndicadores
from utils.services.indicadores.indicadores_repository import listar_indicadores_por_eixo

def criar_layout_lista(
    page: ft.Page, 
    estado: EstadoIndicadores, 
    titulo_pasta: str, 
    eixo_id: int, 
    callback_voltar: Callable[[], None]
) -> ft.Column:
    """
    Gera a interface interna de uma "pasta" (Eixo) exibindo a lista de indicadores cadastrados nela.
        Esta tela substitui a visualização de pastas quando o usuário clica em um dos eixos.
    """
    
    # 1. Busca os dados reais vinculados a este eixo específico
    lista_da_pasta = listar_indicadores_por_eixo(eixo_id)

    # 2. Construção do Cabeçalho da Lista
    # Inicializamos a lista de controles com o topo da tela.
    controles_lista: list[ft.Control] = [
        
        # A Row com SPACE_BETWEEN empurra o grupo "Voltar + Título" para a extrema esquerda e o botão "Novo" para a extrema direita da tela.
        ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                
                # Bloco da Esquerda (Botão Voltar e Título agrupados)
                ft.Row([
                    ft.IconButton(
                        icon=ft.Icons.ARROW_BACK, 
                        on_click=lambda _: callback_voltar() # Quando clicado, executa a função que destrói esta tela e volta para as pastas
                    ),
                    ft.Text(
                        titulo_pasta, 
                        size=22, 
                        weight="bold", 
                        color=ft.Colors.BLACK87
                    ),
                ]),
                
                # Bloco da Direita (Botão de Ação Primária)
                ft.ElevatedButton(
                    "Novo Indicador", 
                    icon=ft.Icons.ADD, 
                    bgcolor=ft.Colors.BLUE_700, 
                    color=ft.Colors.WHITE,
                    on_click=lambda e: estado.abrir_modal_novo(),                     # Aciona o método da classe de Estado que gerencia a abertura do modal de criação

                ),
            ],
        ),
        ft.Divider(height=20, color=ft.Colors.TRANSPARENT), # Separador invisível para criar um respiro entre o cabeçalho e os itens da lista
    ]

    # 3. Construção dinâmica das linhas da lista
    for item in lista_da_pasta:
        controles_lista.append(
            criar_linha_indicador(
                item,
                lambda e, i=item: estado.abrir_modal_criterios(e, i),
                lambda e, i=item: estado.abrir_modal_edicao(e, i),
                lambda i=item: estado.preparar_exclusao(i),
            )
        )
        
    # 4. Retorna o contêiner raiz da visualização
    return ft.Column(
        expand=True,               # Permite que a lista ocupe todo o espaço até o fim da tela
        scroll=ft.ScrollMode.AUTO, # Adiciona barra de rolagem automática se houver muitos itens
        spacing=15,                # Espaço uniforme de 15px entre cada linha de indicador
        controls=controles_lista   # Injeta a lista que construímos ao longo da função
    )