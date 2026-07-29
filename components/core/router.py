"""Mapeia rotas para as views (páginas) correspondentes da aplicação."""

import flet as ft
import logging as lg
from typing import Callable
'''
Importação dos construtores de tela (Views) de cada módulo do sistema.
Cada um desses imports representa uma função ou classe responsável por desenhar a interface de uma página específica.
'''
from models.configuracoes.configuracoes import ViewConfiguracoes
from models.avaliacoes.avaliacoes import ViewAvaliacoes
from models.relatorios.relatorios import ViewRelatorios
from models.formulario.formulario import ViewFormulario
from models.dashboard.dashboard import ViewDashboard
from models.inicio.inicio import ViewInicio
from models.cursos.cursos import ViewCursos
from models.login.login import ViewLogin

logger = lg.getLogger(__name__)

'''
Definição do Tipo (Type Alias) baseada em um contrato rigoroso:
    Qualquer função de view precisa receber um ft.Page e uma função de navegação (que recebe uma string e retorna None), e obrigatoriamente devolver uma instância de ft.View (a tela pronta do Flet).
'''
ViewBuilder = Callable[[ft.Page, Callable[[str], None]], ft.View]

'''
Constantes que definem os caminhos (paths) da aplicação.
    O uso de constantes previne bugs causados por erros de digitação (ex: "/dshboard") e facilita a alteração de nomes no futuro, centralizando as rotas em um só lugar.
'''
ROTA_LOGIN = "/"
ROTA_INICIO = "/inicio"
ROTA_DASHBOARD = "/dashboard"
ROTA_AVALIACOES = "/avaliacoes"
ROTA_RELATORIOS = "/relatorios"
ROTA_CURSOS = "/cursos"
ROTA_FORMULARIO = "/formulario"
ROTA_CONFIGURACOES = "/configuracoes"

'''
O dicionário ROTAS funciona como uma "Tabela de Roteamento".
Ele vincula diretamente a string da rota (chave) ao construtor da tela (valor).
'''
ROTAS: dict[str, ViewBuilder] = {
    ROTA_LOGIN: ViewLogin,                  # Rota inicial (login)
    ROTA_INICIO: ViewInicio,                # Página principal
    ROTA_DASHBOARD: ViewDashboard,          # Página de Dashboard
    ROTA_AVALIACOES: ViewAvaliacoes,        # Página de avaliações
    ROTA_RELATORIOS: ViewRelatorios,        # Página de relatórios
    ROTA_CURSOS: ViewCursos,                # Página de cursos
    ROTA_FORMULARIO: ViewFormulario,        # Página de formulário
    ROTA_CONFIGURACOES: ViewConfiguracoes,  # Página de configurações
}

def obter_view(rota: str) -> ViewBuilder:
    """
    Retorna a view correspondente à rota informada.
    Caso a rota não exista no mapeamento, retorna ViewLogin como
    fallback e registra um aviso para facilitar o diagnóstico.
    """
    
    view = ROTAS.get(rota) # O método .get() tenta buscar a rota no dicionário. Se ela não existir, ele retorna None (não quebra o código com KeyError).
    if view is None:
        '''
        Padrão de Fallback + Log: se o usuário ou o sistema tentar acessar uma tela que não existe, o aplicativo não crasha. Ele registra um aviso no terminal e joga o usuário de volta para o Login.
            logger.warning("Rota desconhecida: '%s'. Redirecionando para login.", rota)
        '''
        return ViewLogin
        
    return view