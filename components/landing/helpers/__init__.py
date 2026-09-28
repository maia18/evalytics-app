"""
Pacote de componentes auxiliares da Landing Page.

Este módulo centraliza a exportação dos helpers visuais
utilizados nas seções da página, permitindo importações
mais simples e desacopladas da estrutura interna do projeto.
"""

# =========================================================
# EXPORTAÇÕES DOS HELPERS
# =========================================================
from components.landing.helpers.etapas import criar_etapa
from components.landing.helpers.recursos import criar_card_recurso
from components.landing.helpers.indicadores import criar_indicador


# =========================================================
# API PÚBLICA DO PACOTE
# =========================================================

'''
    Define explicitamente quais objetos poderão ser importados quando o pacote for utilizado por outros módulos da aplicação.
'''
__all__ = [
    "criar_etapa",
    "criar_card_recurso",
    "criar_indicador",
]