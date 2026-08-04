import logging

from database.services.firebase_config import db
from utils.services.indicadores_service import listar_indicadores

logger = logging.getLogger(__name__)

COLECAO_AVALIACOES = "avaliacoes"
EIXO_PADRAO = 1  # Assumido quando um indicador não tem eixo definido
EIXOS_PADRAO = (1, 2, 3)


def calcular_medias_eixos() -> dict[int, float]:
    """Calcula a média das avaliações por eixo temático.

    Fluxo:
        1. Lista os indicadores e mapeia cada um ao seu eixo.
        2. Busca todas as avaliações no Firestore.
        3. Agrupa as notas por eixo.
        4. Calcula a média de cada eixo.

    NOTA: esta função espera que `respostas` (dentro de cada avaliação) esteja
    chaveada pelo ID do documento Firestore do indicador. O FormularioController
    atual (form_controller.py) grava as respostas chaveadas pelo TÍTULO do
    indicador, não pelo ID — ou seja, mesmo com dados reais na coleção
    "avaliacoes", o cruzamento de chaves aqui não teria correspondência.
    Ver observação arquitetural na análise deste lote.

    Returns:
        Dicionário {eixo_id: média}.
    """
    try:
        todos_indicadores = listar_indicadores()
        mapa_eixo = {ind['id']: ind.get('eixo', EIXO_PADRAO) for ind in todos_indicadores}

        avaliacoes = db.collection(COLECAO_AVALIACOES).stream()

        acumulador: dict[int, list[float]] = {eixo: [] for eixo in EIXOS_PADRAO}

        for av in avaliacoes:
            respostas = av.to_dict().get("respostas", {})
            for ind_id, nota in respostas.items():
                eixo_id = mapa_eixo.get(ind_id)
                if eixo_id in acumulador:
                    acumulador[eixo_id].append(float(nota))

        return {
            eixo: (sum(notas) / len(notas) if notas else 0.0)
            for eixo, notas in acumulador.items()
        }

    except Exception:
        logger.exception("Erro ao calcular médias por eixo.")
        return {eixo: 0.0 for eixo in EIXOS_PADRAO}