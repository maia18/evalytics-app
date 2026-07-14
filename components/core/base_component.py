# ==========================================
# components/core/base_component.py
# Classe base dos componentes
# ==========================================

import flet as ft

from components.theme.theme import get_theme


class BaseComponent:
    """
    Classe base para todos os componentes.

    Disponibiliza automaticamente:

    • page
    • theme
    """

    def __init__(self, page: ft.Page):

        self.page = page

        self.theme = get_theme(
            page.theme_mode == ft.ThemeMode.DARK
        )