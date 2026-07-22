import flet as ft 
from components.layout.sidebar.sidebar import Sidebar 

def criar_sidebar_desktop(dark_mode, mudar_tela, collapsed=False): 
    """Instancia a Sidebar diretamente no modo Desktop (Fica fixa na tela)."""
    return Sidebar(dark_mode=dark_mode, mudar_tela=mudar_tela, collapsed=collapsed) 

def criar_sidebar_mobile(dark_mode, mudar_tela): 
    """
    Cria a Sidebar de navegação voltada para telas reduzidas (Mobile e Tablets verticais).
    O comportamento muda para um menu deslizante em forma de gaveta (Drawer).
    """
    return ft.Container( 
        left=-270, top=0, bottom=0, width=250, # Posição inicial: Escondida na lateral esquerda, puxada 270px para fora da visão
        animate_position=ft.Animation(300, ft.AnimationCurve.EASE_OUT), # Animação de entrada/saída que dura 300 milissegundos com uma curvatura de alívio suave
        shadow=ft.BoxShadow(blur_radius=25, spread_radius=2, color="#33000000"), # Projeta uma sombra para dar profundidade de janela que flutua sobre a principal
        content=Sidebar(dark_mode=dark_mode, mudar_tela=mudar_tela, collapsed=False) # Injete o componente completo dentro deste "envelope animado"
    ) 