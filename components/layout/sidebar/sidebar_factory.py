import flet as ft
from components.layout.sidebar.sidebar import Sidebar

def criar_sidebar_desktop(dark_mode, mudar_tela, collapsed=False):
    return Sidebar(dark_mode=dark_mode, mudar_tela=mudar_tela, collapsed=collapsed)

def criar_sidebar_mobile(dark_mode, mudar_tela):
    return ft.Container(
        left=-270, top=0, bottom=0, width=250,
        animate_position=ft.Animation(300, ft.AnimationCurve.EASE_OUT),
        shadow=ft.BoxShadow(blur_radius=25, spread_radius=2, color="#33000000"),
        content=Sidebar(dark_mode=dark_mode, mudar_tela=mudar_tela, collapsed=False)
    )
