import logging

from database.services.firebase_config import db
from utils.services.indicadores.indicadores_repository import (
    listar_indicadores,
)

logger = logging.getLogger(__name__)

COLECAO_AVALIACOES = "avaliacoes"

EIXO_PADRAO = 1
EIXOS_PADRAO = (1, 2, 3)


def _obter_mapa_eixos() -> dict[str, int]:
    """
    Monta um mapa relacionando o ID do indicador ao seu eixo.

    Exemplo:
        {
            "abc123": 1,
            "def456": 2,
            "ghi789": 3,
        }
    """

    indicadores = listar_indicadores()

    return {
        indicador["id"]: indicador.get("eixo", EIXO_PADRAO)
        for indicador in indicadores
        if indicador.get("id")
    }


def calcular_medias_eixos() -> dict[int, float]:
    """
    Calcula a média geral das avaliações agrupada por eixo.

    As respostas são relacionadas aos eixos através do ID
    real de cada indicador armazenado no Firestore.
    """

    try:
        mapa_eixo = _obter_mapa_eixos()

        avaliacoes = db.collection(COLECAO_AVALIACOES).stream()

        acumulador: dict[int, list[float]] = {
            eixo: []
            for eixo in EIXOS_PADRAO
        }

        for avaliacao in avaliacoes:
            dados = avaliacao.to_dict()
            respostas = dados.get("respostas", {})

            for indicador_id, nota in respostas.items():
                eixo_id = mapa_eixo.get(indicador_id)

                if eixo_id not in acumulador:
                    continue

                try:
                    acumulador[eixo_id].append(float(nota))
                except (TypeError, ValueError):
                    logger.warning(
                        "Nota inválida ignorada. "
                        "Indicador=%s, nota=%r",
                        indicador_id,
                        nota,
                    )

        return {
            eixo: (
                sum(notas) / len(notas)
                if notas
                else 0.0
            )
            for eixo, notas in acumulador.items()
        }

    except Exception:
        logger.exception(
            "Erro ao calcular médias por eixo."
        )

        return {
            eixo: 0.0
            for eixo in EIXOS_PADRAO
        }


def listar_resultados_consolidados() -> list[dict]:
    """
    Retorna cada avaliação armazenada no Firestore como uma
    linha consolidada para a tabela de resultados.

    Cada item contém:

        {
            "id": "...",
            "curso_id": "...",
            "curso_nome": "...",
            "data_avaliacao": "...",
            "eixos": {
                1: 4.2,
                2: 3.8,
                3: 4.5,
            },
            "media_geral": 4.17,
        }

    A média de cada eixo é calculada a partir das respostas
    dos indicadores pertencentes àquele eixo.
    """

    try:
        mapa_eixo = _obter_mapa_eixos()

        documentos = (
            db.collection(COLECAO_AVALIACOES)
            .stream()
        )

        resultados = []

        for documento in documentos:
            dados = documento.to_dict()

            respostas = dados.get("respostas", {})

            acumulador: dict[int, list[float]] = {
                eixo: []
                for eixo in EIXOS_PADRAO
            }

            for indicador_id, nota in respostas.items():
                eixo_id = mapa_eixo.get(indicador_id)

                if eixo_id not in acumulador:
                    continue

                try:
                    acumulador[eixo_id].append(float(nota))
                except (TypeError, ValueError):
                    logger.warning(
                        "Nota inválida ignorada na avaliação %s. "
                        "Indicador=%s, nota=%r",
                        documento.id,
                        indicador_id,
                        nota,
                    )

            medias_eixos = {
                eixo: (
                    sum(notas) / len(notas)
                    if notas
                    else 0.0
                )
                for eixo, notas in acumulador.items()
            }

            medias_validas = [
                media
                for media in medias_eixos.values()
                if media > 0
            ]

            media_geral = (
                sum(medias_validas) / len(medias_validas)
                if medias_validas
                else 0.0
            )

            resultados.append(
                {
                    "id": documento.id,
                    "curso_id": dados.get("curso_id"),
                    "curso_nome": dados.get(
                        "curso_nome",
                        "Curso não informado",
                    ),
                    "data_avaliacao": dados.get(
                        "data_avaliacao",
                        "",
                    ),
                    "eixos": medias_eixos,
                    "media_geral": media_geral,
                }
            )

        # Mais recentes primeiro.
        resultados.sort(
            key=lambda item: item.get(
                "data_avaliacao",
                ""
            ),
            reverse=True,
        )

        return resultados

    except Exception:
        logger.exception(
            "Erro ao listar resultados consolidados."
        )
        return []