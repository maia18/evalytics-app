import asyncio

import flet as ft

from components.landing.palette import ROXO, ROXO_CLARO


def _criar_nuvem(page: ft.Page, cor: str, topo: int, duracao: int) -> ft.Container:
    nuvem = ft.Container(
        left=-260,
        top=topo,
        width=360,
        height=150,
        border_radius=ft.BorderRadius.all(200),
        gradient=ft.RadialGradient(
            colors=[
                ft.Colors.with_opacity(0.34, cor),
                ft.Colors.with_opacity(0.16, cor),
                ft.Colors.with_opacity(0, cor),
            ],
            stops=[0, 0.42, 1],
        ),
        animate_position=ft.Animation(duracao, ft.AnimationCurve.EASE_IN_OUT_SINE),
    )
    direcao = {"para_direita": True}

    def continuar_fluxo(e):
        if getattr(page, "rota_navegacao_atual", "/") != "/":
            return
        nuvem.left = (page.width or 1280) + 80 if direcao["para_direita"] else -260
        direcao["para_direita"] = not direcao["para_direita"]
        nuvem.update()

    nuvem.on_animation_end = continuar_fluxo

    async def iniciar_fluxo():
        await asyncio.sleep(0.35)
        if getattr(page, "rota_navegacao_atual", "/") == "/":
            nuvem.left = (page.width or 1280) + 80
            direcao["para_direita"] = False
            nuvem.update()

    page.run_task(iniciar_fluxo)
    return nuvem


def criar_fluxo_animado(page: ft.Page, altura_secao: int) -> list[ft.Container]:
    """Luzes decorativas que percorrem o fundo da seção em um loop suave."""
    return [
        _criar_nuvem(page, ROXO, -32, 8200),
        _criar_nuvem(page, ROXO_CLARO, max(0, altura_secao - 150), 10400),
    ]


def preparar_entrada(page: ft.Page, controle: ft.Control, atraso: float) -> ft.Control:
    """Revela o conteúdo com um leve deslocamento e fade, em sequência por seção."""
    controle.opacity = 0
    controle.offset = ft.Offset(0, 0.035)
    controle.animate_opacity = ft.Animation(720, ft.AnimationCurve.EASE_OUT)
    controle.animate_offset = ft.Animation(720, ft.AnimationCurve.EASE_OUT)

    async def revelar():
        await asyncio.sleep(atraso)
        if getattr(page, "rota_navegacao_atual", "/") == "/":
            controle.opacity = 1
            controle.offset = ft.Offset(0, 0)
            controle.update()

    page.run_task(revelar)
    return controle
