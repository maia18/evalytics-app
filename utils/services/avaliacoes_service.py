import logging
from datetime import datetime
from typing import Optional

from database.services.firebase_config import db

logger = logging.getLogger(__name__)

COLECAO_AVALIACOES = "avaliacoes"


def salvar_avaliacao(curso_id: str, curso_nome: str, respostas: dict) -> bool:
    """Salva o formulário de avaliação preenchido no Firestore.

    Args:
        curso_id: identificador único do curso avaliado.
        curso_nome: nome do curso, para leitura humana direta no banco.
        respostas: dicionário no formato {id_do_indicador: nota}.

    Returns:
        True se a gravação for bem-sucedida, False em caso de erro.
    """
    try:
        nova_avaliacao = {
            "curso_id": curso_id,
            "curso_nome": curso_nome,
            "data_avaliacao": datetime.now().isoformat(),  # ISO 8601, ordenável cronologicamente
            "respostas": respostas,
        }
        db.collection(COLECAO_AVALIACOES).add(nova_avaliacao)
        return True

    except Exception:
        logger.exception("Erro ao salvar a avaliação do curso '%s'.", curso_nome)
        return False


def listar_avaliacoes() -> list[dict]:
    """Busca todas as avaliações concluídas armazenadas no Firestore.

    Returns:
        Lista de dicionários, cada um representando uma avaliação com seu ID de documento.
    """
    try:
        docs = db.collection(COLECAO_AVALIACOES).stream()
        return [{"id": doc.id, **doc.to_dict()} for doc in docs]

    except Exception:
        logger.exception("Erro ao buscar avaliações.")
        return []