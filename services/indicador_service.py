from repositories.indicador_repository import (
    listar,
    listar_por_eixo
)


def listar_indicadores():
    return listar()


def listar_indicadores_por_eixo(eixo: int):
    return listar_por_eixo(eixo)