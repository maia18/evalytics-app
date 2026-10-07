import logging

from database.services.firebase_config import db
from utils.services.indicadores.indicadores_repository import (
    listar_indicadores,
)

logger = logging.getLogger(__name__)

COLECAO_AVALIACOES = "avaliacoes"

EIXOS_PADRAO = (1, 2, 3)


# ==========================================================
# MAPA DOS INDICADORES
# ==========================================================

def _obter_mapa_eixos() -> dict[str, int]:
    """
    Cria um mapa relacionando o ID do indicador ao seu eixo.

    Exemplo:

        {
            "abc123": 1,
            "def456": 1,
            "ghi789": 3,
        }
    """

    try:
        indicadores = listar_indicadores()

        return {
            indicador["id"]: int(indicador.get("eixo", 1))
            for indicador in indicadores
            if indicador.get("id")
        }

    except Exception:
        logger.exception(
            "Erro ao montar mapa de eixos."
        )
        return {}


# ==========================================================
# NORMALIZAÇÃO DAS NOTAS
# ==========================================================

def _normalizar_nota(valor) -> float | None:
    """
    Converte uma resposta armazenada no Firestore
    para float.

    Retorna None quando a resposta não representa
    uma nota válida.
    """

    try:
        nota = float(valor)
    except (TypeError, ValueError):
        return None

    if not 1.0 <= nota <= 5.0:
        return None

    return nota


# ==========================================================
# DADOS PRINCIPAIS DO DASHBOARD
# ==========================================================

def obter_dados_dashboard() -> dict:
    """
    Calcula as métricas principais do Dashboard
    utilizando o formato atual das avaliações.

    Métricas:

        avaliações
            Quantidade de documentos da coleção.

        respostas
            Quantidade total de respostas registradas
            dentro dos documentos.

        cursos
            Quantidade de cursos distintos avaliados.

        media_geral
            Média de todas as respostas válidas.

        medias_eixos
            Média das respostas agrupadas pelos
            respectivos eixos dos indicadores.
    """

    resultado_vazio = {
        "avaliacoes": 0,
        "respostas": 0,
        "cursos": 0,
        "media_geral": 0.0,
        "medias_eixos": {},
    }

    try:
        # --------------------------------------------------
        # BUSCA AS AVALIAÇÕES
        # --------------------------------------------------

        documentos = (
            db.collection(COLECAO_AVALIACOES)
            .stream()
        )

        mapa_eixos = _obter_mapa_eixos()

        quantidade_avaliacoes = 0
        quantidade_respostas = 0

        cursos_avaliados: set[str] = set()

        todas_notas: list[float] = []

        notas_por_eixo: dict[int, list[float]] = {
            eixo: []
            for eixo in EIXOS_PADRAO
        }

        # --------------------------------------------------
        # PROCESSAMENTO
        # --------------------------------------------------

        for documento in documentos:

            dados = documento.to_dict() or {}

            quantidade_avaliacoes += 1

            # --------------------------------------------------
            # CURSO
            # --------------------------------------------------

            curso_id = dados.get("curso_id")

            if curso_id:
                cursos_avaliados.add(str(curso_id))

            else:
                # Fallback para documentos antigos
                # que eventualmente possuam somente curso_nome.
                curso_nome = dados.get("curso_nome")

                if curso_nome:
                    cursos_avaliados.add(
                        f"nome:{curso_nome}"
                    )

            # --------------------------------------------------
            # RESPOSTAS
            # --------------------------------------------------

            respostas = dados.get(
                "respostas",
                {},
            )

            if not isinstance(respostas, dict):
                continue

            # Cada item dentro de "respostas"
            # representa uma resposta a um indicador.
            quantidade_respostas += len(respostas)

            # --------------------------------------------------
            # DISTRIBUIÇÃO DAS NOTAS
            # --------------------------------------------------

            for indicador_id, valor in respostas.items():

                nota = _normalizar_nota(valor)

                if nota is None:
                    continue

                # Média geral
                todas_notas.append(nota)

                # Descobre o eixo do indicador
                eixo_id = mapa_eixos.get(
                    str(indicador_id)
                )

                if eixo_id not in notas_por_eixo:
                    continue

                notas_por_eixo[eixo_id].append(
                    nota
                )

        # --------------------------------------------------
        # MÉDIA GERAL
        # --------------------------------------------------

        media_geral = (
            sum(todas_notas) / len(todas_notas)
            if todas_notas
            else 0.0
        )

        # --------------------------------------------------
        # MÉDIAS POR EIXO
        # --------------------------------------------------

        medias_eixos: dict[int, float] = {}

        for eixo_id, notas in notas_por_eixo.items():

            # Só adiciona o eixo se realmente houver
            # respostas para ele.
            if notas:
                medias_eixos[eixo_id] = round(
                    sum(notas) / len(notas),
                    2,
                )

        # --------------------------------------------------
        # RESULTADO FINAL
        # --------------------------------------------------

        return {
            "avaliacoes": quantidade_avaliacoes,
            "respostas": quantidade_respostas,
            "cursos": len(cursos_avaliados),
            "media_geral": round(
                media_geral,
                2,
            ),
            "medias_eixos": medias_eixos,
        }

    except Exception:
        logger.exception(
            "Erro ao calcular dados do Dashboard."
        )

        return resultado_vazio