from typing import Callable

import flet as ft


def criar_stepper_eixos(eixo_atual: int, pular_para_eixo: Callable[[int], None]) -> ft.Row:
    """Cria uma barra de navegação em formato de pílulas para os 3 eixos da avaliação.

    Args:
        eixo_atual: o número do eixo onde o usuário se encontra no momento.
        pular_para_eixo: callback disparado ao clicar em um dos botões.
    """
    controles = []

    for i in range(1, 4):
        ativo = i == eixo_atual

        controles.append(
            ft.Container(
                content=ft.Text(f"Eixo {i}", color="onPrimary" if ativo else "onSurface", weight="bold"),
                bgcolor="primary" if ativo else "surfaceVariant",
                padding=10,
                border_radius=20,
                ink=True,
                # `e_alvo=i` congela o valor de `i` no momento da criação do botão
                on_click=lambda e, e_alvo=i: pular_para_eixo(e_alvo),
            )
        )

    return ft.Row(controles, alignment=ft.MainAxisAlignment.END, spacing=10)