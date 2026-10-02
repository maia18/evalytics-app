import flet as ft
from typing import Callable
from components.core.constants.constants import TEXTO_PRINCIPAL
from components.layout.sidebar.sidebar_logout import criar_botao_logout
from components.layout.sidebar.sidebar_logo import criar_logo
from components.layout.sidebar.sidebar_items import montar_botoes_menu
from components.widgets.menu.menu import MENU_ITEMS
from components.widgets.menu.menu_item import criar_item_menu

<<<<<<< HEAD
# Constrói a visualização padrão do menu, com logotipo completo e botões descritivos
def criar_sidebar_content(
    page,
    dark_mode: bool,
    mudar_tela: Callable[[str], None],
    cores: dict[str, str],
) -> ft.Column:
    
=======
def criar_sidebar_content(
    dark_mode: bool, 
    mudar_tela: Callable[[str], None], 
    cores: dict[str, str]
) -> ft.Column:
    """Constrói a visualização padrão (expandida) da barra lateral do sistema."""
    
    # 1. Estrutura Base (Cabeçalho da Sidebar)
>>>>>>> ea794a06b2548ae4a0bed3f239fa3214c9fd367e
    controles: list[ft.Control] = [
        criar_logo(cores), # Renderiza a versão completa do logo (por padrão compact=False)
        ft.Divider(height=2), # Linha divisória para separar visualmente a marca da área de navegação.
    ]

    # 2. Construção da Lista de Navegação
    controles.extend(
        montar_botoes_menu(
<<<<<<< HEAD
            MENU_ITEMS,
            criar_item_menu,
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
            ),
        ]
=======
            MENU_ITEMS,       # Estrutura com os dados dos menus completos (ícone + texto explicativo)
            criar_item_menu,  # Factory function: sabe desenhar um botão de menu expandido
            dark_mode, 
            cores[TEXTO_PRINCIPAL], 
            mudar_tela        # Callback executado no evento 'on_click' dos botões
        )
>>>>>>> ea794a06b2548ae4a0bed3f239fa3214c9fd367e
    )

    # 3. Retorno do Contêiner Principal (Coluna)
    return ft.Column(
        controls=controles,
<<<<<<< HEAD
        spacing=0,                    # Mantém os botões colados uns nos outros
        expand=True,                 # Não força a coluna a ocupar mais espaço do que o necessário
=======
        spacing=0, # Remove o vão automático entre os elementos.                 
        scroll=ft.ScrollMode.AUTO, # Só exibe a barra de rolagem se a quantidade de itens no menu ultrapassar a altura disponível da tela do usuário.
        expand=False, # A coluna ocupará apenas a altura necessária para seu conteúdo.                
>>>>>>> ea794a06b2548ae4a0bed3f239fa3214c9fd367e
    )