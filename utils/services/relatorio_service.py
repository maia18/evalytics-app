import logging
from database.services.firebase_config import db
from utils.services.indicadores_service import listar_indicadores

logger = logging.getLogger(__name__)

COLECAO_AVALIACOES = "avaliacoes"
EIXO_PADRAO = 1  # Eixo fallback assumido quando um indicador não tem eixo definido explicitamente.
EIXOS_PADRAO = (1, 2, 3)

def calcular_medias_eixos() -> dict[int, float]:
    """
    Calcula a média das avaliações cruzando dados de Eixos e Notas.

    NOTA ARQUITETURAL: 
        A lógica cruza as respostas pelo ID do indicador, porém o FormularioController atual está gravando usando o TÍTULO do indicador.
        Para que essa função opere corretamente  em produção, é necessário parear as chaves (usar ID em ambos os lados).
    """
    try:
        # Monta um dicionário em memória relacionando o ID de cada indicador ao seu eixo pertencente
        todos_indicadores = listar_indicadores()
        mapa_eixo = {ind['id']: ind.get('eixo', EIXO_PADRAO) for ind in todos_indicadores}

        avaliacoes = db.collection(COLECAO_AVALIACOES).stream()

        # Inicializa o acumulador com listas vazias para receber as notas de cada eixo
        acumulador: dict[int, list[float]] = {eixo: [] for eixo in EIXOS_PADRAO}

        for av in avaliacoes:
            respostas = av.to_dict().get("respostas", {})
            for ind_id, nota in respostas.items():
                eixo_id = mapa_eixo.get(ind_id)
                if eixo_id in acumulador:
                    acumulador[eixo_id].append(float(nota))

        # Resolve a média (soma total dividida pela quantidade), prevenindo erro de divisão por zero
        return {
            eixo: (sum(notas) / len(notas) if notas else 0.0)
            for eixo, notas in acumulador.items()
        }

    except Exception:
        logger.exception("Erro ao calcular médias por eixo.")
        return {eixo: 0.0 for eixo in EIXOS_PADRAO}