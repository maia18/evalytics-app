"""
Módulo de Repositório de Indicadores (Facade).
   Este arquivo agrupa as funções de leitura e escrita separadas em módulos menores para manter a retrocompatibilidade com a interface gráfica do sistema.
"""

from utils.services.indicadores.indicadores_queries import (
    buscar_indicador,
    contar_indicadores_por_eixo,
    listar_indicadores_por_eixo,
)
from utils.services.indicadores.indicadores_commands import (
    adicionar_indicador,
    atualizar_indicador,
    atualizar_criterios_indicador,
    excluir_indicador,
)

'''A variável `__all__` garante que quem fizer `from indicadores_repository import *` receba exatamente estas funções'''
__all__ = [
    "buscar_indicador",
    "contar_indicadores_por_eixo",
    "listar_indicadores_por_eixo",
    "adicionar_indicador",
    "atualizar_indicador",
    "atualizar_criterios_indicador",
    "excluir_indicador",
]