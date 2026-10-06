import flet as ft
from typing import Callable, Optional

from components.core.theme.theme_config import configurar_tema


def toggle_dark_mode(
    page: ft.Page,
    dark_mode: bool,
    mudar_tela: Optional[Callable[[str], None]],
    rota_atual: Optional[str],
) -> bool:
    """
    Alterna entre os temas claro e escuro.

    A tela atual é reconstruída após a troca do tema para que
    os componentes recebam novamente as cores correspondentes
    ao novo tema.

    O estado de uma avaliação em andamento é preservado pelo
    FormularioController, que é reutilizado pela tela /formulario.
    """

    # ==========================================================
    # INVERTE O TEMA ATUAL
    # ==========================================================

    dark_mode = not dark_mode

    page.is_dark_mode = dark_mode

    # ==========================================================
    # APLICA AS CORES DO NOVO TEMA
    # ==========================================================

    configurar_tema(
        page,
        dark_mode,
    )

    # ==========================================================
    # RECONSTRÓI A TELA ATUAL
    # ==========================================================

    if mudar_tela and rota_atual:
        mudar_tela(rota_atual)

    else:
        # Fallback caso não exista uma rota para reconstruir.
        page.update()

    return dark_mode