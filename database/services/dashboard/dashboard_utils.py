import logging
from utils.services.indicadores.indicadores_repository import listar_indicadores

logger = logging.getLogger(__name__)

def obter_mapa_eixos() -> dict[str, int]:
    """Cria um mapa relacionando o ID do indicador ao seu eixo."""
    try:
        indicadores = listar_indicadores()

        return {
            indicador["id"]: int(indicador.get("eixo", 1))
            for indicador in indicadores
            if indicador.get("id")
        }

    except Exception:
        logger.exception("Erro ao montar mapa de eixos.")
        return {}

def normalizar_nota(valor) -> float | None:
    """
    Converte uma resposta armazenada no Firestore para float.
        Retorna None quando a resposta não representa uma nota válida.
    """
    try:
        nota = float(valor)
    except (TypeError, ValueError):
        return None

    if not 1.0 <= nota <= 5.0:
        return None

    return nota