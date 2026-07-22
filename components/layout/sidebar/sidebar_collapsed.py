import flet as ft 
from components.widgets.menu.menu import MENU_ITEMS_COLLAPSED 
from components.widgets.menu.botao_icon import criar_botao_icon 
from components.layout.sidebar.sidebar_logo import criar_logo 
from components.core.constants.constants import * 

# Sidebar compacta
def criar_sidebar_colapsada(dark_mode, mudar_tela, cores): 
    """Constrói os elementos do menu lateral focado apenas em ícones."""
    
    controles = [ 
        criar_logo(cores, compact=True), # Gera a versão de logo que só mostra o ícone da aplicação
        ft.Divider(height=1), # Linha horizontal fina logo abaixo da marca
    ] 

    # Laço de repetição (Loop) para criar cada botão baseando-se nos itens do menu compacto
    for icone, texto, rota in MENU_ITEMS_COLLAPSED: 
        controles.append( 
            criar_botao_icon( # Utiliza o widget que exibe só o ícone clicável
                icone, texto, rota, dark_mode, cores[TEXTO_PRINCIPAL], mudar_tela 
            ) 
        ) 

    controles.append(ft.Divider(height=1)) # Adiciona mais uma linha divisória ao fim da lista

    return ft.Column( 
        controls=controles, # Injeta todos os itens gerados acima
        spacing=0, # Zera o espaçamento automático entre elementos no eixo Y
        scroll=ft.ScrollMode.AUTO, # Permite rolar a lista se a altura da tela for pequena
        alignment=ft.MainAxisAlignment.START, # Empurra os itens para o topo da coluna
    ) 