import flet as ft
from typing import Callable

from utils.services.indicadores.indicadores_repository import contar_indicadores_por_eixo
from models.configuracoes.widgets.indicadores_ui import criar_pasta_indicador
from models.configuracoes.widgets.estado_indicadores import EstadoIndicadores

# Relaciona o título da interface ao ID inteiro do Eixo esperado pelo repositório
MAPA_EIXOS: dict[str, int] = {
    "Organização Didático-Pedagógica": 1,
    "Corpo Docente e Tutorial": 2,
    "Infraestrutura": 3,
}

def criar_layout_pastas(page: ft.Page, estado: EstadoIndicadores, callback_abrir: Callable[[str], None]) -> ft.Column:
    """
    Monta a listagem inicial visual de pastas (uma por eixo), buscando as contagens atualizadas.
    Recebe 'callback_abrir' por parâmetro para evitar importações circulares.
    """
    return ft.Column(
        expand=True, spacing=25,
        controls=[
            ft.Text("Gerenciar Indicadores", size=22, weight="bold", color=ft.Colors.BLACK87),
            ft.Column(
                spacing=15,
                controls=[
                    # Gera as pastas iterando no dicionário MAPA_EIXOS[cite: 60]
                    criar_pasta_indicador(
                        titulo, contar_indicadores_por_eixo(eixo_id),
                        lambda t: callback_abrir(t),
                    ) 
                    for titulo, eixo_id in MAPA_EIXOS.items()
                ],
            ),
        ],
    )