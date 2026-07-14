# ==========================================
# components/core/base_page.py
# Página base da aplicação
# ==========================================

import flet as ft

from components.layout.responsive_layout import ResponsiveLayout


class BasePage:

    title = ""
    subtitle = ""

    def __init__(
        self,
        page: ft.Page,
        mudar_tela,
    ):

        self.page = page

        self.layout = ResponsiveLayout(

            page,

            titulo_pagina=self.title,

            subtitulo=self.subtitle,

            mudar_tela=mudar_tela,

        )

    # --------------------------------------

    def build_content(self):

        """
        Deve ser implementado pelas subclasses.
        """

        raise NotImplementedError()

    # --------------------------------------

    def build(self):

        self.layout.add_content(

            self.build_content()

        )

        return self.layout.create_view(
            self.page.route
        )