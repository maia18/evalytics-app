from typing import Callable, Optional

import flet as ft


class EstadoIndicadores:
    """Estado compartilhado entre a listagem de pastas/indicadores e os modais de gerenciamento.

    Substitui os dicionários soltos `pasta_aberta_atualmente` e `item_alvo_acao`,
    e centraliza as referências às funções que abrem cada modal e ao container
    de conteúdo da aba ativa — evitando que sejam repassadas (e, em alguns
    casos, esquecidas como None) através de várias camadas de lambdas.
    """

    def __init__(self) -> None:
        self.pasta_titulo: str = ""
        self.pasta_eixo: Optional[int] = 0
        self.item_alvo: dict = {}

        # Preenchidos por ViewConfiguracoes após a criação dos modais e das abas
        self.area_conteudo_aba: Optional[ft.Container] = None
        self.abrir_modal_novo: Optional[Callable[[], None]] = None
        self.abrir_modal_criterios: Optional[Callable[..., None]] = None
        self.abrir_modal_edicao: Optional[Callable[..., None]] = None
        self.preparar_exclusao: Optional[Callable[[dict], None]] = None

    def definir_pasta_aberta(self, titulo: str, eixo: Optional[int]) -> None:
        self.pasta_titulo = titulo
        self.pasta_eixo = eixo

    def definir_item_alvo(self, item: dict) -> None:
        self.item_alvo = dict(item)