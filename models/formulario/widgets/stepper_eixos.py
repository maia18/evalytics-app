import flet as ft 
from typing import Callable
from components.core.constants.constants import (
    TEXTO_PRINCIPAL,
    TEXTO_SECUNDARIO,
    CARD_SECUNDARIO,
)

def criar_stepper_eixos(
    eixo_atual: int,
    pular_para_eixo: Callable[[int], None],
    cores: dict[str, str],
    dark_mode: bool,
) -> ft.Row:
    """Cria a barra de navegação dos 3 eixos da avaliação."""

    controles = []

    cor_ativo = "#5E35B1" if dark_mode else "#EDE7F6"
    cor_texto_ativo = (
        cores[TEXTO_PRINCIPAL]
        if dark_mode
        else "#512DA8"
    )

    for i in range(1, 4):
        ativo = i == eixo_atual

        controles.append(
            ft.Container(
                content=ft.Text(
                    f"Eixo {i}",
                    color=(
                        cor_texto_ativo
                        if ativo
                        else cores[TEXTO_SECUNDARIO]
                    ),
                    weight="bold",
                ),
                bgcolor=(
                    cor_ativo
                    if ativo
                    else cores[CARD_SECUNDARIO]
                ),
                padding=10,
                border_radius=20,
                ink=True,
                on_click=lambda e, e_alvo=i: (
                    pular_para_eixo(e_alvo)
                ),
            )
        )

    return ft.Row(
        controles,
        alignment=ft.MainAxisAlignment.END,
        spacing=10,
    )