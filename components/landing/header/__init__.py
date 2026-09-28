"""
Módulo de exportação do componente Header.

Este arquivo expõe publicamente a função `criar_header`,
permitindo que outros módulos realizem importações mais
simples sem precisar conhecer a estrutura interna de
diretórios do projeto.

Exemplo:

    from components.landing.header import criar_header

Em vez de:

    from components.landing.header.header import criar_header
"""

# Importa a implementação principal do Header.
from components.landing.header.header import criar_header

'''
Define explicitamente quais símbolos serão exportados

    quando alguém utilizar:
        from components.landing.header import *
    
    Isso ajuda a controlar a API pública do módulo e evita exportações acidentais de funções internas.
'''

__all__ = ["criar_header"]