import flet as ft
from typing import Callable
from components.core.constants.constants import TEXTO_PRINCIPAL
from components.layout.sidebar.sidebar_logout import criar_botao_logout
from components.layout.sidebar.sidebar_logo import criar_logo
from components.layout.sidebar.sidebar_items import montar_botoes_menu
from components.widgets.menu.menu import MENU_ITEMS_COLLAPSED
from components.widgets.menu.botao_icon import criar_botao_icon

<<<<<<< HEAD
# Constrói os elementos do menu lateral focado apenas em ícones
def criar_sidebar_colapsada(
    page: ft.Page,
    dark_mode: bool,
    mudar_tela: Callable[[str], None],
    cores: dict[str, str],
) -> ft.Column:
    
=======
def criar_sidebar_colapsada(
    dark_mode: bool, 
    mudar_tela: Callable[[str], None], 
    cores: dict[str, str]
) -> ft.Column:
    """
    Constrói a versão retraída (colapsada/mini) da barra lateral de navegação (Sidebar).   
        Neste estado, a sidebar exibe apenas ícones para economizar espaço horizontal na tela.
    """
    
    # 1. Inicializa a lista de controles da Sidebar.
>>>>>>> ea794a06b2548ae4a0bed3f239fa3214c9fd367e
    controles: list[ft.Control] = [
        
        # Logo em versão reduzida (ex: apenas o símbolo, sem o texto da marca)
        criar_logo(
            cores, 
            compact=True # Flag que avisa ao componente de logo para renderizar sua versão mini
        ),
        ft.Divider(height=1), # Linha divisória sutil para separar o topo (logo) da área de navegação
    ]
    
    # 2. Geração dinâmica dos botões do menu
    controles.extend(
        montar_botoes_menu(
<<<<<<< HEAD
            MENU_ITEMS_COLLAPSED,
            criar_botao_icon,
            dark_mode,
            cores[TEXTO_PRINCIPAL],
            mudar_tela,
        )
    )
    
    controles.extend(
        [
            ft.Container(expand=True),

            ft.Divider(height=1),

            criar_botao_logout(
                page=page,
                dark_mode=dark_mode,
                cor_texto=cores[TEXTO_PRINCIPAL],
                mudar_tela=mudar_tela,
                compact=True,
            ),
        ]
    )
=======
            MENU_ITEMS_COLLAPSED, # Estrutura de dados contendo as rotas e ícones da versão mini
            criar_botao_icon,     # Função 'factory' que sabe como desenhar um botão de ícone
            dark_mode, 
            cores[TEXTO_PRINCIPAL], 
            mudar_tela            # Injeta a função de navegação para o click do botão
        )
    )
    
    # 3. Rodapé do menu
    controles.append(ft.Divider(height=1))
>>>>>>> ea794a06b2548ae4a0bed3f239fa3214c9fd367e

    # 4. Retorna a Coluna que engloba tudo
    return ft.Column(
        controls=controles,
<<<<<<< HEAD
        spacing=0,
        expand=True,
=======
        spacing=0, # Remove os espaços automáticos do Flet entre os itens. 
        scroll=ft.ScrollMode.AUTO, # AUTO permite que a barra lateral crie uma barra de rolagem (scroll) apenas se a altura da tela for muito pequena para mostrar todos os ícones.
        alignment=ft.MainAxisAlignment.START, # Alinha todos os itens (logo e botões) no topo da barra lateral
>>>>>>> ea794a06b2548ae4a0bed3f239fa3214c9fd367e
    )