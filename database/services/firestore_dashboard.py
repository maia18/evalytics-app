import logging as lg
from typing import Optional

from database.services.firebase_config import db
from utils.services.indicadores.indicadores_repository import listar_indicadores


logger = lg.getLogger(__name__)

COLECAO_AVALIACOES = "avaliacoes"


def obter_dados_dashboard() -> dict:
    """
    Obtém os principais indicadores utilizados pelo Dashboard.

    Os dados são calculados diretamente a partir das avaliações
    armazenadas atualmente no Firestore.

    Retorna:
        {
            "avaliacoes": int,
            "respostas": int,
            "cursos": int,
            "media_geral": float,
            "medias_eixos": {
                1: float,
                2: float,
                3: float,
            }
        }
    """

    try:
        # ==========================================================
        # INDICADORES ATIVOS
        # ==========================================================

        indicadores = listar_indicadores()

        indicadores_por_id = {
            indicador.get("id"): indicador
            for indicador in indicadores
            if indicador.get("id")
        }

        # ==========================================================
        # AVALIAÇÕES
        # ==========================================================

        documentos = list(
            db.collection(COLECAO_AVALIACOES).stream()
        )

        quantidade_avaliacoes = len(documentos)

        if not documentos:
            return {
                "avaliacoes": 0,
                "respostas": 0,
                "cursos": 0,
                "media_geral": 0.0,
                "medias_eixos": {},
            }

        # ==========================================================
        # ACUMULADORES
        # ==========================================================

        cursos_avaliados = set()

        quantidade_respostas = 0

        soma_geral = 0.0
        total_notas_geral = 0

        soma_por_eixo: dict[int, float] = {}
        quantidade_por_eixo: dict[int, int] = {}

        # ==========================================================
        # PROCESSAMENTO DAS AVALIAÇÕES
        # ==========================================================

        for documento in documentos:
            dados = documento.to_dict() or {}

            curso_id = dados.get("curso_id")

            if curso_id:
                cursos_avaliados.add(curso_id)

            respostas = dados.get("respostas", {})

            if not isinstance(respostas, dict):
                continue

            for indicador_id, resposta in respostas.items():

                # Ignora respostas inválidas
                try:
                    nota = float(resposta)
                except (TypeError, ValueError):
                    continue

                # Garante que a nota esteja dentro da escala
                # utilizada pelo formulário.
                if nota < 1 or nota > 5:
                    continue

                quantidade_respostas += 1

                soma_geral += nota
                total_notas_geral += 1

                # --------------------------------------------------
                # Identificação do eixo do indicador
                # --------------------------------------------------

                indicador = indicadores_por_id.get(indicador_id)

                if not indicador:
                    continue

                eixo = indicador.get("eixo")

                if eixo is None:
                    continue

                try:
                    eixo = int(eixo)
                except (TypeError, ValueError):
                    continue

                soma_por_eixo[eixo] = (
                    soma_por_eixo.get(eixo, 0.0) + nota
                )

                quantidade_por_eixo[eixo] = (
                    quantidade_por_eixo.get(eixo, 0) + 1
                )

        # ==========================================================
        # MÉDIA GERAL
        # ==========================================================

        media_geral = (
            soma_geral / total_notas_geral
            if total_notas_geral
            else 0.0
        )

        # ==========================================================
        # MÉDIAS POR EIXO
        # ==========================================================

        medias_eixos = {}

        for eixo in sorted(soma_por_eixo):
            quantidade = quantidade_por_eixo.get(eixo, 0)

            if quantidade:
                medias_eixos[eixo] = round(
                    soma_por_eixo[eixo] / quantidade,
                    1,
                )

        # ==========================================================
        # RESULTADO
        # ==========================================================

        return {
            "avaliacoes": quantidade_avaliacoes,
            "respostas": quantidade_respostas,
            "cursos": len(cursos_avaliados),
            "media_geral": round(media_geral, 1),
            "medias_eixos": medias_eixos,
        }

    except Exception:
        logger.exception(
            "Erro ao obter dados do Dashboard."
        )

        return {
            "avaliacoes": 0,
            "respostas": 0,
            "cursos": 0,
            "media_geral": 0.0,
            "medias_eixos": {},
        }


def obter_medias_dashboard() -> Optional[dict[int, float]]:
    """
    Compatibilidade com componentes antigos.

    Retorna somente as médias por eixo.
    """

    dados = obter_dados_dashboard()

    medias = dados.get("medias_eixos", {})

    if not medias:
        return None

    return medias