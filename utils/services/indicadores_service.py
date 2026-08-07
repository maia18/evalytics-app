import logging
from database.services.firebase_config import db

logger = logging.getLogger(__name__)

'''
ATENÇÃO ARQUITETURAL: 
    Esta é uma coleção Firestore independente do arquivo local (indicadores.py).
    Os dois back-ends não estão sincronizados entre si automaticamente.
'''
COLECAO_INDICADORES = "indicadores"

def listar_indicadores() -> list[dict]:
    """Busca todos os indicadores de avaliação cadastrados no Firestore."""
    
    try:
        docs = db.collection(COLECAO_INDICADORES).stream()
        return [{"id": doc.id, **doc.to_dict()} for doc in docs]

    except Exception:
        logger.exception("Erro ao buscar indicadores.")
        return []

def criar_indicador(nome: str, categoria: str) -> None:
    """Cadastra um novo indicador (pergunta/critério) no Firestore."""
    
    try:
        novo_indicador = {
            "nome": nome,
            "categoria": categoria,
            "ativo": True,  # Soft delete: permite desativar a pergunta sem quebrar relatórios antigos.
        }
        db.collection(COLECAO_INDICADORES).add(novo_indicador)

    except Exception:
        logger.exception("Erro ao criar indicador '%s'.", nome)

def atualizar_indicador(id_indicador: str, novo_nome: str) -> None:
    """Atualiza o nome/texto de um indicador JÁ existente."""
    
    try:
        db.collection(COLECAO_INDICADORES).document(id_indicador).update({"nome": novo_nome}) # O método .update() modifica apenas o campo informado

    except Exception:
        logger.exception("Erro ao atualizar indicador '%s'.", id_indicador)