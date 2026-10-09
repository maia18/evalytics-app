import flet as ft
from typing import Callable
from components.core.constants.constants import TEXTO_PRINCIPAL
from models.configuracoes.widgets.indicadores_ui import criar_pasta_indicador
from models.configuracoes.widgets.estado_indicadores import EstadoIndicadores
from utils.services.indicadores.indicadores_repository import contar_indicadores_por_eixo

'''
Mapa de Eixos: Centraliza a configuração.
    Se a instituição criar um novo eixo no futuro, basta adicionar uma linha neste dicionário, e a UI será gerada automaticamente.
'''
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
    """
    Gera a visualização inicial da aba de Indicadores (A visualização em formato de Pastas).
        Cada pasta representa um eixo de avaliação institucional.
    """

    return ft.Column(
        expand=True,
        spacing=10,
        controls=[
            # Título da Seção
            ft.Text(
                "Gerenciar Indicadores",
                size=22,
                weight=ft.FontWeight.BOLD,
                color=cores[TEXTO_PRINCIPAL],
            ),

            # Contêiner que agrupa as pastas
            ft.Column(
                expand=True,
                spacing=12, # Espaçamento vertical entre as pastas
                
                # List Comprehension: Cria os componentes de pasta dinamicamente varrendo o dicionário MAPA_EIXOS.
                controls=[
                    criar_pasta_indicador(
                        titulo,
                        
                        # Consulta ao banco para mostrar a tag visual de contagem (ex: "5 indicadores")
                        contar_indicadores_por_eixo(eixo_id), 
                        
                        # Callback que avisará o Layout principal para trocar a tela
                        lambda t=titulo: callback_abrir(t),
                        cores,
                    )
                    for titulo, eixo_id in MAPA_EIXOS.items()
                ],
            ),
        ],
    )