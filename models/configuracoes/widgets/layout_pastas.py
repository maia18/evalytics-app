import flet as ft

from typing import Callable

from components.core.constants.constants import (
    TEXTO_PRINCIPAL,
    TEXTO_SECUNDARIO,
)

from models.configuracoes.widgets.indicadores_ui import (
    criar_pasta_indicador,
)

from models.configuracoes.widgets.estado_indicadores import (
    EstadoIndicadores,
)

from utils.services.indicadores.indicadores_repository import (
    contar_indicadores_por_eixo,
)


# Relaciona o título da interface ao ID inteiro do Eixo
MAPA_EIXOS: dict[str, int] = {
    "Organização Didático-Pedagógica": 1,
    "Corpo Docente e Tutorial": 2,
    "Infraestrutura": 3,
}

<<<<<<< HEAD

def criar_layout_pastas(
    page: ft.Page,
    estado: EstadoIndicadores,
    callback_abrir: Callable[[str], None],
    cores: dict[str, str],
) -> ft.Column:
    """
    Monta a listagem inicial das pastas/eixos.

    Cada pasta representa um eixo da avaliação institucional
    e exibe a quantidade atual de indicadores cadastrados.
    """

    return ft.Column(
        expand=True,
        spacing=25,
        controls=[
            ft.Text(
                "Gerenciar Indicadores",
                size=22,
                weight=ft.FontWeight.BOLD,
                color=cores[TEXTO_PRINCIPAL],
            ),

            ft.Text(
                "Organize os indicadores por eixo de avaliação.",
                size=14,
                color=cores[TEXTO_SECUNDARIO],
            ),

=======
def criar_layout_pastas(
    page: ft.Page, 
    estado: EstadoIndicadores, 
    callback_abrir: Callable[[str], None]
) -> ft.Column:
    """Monta a listagem inicial visual de pastas (uma por eixo), buscando as contagens atualizadas."""
    return ft.Column(
        expand=True, 
        spacing=25,
        controls=[
            ft.Text(
                "Gerenciar Indicadores", 
                size=22, 
                weight="bold", 
                color=ft.Colors.BLACK87
            ),
>>>>>>> ea794a06b2548ae4a0bed3f239fa3214c9fd367e
            ft.Column(
                spacing=15,
                controls=[
                    criar_pasta_indicador(
                        titulo,
                        contar_indicadores_por_eixo(eixo_id),
                        lambda t: callback_abrir(t),
                        cores,
                    )
                    for titulo, eixo_id in MAPA_EIXOS.items()
                ],
            ),
        ],
    )