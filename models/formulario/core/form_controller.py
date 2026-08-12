from typing import Callable
import flet as ft

from database.indicadores import INDICADORES
from models.formulario.core.steps import FormularioStepsMixin
from models.formulario.core.render import FormularioRenderMixin

class FormularioController(FormularioStepsMixin, FormularioRenderMixin):
    """
    Controller central do formulário:
        Guarda o estado da pergunta atual e orquestra transições, delegando a montagem visual e a navegação aos mixins.
    """

    def __init__(
        self, page: ft.Page, mudar_tela: Callable[[str], None], area_dinamica: ft.Column, area_central: ft.Container,) -> None:
        self.page = page
        self.mudar_tela = mudar_tela
        self.area_dinamica = area_dinamica
        self.area_central = area_central

        # Filtra a base e carrega apenas os indicadores com status de "ATIVO", ignorando inativos
        self.indicadores_ativos = [
            ind for ind in INDICADORES if ind.get("status", "ATIVO") == "ATIVO"
        ]

        # Estado que monitora em que parte do formulário o usuário está e quais respostas preencheu
        self.estado: dict = {
            "indice_atual": 0,
            "respostas": {},
        }