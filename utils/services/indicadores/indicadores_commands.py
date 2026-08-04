import logging
from typing import Optional

from database.services.firebase_config import db
from utils.services.indicadores.indicadores_queries import buscar_indicador

logger = logging.getLogger(__name__)
COLECAO_INDICADORES = "indicadores"


def adicionar_indicador(titulo: str, eixo: Optional[int], descricao: str) -> None:
    """Cria e persiste um novo indicador na nuvem."""
    try:
        novo_item = {
            "titulo": titulo,
            "eixo": eixo,
            "descricao": descricao,
            "status": "ATIVO",
            "criterios": {str(i): "" for i in range(1, 6)},
        }
        db.collection(COLECAO_INDICADORES).add(novo_item)
    except Exception:
        logger.exception("Erro ao adicionar indicador ao Firestore.")


def atualizar_indicador(titulo_atual: str, eixo: int, novo_titulo: str, nova_descricao: str) -> bool:
    """Altera campos textuais básicos (Título e Descrição) de um indicador existente."""
    try:
        indicador = buscar_indicador(titulo_atual, eixo)
        if not indicador:
            return False

        doc_ref = db.collection(COLECAO_INDICADORES).document(indicador["id"])
        doc_ref.update({
            "titulo": novo_titulo,
            "descricao": nova_descricao
        })
        return True
    except Exception:
        logger.exception("Erro ao atualizar indicador no Firestore.")
        return False


def atualizar_criterios(titulo: str, eixo: int, novos_criterios: dict) -> bool:
    """Substitui a árvore de textos correspondente às notas (critérios) do indicador."""
    try:
        indicador = buscar_indicador(titulo, eixo)
        if not indicador:
            return False

        doc_ref = db.collection(COLECAO_INDICADORES).document(indicador["id"])
        doc_ref.update({"criterios": novos_criterios})
        return True
    except Exception:
        logger.exception("Erro ao atualizar critérios no Firestore.")
        return False


def excluir_indicador(titulo: str, eixo: int) -> bool:
    """Remove permanentemente o indicador da coleção na nuvem."""
    try:
        indicador = buscar_indicador(titulo, eixo)
        if not indicador:
            return False

        doc_ref = db.collection(COLECAO_INDICADORES).document(indicador["id"])
        doc_ref.delete()
        return True
    except Exception:
        logger.exception("Erro ao excluir indicador no Firestore.")
        return False