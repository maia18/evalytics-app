import logging
from database.services.firebase_config import db
from .dashboard_utils import obter_mapa_eixos, normalizar_nota

logger = logging.getLogger(__name__)

COLECAO_AVALIACOES = "avaliacoes"
EIXOS_PADRAO = (1, 2, 3)

def obter_dados_dashboard() -> dict:
    """
    Calcula as métricas principais do Dashboard utilizando o formato atual das avaliações.
    """
    
    resultado_vazio = {
        "avaliacoes": 0,
        "respostas": 0,
        "cursos": 0,
        "media_geral": 0.0,
        "medias_eixos": {},
    }
    
    try:
        # Busca as avaliações no Firestore
        documentos = db.collection(COLECAO_AVALIACOES).stream()
        mapa_eixos = obter_mapa_eixos()

        quantidade_avaliacoes = 0
        quantidade_respostas = 0
        cursos_avaliados: set[str] = set()
        todas_notas: list[float] = []
        notas_por_eixo: dict[int, list[float]] = {
            eixo: [] for eixo in EIXOS_PADRAO
        }

        # Processamento do fluxo de documentos
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
                curso_nome = dados.get("curso_nome")
                if curso_nome:
                    cursos_avaliados.add(f"nome:{curso_nome}")

            # --------------------------------------------------
            # RESPOSTAS E NOTAS
            # --------------------------------------------------
            respostas = dados.get("respostas", {})
            if not isinstance(respostas, dict):
                continue

            quantidade_respostas += len(respostas)

            for indicador_id, valor in respostas.items():
                nota = normalizar_nota(valor)

                if nota is None:
                    continue

                todas_notas.append(nota)

                eixo_id = mapa_eixos.get(str(indicador_id))
                if eixo_id in notas_por_eixo:
                    notas_por_eixo[eixo_id].append(nota)

        # --------------------------------------------------
        # CÁLCULO DE MÉDIAS
        # --------------------------------------------------
        media_geral = (
            sum(todas_notas) / len(todas_notas) if todas_notas else 0.0
        )

        medias_eixos: dict[int, float] = {}
        for eixo_id, notas in notas_por_eixo.items():
            if notas:
                medias_eixos[eixo_id] = round(sum(notas) / len(notas), 2)

        # --------------------------------------------------
        # RESULTADO FINAL
        # --------------------------------------------------
        return {
            "avaliacoes": quantidade_avaliacoes,
            "respostas": quantidade_respostas,
            "cursos": len(cursos_avaliados),
            "media_geral": round(media_geral, 2),
            "medias_eixos": medias_eixos,
        }

    except Exception:
        logger.exception("Erro ao calcular dados do Dashboard.")
        return resultado_vazio