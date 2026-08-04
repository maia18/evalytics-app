import logging
from datetime import datetime

from database.services.firebase_config import db

logger = logging.getLogger(__name__)

COLECAO_AVALIACOES = "avaliacoes"

def salvar_avaliacao(curso_id: str, curso_nome: str, respostas: dict) -> bool:
    """Salva o formulário de avaliação preenchido no Firestore."""
    try:
        nova_avaliacao = {
            "curso_id": curso_id,
            "curso_nome": curso_nome,
            # Salva o timestamp no padrão ISO 8601, que é excelente para ordenação cronológica e leitura em APIs.
            "data_avaliacao": datetime.now().isoformat(),
            "respostas": respostas,
        }
        # Adiciona o documento e gera um ID automaticamente.
        db.collection(COLECAO_AVALIACOES).add(nova_avaliacao)
        return True

    except Exception:
        logger.exception("Erro ao salvar a avaliação do curso '%s'.", curso_nome)
        return False

def listar_avaliacoes() -> list[dict]:
    """Busca todas as avaliações concluídas armazenadas no Firestore."""
    try:
        docs = db.collection(COLECAO_AVALIACOES).stream()
        # Retorna uma lista injetando o ID do documento junto com os dados brutos usando desempacotamento de dicionário (**).
        return [{"id": doc.id, **doc.to_dict()} for doc in docs]

    except Exception:
        logger.exception("Erro ao buscar avaliações.")
        return []