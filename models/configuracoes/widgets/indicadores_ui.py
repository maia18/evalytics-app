"""
Módulo agregador dos componentes de UI de Indicadores (Facade).
    Centraliza as importações dos widgets extraídos para manter a compatibilidade.
"""

# Altere os caminhos de importação conforme a estrutura real de pastas do seu projeto
from models.configuracoes.widgets.linha_indicador import criar_linha_indicador
from models.configuracoes.widgets.pasta_indicador import criar_pasta_indicador

# O __all__ define exatamente quais funções este arquivo disponibiliza para o resto do sistema
__all__ = [
    "criar_linha_indicador",
    "criar_pasta_indicador"
]