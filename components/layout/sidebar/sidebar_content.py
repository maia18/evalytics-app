import flet as ft 
from components.widgets.menu.menu import MENU_ITEMS 
from components.widgets.menu.menu_item import criar_item_menu 
from components.layout.sidebar.sidebar_logo import criar_logo 
from components.core.constants.constants import * 

# Sidebar completa
def criar_sidebar_content(dark_mode, mudar_tela, cores): 
    """Constrói a visualização padrão do menu, contendo o logotipo completo e os botões de ação descritivos."""
    
    controles = [ 
        criar_logo(cores), # Renderiza a versão em texto e ícone do logo do sistema
        ft.Divider(height=2), # Separa o cabeçalho das rotas de navegação
    ] 

    # Popula o restante do menu usando o mapeamento de telas configurado
    for icone, texto, rota in MENU_ITEMS: 
        controles.append( 
            criar_item_menu( # Gera os botões retangulares longos
                icone, texto, rota, dark_mode, cores[TEXTO_PRINCIPAL], mudar_tela 
            ) 
        ) 

    return ft.Column( 
        controls=controles, # Aloca toda a sequência
        spacing=0, # Mantém os botões colados uns nos outros (normalmente padding interno lida com margens)
        scroll=ft.ScrollMode.AUTO, # Funcionalidade de barra de rolagem
        expand=False, # Não força a coluna a ocupar mais espaço vertical do que o conteúdo necessita
    ) 