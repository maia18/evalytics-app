from typing import Callable

import flet as ft

from database.indicadores import INDICADORES
from models.formulario.core.steps import FormularioStepsMixin
from models.formulario.core.render import FormularioRenderMixin


class FormularioController(FormularioStepsMixin, FormularioRenderMixin):
    """Controller central do formulário: guarda o estado (pergunta atual, respostas)
    e orquestra transições, delegando a montagem visual e a navegação aos mixins.
    """

    def __init__(
        self,
        page: ft.Page,
        mudar_tela: Callable[[str], None],
        area_dinamica: ft.Column,
        area_central: ft.Container,
    ) -> None:
        self.page = page
        self.mudar_tela = mudar_tela
        self.area_dinamica = area_dinamica
        self.area_central = area_central

        # Carrega apenas os indicadores com status "ATIVO"
        self.indicadores_ativos = [
            ind for ind in INDICADORES if ind.get("status", "ATIVO") == "ATIVO"
        ]

        self.estado: dict = {
            "indice_atual": 0,
            "respostas": {},
        }