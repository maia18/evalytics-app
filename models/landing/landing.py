import flet as ft
from typing import Callable

from components.core.constants.constants import COR_FUNDO

from components.landing.header import criar_header
from components.landing.hero import criar_hero
from components.landing.recursos import criar_secao_recursos
from components.landing.sobre import criar_secao_sobre
from components.landing.cta import criar_cta
from components.landing.rodape import criar_rodape

def ViewLanding(
    page: ft.Page,
    mudar_tela: Callable[[str], None],
) -> ft.View:

    # =========================================================
    # NAVEGAÇÃO INTERNA
    # =========================================================

    async def ir_para_recursos(e):

        await view.scroll_to(
            scroll_key="recursos",
            duration=500,
            curve=ft.AnimationCurve.EASE_IN_OUT,
        )

    async def ir_para_sobre(e):

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
        mudar_tela=mudar_tela,
        ir_para_recursos=ir_para_recursos,
    )

    recursos = criar_secao_recursos()

    sobre = criar_secao_sobre()

    cta = criar_cta(
        mudar_tela=mudar_tela,
    )

    rodape = criar_rodape()

    # =========================================================
    # VIEW
    # =========================================================

    view = ft.View(
        route="/",
        bgcolor=COR_FUNDO,
        padding=0,
        scroll=ft.ScrollMode.AUTO,
        controls=[
            header,
            hero,
            recursos,
            sobre,
            cta,
            rodape,
        ],
    )

    return view