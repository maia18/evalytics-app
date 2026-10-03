import logging

from database.services.firebase_config import db
from utils.services.indicadores.indicadores_repository import (
    listar_indicadores,
)

logger = logging.getLogger(__name__)

COLECAO_AVALIACOES = "avaliacoes"

EIXO_PADRAO = 1
EIXOS_PADRAO = (1, 2, 3)


# ==========================================================
# MAPA DOS INDICADORES
# ==========================================================

def _obter_mapa_eixos() -> dict[str, int]:
    """
    Cria um mapa relacionando o ID do indicador ao seu eixo.
    """

    try:
        indicadores = listar_indicadores()

        return {
            indicador["id"]: indicador.get(
                "eixo",
                EIXO_PADRAO,
            )
            for indicador in indicadores
            if indicador.get("id")
        }

    except Exception:
        logger.exception(
            "Erro ao montar mapa de eixos."
        )
        return {}


# ==========================================================
# UTILITÁRIOS DE DATA / SEMESTRE
# ==========================================================

def _obter_semestre(data_iso: str) -> str:
    """
    Converte uma data ISO para o semestre acadêmico.

    Exemplos:
        2026-02-15 -> 2026.1
        2026-08-20 -> 2026.2
    """

    if not data_iso:
        return ""

    try:
        ano = int(data_iso[:4])
        mes = int(data_iso[5:7])

        semestre = "1" if mes <= 6 else "2"

        return f"{ano}.{semestre}"

    except (ValueError, TypeError):
        return ""


def listar_semestres_disponiveis() -> list[str]:
    """
    Retorna os semestres encontrados nas avaliações reais
    armazenadas no Firestore.
    """

    try:
        documentos = (
            db.collection(COLECAO_AVALIACOES)
            .stream()
        )

        semestres = set()

        for documento in documentos:

            dados = documento.to_dict()

            data_avaliacao = dados.get(
                "data_avaliacao",
                "",
            )

            semestre = _obter_semestre(
                data_avaliacao
            )

            if semestre:
                semestres.add(semestre)

        return sorted(
            semestres,
            reverse=True,
        )

    except Exception:
        logger.exception(
            "Erro ao listar semestres disponíveis."
        )
        return []


# ==========================================================
# DASHBOARD EXECUTIVO
# ==========================================================

def calcular_medias_eixos(
    semestre: str | None = None,
    eixo: int | None = None,
) -> dict[int, float | None]:
    """
    Calcula as médias das avaliações por eixo.

    Filtros opcionais:
        semestre:
            Ex.: "2026.2"

        eixo:
            1, 2 ou 3.

    Retorno:
        {
            1: 2.5,
            2: None,
            3: None,
        }

    None significa que não existem respostas para aquele eixo.
    """

    try:
        mapa_eixo = _obter_mapa_eixos()

        avaliacoes = (
            db.collection(COLECAO_AVALIACOES)
            .stream()
        )

        acumulador: dict[int, list[float]] = {
            eixo_id: []
            for eixo_id in EIXOS_PADRAO
        }

        for avaliacao in avaliacoes:

            dados = avaliacao.to_dict()

            # --------------------------------------------------
            # FILTRO DE SEMESTRE
            # --------------------------------------------------

            data_avaliacao = dados.get(
                "data_avaliacao",
                "",
            )

            semestre_avaliacao = _obter_semestre(
                data_avaliacao
            )

            if semestre:
                if semestre_avaliacao != semestre:
                    continue

            # --------------------------------------------------
            # RESPOSTAS
            # --------------------------------------------------

            respostas = dados.get(
                "respostas",
                {},
            )

            if not isinstance(respostas, dict):
                continue

            # --------------------------------------------------
            # DISTRIBUI RESPOSTAS PELOS EIXOS
            # --------------------------------------------------

            for indicador_id, nota in respostas.items():

                eixo_id = mapa_eixo.get(indicador_id)

                if eixo_id not in acumulador:
                    continue

                # Se um eixo específico foi selecionado,
                # ignoramos os demais.
                if eixo is not None and eixo_id != eixo:
                    continue

                try:
                    acumulador[eixo_id].append(
                        float(nota)
                    )
                except (TypeError, ValueError):
                    continue

        # ------------------------------------------------------
        # MÉDIAS
        # ------------------------------------------------------

        return {
            eixo_id: (
                sum(notas) / len(notas)
                if notas
                else None
            )
            for eixo_id, notas in acumulador.items()
        }

    except Exception:
        logger.exception(
            "Erro ao calcular médias dos eixos."
        )

        return {
            eixo_id: None
            for eixo_id in EIXOS_PADRAO
        }

# ==========================================================
# RESULTADOS CONSOLIDADOS
# ==========================================================

