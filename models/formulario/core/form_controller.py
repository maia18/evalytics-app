import flet as ft
from database.indicadores import INDICADORES
from models.formulario.core.steps import FormularioStepsMixin
from models.formulario.core.render import FormularioRenderMixin

# Controlador responsável por gerenciar o estado e a lógica da tela de Formulário
class FormularioController(FormularioStepsMixin, FormularioRenderMixin):
    def __init__(self, page: ft.Page, mudar_tela, area_dinamica, area_central):
        self.page = page
        self.mudar_tela = mudar_tela
        self.area_dinamica = area_dinamica
        self.area_central = area_central
        
        self.indicadores_ativos = [ind for ind in INDICADORES if ind.get("status", "ATIVO") == "ATIVO"]
        self.estado = {"indice_atual": 0, "respostas": {}}