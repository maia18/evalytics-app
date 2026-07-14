# ==========================================
# components/layout/responsive.py
# Responsável por identificar o tamanho da tela
# ==========================================

import flet as ft


class Responsive:

    MOBILE = 700
    DESKTOP = 1100

    @staticmethod
    def is_mobile(page: ft.Page) -> bool:
        return page.width < Responsive.MOBILE

    @staticmethod
    def is_tablet(page: ft.Page) -> bool:
        return Responsive.MOBILE <= page.width < Responsive.DESKTOP

    @staticmethod
    def is_desktop(page: ft.Page) -> bool:
        return page.width >= Responsive.DESKTOP

    @staticmethod
    def sidebar_width(page: ft.Page):

        if Responsive.is_mobile(page):
            return 0

        if Responsive.is_tablet(page):
            return 72

        return 250

    @staticmethod
    def sidebar_collapsed(page: ft.Page):

        return Responsive.is_tablet(page)

    @staticmethod
    def show_hamburger(page: ft.Page):

        return Responsive.is_mobile(page)