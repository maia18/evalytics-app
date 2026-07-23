import flet as ft
from database.indicadores import INDICADORES # Importa o banco de dados/lista local contendo todas as perguntas (indicadores)
# Importa as extensões (Mixins) que fornecem métodos adicionais para esta classe
from models.formulario.core.steps import FormularioStepsMixin
from models.formulario.core.render import FormularioRenderMixin

# Controlador responsável por gerenciar o estado e a lógica da tela de Formulário
# A herança múltipla (Mixins) permite injetar as funcionalidades de "Steps" e "Render" nesta classe principal
class FormularioController(FormularioStepsMixin, FormularioRenderMixin):
    """
    Classe central (Controller) que gerencia o fluxo de preenchimento do formulário.
    Guarda o estado atual (qual pergunta está sendo exibida) e as respostas do usuário.
    """
    
    def __init__(self, page: ft.Page, mudar_tela, area_dinamica, area_central):
        # Referências da interface do usuário (UI) repassadas pela View
        self.page = page 
        self.mudar_tela = mudar_tela # Função de roteamento para navegar entre páginas
        self.area_dinamica = area_dinamica # Container onde as perguntas serão injetadas a cada passo
        self.area_central = area_central # Container pai para controle de alinhamento e scroll

        # Carrega o banco de perguntas, mas filtra (usando list comprehension) 
        # para trazer SOMENTE os indicadores cujo status atual é "ATIVO".
        self.indicadores_ativos = [
            ind for ind in INDICADORES if ind.get("status", "ATIVO") == "ATIVO"
        ]
        
        # Dicionário de Estado da Sessão:
        # 'indice_atual' rastreia em qual pergunta o usuário está (0 é a primeira)
        # 'respostas' armazena os dados coletados ao longo do preenchimento para envio no final
        self.estado = {
            "indice_atual": 0, 
            "respostas": {}
        }