# ==========================================
# components/layout/menu.py
# Itens do menu lateral
# ==========================================

import flet as ft
from dataclasses import dataclass


@dataclass(frozen=True)
class MenuItemData:
    """Representa um item do menu."""

    icon: str
    title: str
    route: str


MENU_ITEMS = [

    MenuItemData(
        icon=ft.Icons.HOME_OUTLINED,
        title="Início",
        route="/inicio",
    ),

    MenuItemData(
        icon=ft.Icons.ADD_BOX_OUTLINED,
        title="Avaliação",
        route="/avaliacoes",
    ),

    MenuItemData(
        icon=ft.Icons.GRID_VIEW_OUTLINED,
        title="Dashboard",
        route="/dashboard",
    ),

    MenuItemData(
        icon=ft.Icons.SCHOOL_OUTLINED,
        title="Cursos",
        route="/cursos",
    ),

    MenuItemData(
        icon=ft.Icons.PIE_CHART_OUTLINE,
        title="Relatórios",
        route="/relatorios",
    ),

]


SETTINGS_ITEM = MenuItemData(
    icon=ft.Icons.SETTINGS_OUTLINED,
    title="Configurações",
    route="/configuracoes",
)