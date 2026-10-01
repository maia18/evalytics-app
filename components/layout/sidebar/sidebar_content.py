import flet as ft
from typing import Callable
from components.core.constants.constants import TEXTO_PRINCIPAL
from components.layout.sidebar.sidebar_logo import criar_logo
from components.layout.sidebar.sidebar_items import montar_botoes_menu
from components.widgets.menu.menu import MENU_ITEMS
from components.widgets.menu.menu_item import criar_item_menu

def criar_sidebar_content(
    dark_mode: bool, 
    mudar_tela: Callable[[str], None], 
    cores: dict[str, str]
) -> ft.Column:
    """Constrói a visualização padrão (expandida) da barra lateral do sistema."""
    
    # 1. Estrutura Base (Cabeçalho da Sidebar)
    controles: list[ft.Control] = [
        criar_logo(cores), # Renderiza a versão completa do logo (por padrão compact=False)
        ft.Divider(height=2), # Linha divisória para separar visualmente a marca da área de navegação.
    ]

    # 2. Construção da Lista de Navegação
    controles.extend(
        montar_botoes_menu(
            MENU_ITEMS,       # Estrutura com os dados dos menus completos (ícone + texto explicativo)
            criar_item_menu,  # Factory function: sabe desenhar um botão de menu expandido
            dark_mode, 
            cores[TEXTO_PRINCIPAL], 
            mudar_tela        # Callback executado no evento 'on_click' dos botões
        )
    )

    # 3. Retorno do Contêiner Principal (Coluna)
    return ft.Column(
        controls=controles,
        spacing=0, # Remove o vão automático entre os elementos.                 
        scroll=ft.ScrollMode.AUTO, # Só exibe a barra de rolagem se a quantidade de itens no menu ultrapassar a altura disponível da tela do usuário.
        expand=False, # A coluna ocupará apenas a altura necessária para seu conteúdo.                
    )