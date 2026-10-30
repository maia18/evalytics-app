import flet as ft
from typing import Callable
from components.landing.palette import FUNDO, FUNDO_CABECALHO

# Componentes da Landing Page
from components.landing.hero import criar_hero
from components.landing.header import criar_header
from components.landing.widgets.cta import criar_cta
from components.landing.sobre import criar_secao_sobre
from components.landing.widgets.footer import criar_rodape
from components.landing.recursos import criar_secao_recursos

def ViewLanding(
    page: ft.Page,
    mudar_tela: Callable[[str], None],
) -> ft.View:
    """Cria e retorna a View principal da Landing Page."""

    # =========================================================
    # NAVEGAÇÃO INTERNA
    # =========================================================

    async def ir_para_recursos(e):
        """Navega até a seção de recursos da Landing Page."""

        await view.scroll_to(
            scroll_key="recursos",
            duration=500,
            curve=ft.AnimationCurve.EASE_IN_OUT,
        )

    async def ir_para_sobre(e):
        """Navega até a seção 'Sobre'."""

        await view.scroll_to(
            scroll_key="sobre",
            duration=500,
            curve=ft.AnimationCurve.EASE_IN_OUT,
        )

    # =========================================================
    # COMPONENTES
    # =========================================================

    header = criar_header(
        page=page,
        mudar_tela=mudar_tela,
        ir_para_recursos=ir_para_recursos,
        ir_para_sobre=ir_para_sobre,
    )

    hero = criar_hero(
        page=page,
        mudar_tela=mudar_tela,
        ir_para_recursos=ir_para_recursos,
    )

    recursos = criar_secao_recursos(page)

    sobre = criar_secao_sobre(page)

    cta = criar_cta(
        page=page,
        mudar_tela=mudar_tela,
    )

    rodape = criar_rodape()

    # =========================================================
    # VIEW
    # =========================================================

    view = ft.View(
        route="/",
        bgcolor=FUNDO_CABECALHO,
        padding=0,
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
        appbar=ft.AppBar(
            title=header,
            toolbar_height=80,
            bgcolor=FUNDO_CABECALHO,
            elevation=0,
            automatically_imply_leading=False,
            title_spacing=0,
        ),
        controls=[
            hero,
            recursos,
            sobre,
            cta,
            rodape,
        ],
    )

    return view
