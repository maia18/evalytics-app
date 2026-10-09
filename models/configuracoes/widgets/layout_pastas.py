import flet as ft
from typing import Callable
from components.core.constants.constants import (
    TEXTO_PRINCIPAL,
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

def criar_layout_pastas(
    page: ft.Page,
    estado: EstadoIndicadores,
    callback_abrir: Callable[[str], None],
    cores: dict[str, str],
) -> ft.Column:

    return ft.Column(
        expand=True,
        spacing=10,
        controls=[
            ft.Text(
                "Gerenciar Indicadores",
                size=22,
                weight=ft.FontWeight.BOLD,
                color=cores[TEXTO_PRINCIPAL],
            ),

            ft.Column(
                expand=True,
                spacing=12,
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