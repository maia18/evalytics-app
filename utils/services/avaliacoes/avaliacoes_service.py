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
            "data_avaliacao": datetime.now().isoformat(), # Salva o timestamp no padrão ISO 8601
            "respostas": respostas,
        }
        db.collection(COLECAO_AVALIACOES).add(nova_avaliacao) # Adiciona o documento e gera um ID automaticamente.
        return True

    except Exception:
        logger.exception("Erro ao salvar a avaliação do curso '%s'.", curso_nome)
        return False

def listar_avaliacoes() -> list[dict]:
    """Busca todas as avaliações concluídas armazenadas no Firestore."""
    
    try:
        docs = db.collection(COLECAO_AVALIACOES).stream()
        return [{"id": doc.id, **doc.to_dict()} for doc in docs] # Retorna uma lista injetando o ID do documento junto com os dados brutos usando desempacotamento de dicionário (**).

    except Exception:
        logger.exception("Erro ao buscar avaliações.")
        return []