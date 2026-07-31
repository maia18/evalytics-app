from typing import Callable, Optional

import flet as ft

from components.core.constants.constants import HOVER

# Geometria padrão de todos os botões de menu (sidebar completa e colapsada).
ALTURA_BOTAO_MENU = 45
RAIO_BOTAO_MENU = 8
PADDING_BOTAO_MENU = 10

# Cor de hover do botão em modo claro. Não corresponde a COR_BORDA
# (usada como hover geral do tema em AppColors) — divergência histórica,
# mantida como estava para não alterar a aparência atual dos botões.
HOVER_CLARO_BOTAO_MENU = "#CCCCCC"


def criar_botao_menu_base(
    content: ft.Control,
    rota: str,
    dark_mode: bool,
    mudar_tela: Optional[Callable[[str], None]],
    alignment: Optional[ft.Alignment] = None,
    expand: bool = False,
) -> ft.Container:
    """Casca compartilhada de um botão de navegação do menu (sidebar).

    Usada tanto pelo botão só-com-ícone (versão colapsada) quanto pelo
    botão ícone+texto (versão completa) — a diferença entre eles fica
    inteiramente no `content` recebido.
    """
    return ft.Container(
        height=ALTURA_BOTAO_MENU,
        alignment=alignment,
        content=ft.TextButton(
            expand=expand,
            content=content,
            style=ft.ButtonStyle(
                padding=PADDING_BOTAO_MENU,
                shape=ft.RoundedRectangleBorder(radius=RAIO_BOTAO_MENU),
                overlay_color=HOVER if dark_mode else HOVER_CLARO_BOTAO_MENU,
            ),
            on_click=lambda _: mudar_tela(rota) if mudar_tela else None,
        ),
    )