def listar_resultados_consolidados(
    semestre: str | None = None,
    eixo: int | None = None,
) -> list[dict]:
    """
    Retorna avaliações consolidadas por eixo.

    Filtros opcionais:

        semestre:
            Exemplo: "2026.1"

        eixo:
            1, 2 ou 3

    A média geral considera somente os eixos
    que possuem respostas.
    """

    try:
        mapa_eixo = _obter_mapa_eixos()

        documentos = (
            db.collection(COLECAO_AVALIACOES)
            .stream()
        )

        resultados: list[dict] = []

        for documento in documentos:

            dados = documento.to_dict()

            data_avaliacao = dados.get(
                "data_avaliacao",
                "",
            )

            # --------------------------------------------------
            # FILTRO DE SEMESTRE
            # --------------------------------------------------

            semestre_avaliacao = _obter_semestre(
                data_avaliacao
            )

            if semestre:
                if semestre_avaliacao != semestre:
                    continue

            # --------------------------------------------------
            # RESPOSTAS
            # --------------------------------------------------

            respostas = dados.get(
                "respostas",
                {},
            )

            if not isinstance(respostas, dict):
                respostas = {}

            acumulador: dict[int, list[float]] = {
                eixo_id: []
                for eixo_id in EIXOS_PADRAO
            }

            # --------------------------------------------------
            # DISTRIBUI RESPOSTAS PELOS EIXOS
            # --------------------------------------------------

            for indicador_id, nota in respostas.items():

                eixo_id = mapa_eixo.get(indicador_id)

                if eixo_id not in acumulador:
                    continue

                try:
                    acumulador[eixo_id].append(
                        float(nota)
                    )
                except (TypeError, ValueError):
                    continue

            # --------------------------------------------------
            # FILTRO DE EIXO
            # --------------------------------------------------

            if eixo is not None:

                if eixo not in acumulador:
                    continue

                if not acumulador[eixo]:
                    continue

            # --------------------------------------------------
            # MÉDIAS DOS EIXOS
            # --------------------------------------------------

            medias_eixos: dict[int, float] = {}

            for eixo_id in EIXOS_PADRAO:

                notas = acumulador[eixo_id]

                medias_eixos[eixo_id] = (
                    sum(notas) / len(notas)
                    if notas
                    else 0.0
                )

            # --------------------------------------------------
            # MÉDIA GERAL
            # --------------------------------------------------

            medias_respondidas = [
                medias_eixos[eixo_id]
                for eixo_id in EIXOS_PADRAO
                if acumulador[eixo_id]
            ]

            media_geral = (
                sum(medias_respondidas)
                / len(medias_respondidas)
                if medias_respondidas
                else 0.0
            )

            # --------------------------------------------------
            # RESULTADO
            # --------------------------------------------------

            resultados.append(
                {
                    "id": documento.id,

                    "curso_id": dados.get(
                        "curso_id",
                        "",
                    ),

                    "curso_nome": dados.get(
                        "curso_nome",
                        "",
                    ),

                    "data_avaliacao": data_avaliacao,

                    "semestre": semestre_avaliacao,

                    "eixos": {
                        1: medias_eixos[1],
                        2: medias_eixos[2],
                        3: medias_eixos[3],
                    },

                    "media_geral": media_geral,
                }
            )

        return resultados

    except Exception:
        logger.exception(
            "Erro ao listar resultados consolidados."
        )

        return []


# ==========================================================
# COMPATIBILIDADE
# ==========================================================

def listar_resultados_avaliacoes() -> list[dict]:
    """
    Mantém compatibilidade com chamadas antigas.
    """

    return listar_resultados_consolidados()

# ==========================================================
# FILTROS DOS RELATÓRIOS
# ==========================================================

def filtrar_resultados(
    resultados: list[dict],
    semestre: str | None = None,
    eixo: int | None = None,
) -> list[dict]:
    """
    Filtra os resultados consolidados por semestre e/ou eixo.

    O semestre é obtido a partir da data da avaliação.

    Janeiro a junho:
        YYYY.1

    Julho a dezembro:
        YYYY.2
    """

    filtrados: list[dict] = []

    for resultado in resultados:

        # --------------------------------------------------
        # FILTRO DE SEMESTRE
        # --------------------------------------------------

        if semestre:

            data_avaliacao = resultado.get(
                "data_avaliacao",
                "",
            )

            if not data_avaliacao:
                continue

            try:
                ano = int(data_avaliacao[:4])
                mes = int(data_avaliacao[5:7])

                semestre_resultado = (
                    f"{ano}.1"
                    if mes <= 6
                    else f"{ano}.2"
                )

            except (ValueError, TypeError):
                continue

            if semestre_resultado != semestre:
                continue

        # --------------------------------------------------
        # FILTRO DE EIXO
        # --------------------------------------------------

        if eixo is not None:

            eixos = resultado.get("eixos", {})

            if not isinstance(eixos, dict):
                continue

            nota_eixo = eixos.get(eixo)

            if nota_eixo is None:
                continue

            try:
                nota_eixo = float(nota_eixo)
            except (TypeError, ValueError):
                continue

            # Sem resposta para o eixo selecionado.
            if nota_eixo <= 0:
                continue

        filtrados.append(resultado)

    return filtrados