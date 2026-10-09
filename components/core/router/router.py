"""Mapeia rotas para as views (páginas) correspondentes da aplicação."""

import flet as ft
import logging as lg
from typing import Callable

# Constantes de rotas
from .rotas_cts import (
    ROTA_INICIAL,
    ROTA_LOGIN,
    ROTA_INICIO,
    ROTA_DASHBOARD,
    ROTA_AVALIACOES,
    ROTA_RELATORIOS,
    ROTA_CURSOS,
    ROTA_FORMULARIO,
    ROTA_CONFIGURACOES,
)

# Construtores de tela (Views)
from components.landing.landing import ViewLanding
from models.login.login import ViewLogin
from models.inicio.inicio import ViewInicio
from models.cursos.cursos import ViewCursos
from models.dashboard.dashboard import ViewDashboard
from models.avaliacoes.avaliacoes import ViewAvaliacoes
from models.relatorios.relatorios import ViewRelatorios
from models.formulario.formulario import ViewFormulario
from models.configuracoes.configuracoes import ViewConfiguracoes

logger = lg.getLogger(__name__)

# Definição do Tipo (Type Alias) de acordo com o contrato
ViewBuilder = Callable[[ft.Page, Callable[[str], None]], ft.View]

'''
Tabela de Roteamento:
    Vincula diretamente a string da rota (chave) ao construtor da tela (valor).
'''
ROTAS: dict[str, ViewBuilder] = {
    ROTA_INICIAL: ViewLanding,
    ROTA_LOGIN: ViewLogin,
    ROTA_INICIO: ViewInicio,
    ROTA_DASHBOARD: ViewDashboard,
    ROTA_AVALIACOES: ViewAvaliacoes,
    ROTA_RELATORIOS: ViewRelatorios,
    ROTA_CURSOS: ViewCursos,
    ROTA_FORMULARIO: ViewFormulario,
    ROTA_CONFIGURACOES: ViewConfiguracoes,
}

def obter_view(rota: str) -> ViewBuilder:
    """
    Retorna a view correspondente à rota informada.
        Caso a rota não exista no mapeamento, retorna ViewLogin como fallback e registra um aviso para facilitar o diagnóstico.
    """
    view = ROTAS.get(rota)
    
    if view is None:
        # Padrão de Fallback + Log para rotas inexistentes
        logger.warning("Rota desconhecida: '%s'. Redirecionando para login.", rota)
        return ViewLogin
        
    return view