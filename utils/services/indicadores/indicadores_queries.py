import logging
from typing import Optional
from database.services.firebase_config import db

logger = logging.getLogger(__name__)
COLECAO_INDICADORES = "indicadores"

def buscar_indicador(titulo: str, eixo: int) -> Optional[dict]:
    """Busca um indicador específico no Firestore através da combinação exata de título e eixo."""
    
    try:
        docs = db.collection(COLECAO_INDICADORES).where("titulo", "==", titulo).where("eixo", "==", eixo).limit(1).stream()
        for doc in docs:
            return {"id": doc.id, **doc.to_dict()}
        return None
    except Exception:
        logger.exception("Erro ao buscar indicador no Firestore.")
        return None


def contar_indicadores_por_eixo(eixo: int) -> int:
    """Calcula a quantidade de indicadores de um eixo consultando a nuvem."""
    
    try:
        docs = db.collection(COLECAO_INDICADORES).where("eixo", "==", eixo).stream()
        return sum(1 for _ in docs)
    except Exception:
        logger.exception("Erro ao contar indicadores no Firestore.")
        return 0


def listar_indicadores_por_eixo(eixo: Optional[int]) -> list[dict]:
    """Filtra e retorna todos os indicadores de uma categoria diretamente do Firestore."""
    
    try:
        docs = db.collection(COLECAO_INDICADORES).where("eixo", "==", eixo).stream()
        return [{"id": doc.id, **doc.to_dict()} for doc in docs]
    except Exception:
        logger.exception("Erro ao listar indicadores por eixo.")
        return []