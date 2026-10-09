import flet as ft
from typing import Callable
from components.core.constants.constants import (
    TEXTO_PRINCIPAL, 
    SURFACE, 
    COR_PRIMARIA,
)
from components.layout.topbar.topbar_utils import obter_icone_tema
from utils.services.location.location_service import obter_localizacao
from .core.notifications.topbar_notifications import criar_componentes_notificacoes

def criar_topbar_content(
    page: ft.Page,
    titulo: str,
    subtitulo: str,
    dark_mode: bool,
    cores: dict[str, str],
    menu_button: ft.IconButton,
    atualizar_tema: Callable[[], None],
    notificacoes_pendentes: int = 0,
) -> ft.Row:
    """Constrói a faixa de navegação superior (Cabeçalho da Página)."""

    local_atual = obter_localizacao()
    icone_tema = obter_icone_tema(dark_mode)

    '''
    Extrai múltiplos componentes interligados relacionados a notificações.
        O "painel_notificacoes" é solto (não fica dentro da Row da Topbar), pois ele será colocado no `page.overlay` global.
    '''
    area_notificacoes, painel_notificacoes, badge_notificacoes, atualizar_lista = criar_componentes_notificacoes(page, cores)

    conteudo = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN, # Joga o bloco 1 pra esquerda e o bloco 2 pra direita
        controls=[
            
            # BLOCO ESQUERDO: Menu Hambúrguer (Mobile) e Títulos da Página
            ft.Row(
                spacing=10,
                controls=[
                    menu_button,
                    ft.Column(
                        spacing=0,
                        controls=[
                            ft.Text(titulo, size=20, weight="bold", color=cores[TEXTO_PRINCIPAL]),
                            ft.Text(subtitulo, size=12, color=ft.Colors.GREY),
                        ],
                    ),
                ],
            ),
    
            # BLOCO DIREITO: Ações Rápidas (Localização, Tema, Notificações, Perfil)
            ft.Row(
                controls=[
                    
                    # Chip/Badge informativo da Localização Atual
                    ft.Container(
                        padding=10,
                        border_radius=8,
                        bgcolor=cores[SURFACE],
                        content=ft.Row(
                            spacing=6,
                            controls=[
                                ft.Icon(ft.Icons.LOCATION_ON_OUTLINED, size=18, color=COR_PRIMARIA),
                                ft.Text(local_atual, size=14, weight="w500", color=cores[TEXTO_PRINCIPAL]),
                            ],
                        ),
                    ),
                    
                    # Botão de Toggle de Tema (Chama o callback recebido por parâmetro)
                    ft.IconButton(
                        icon=icone_tema,
                        on_click=lambda e: atualizar_tema(),
                    ),
                    
                    # Ícone do sininho de notificações
                    area_notificacoes,
                    
                    # Foto do Usuário (Placeholder)
                    ft.CircleAvatar(
                        radius=18,
                        color=cores[TEXTO_PRINCIPAL],
                        content=ft.Text("AC"),
                    ),
                ],
            ),
        ],
    )
    
    '''
    MONKEY PATCHING (Atenção):
        O Python permite injetar atributos dinamicamente em objetos existentes.
            Estamos grudando referências do painel e do atualizador diretamente na instância  visual da `Row` (conteudo). 
            Isso permite que o `ResponsiveLayout` encontre o  `painel_notificacoes` para injetá-lo no `page.overlay` posteriormente.
    '''
    conteudo.badge_notificacoes = badge_notificacoes
    conteudo.painel_notificacoes = painel_notificacoes
    conteudo.atualizar_lista_notificacoes = atualizar_lista

    return conteudo