import logging

from database.services.firebase_config import db

logger = logging.getLogger(__name__)

# ATENÇÃO: esta constante aponta para a mesma coleção "cursos" usada em
# database/services/firestore_courses.py, porém com um formato de documento
# diferente (nome/modalidade/ativo aqui, vs. codigo/nome/departamento/
# coordenador/timestamp lá). Ver observação arquitetural na análise —
# recomenda-se unificar em um único serviço antes de usar ambos em produção.
COLECAO_CURSOS = "cursos"


def listar_cursos() -> list[dict]:
    """Busca todos os cursos cadastrados na coleção 'cursos' do Firestore.

    Returns:
        Lista de dicionários, cada um representando um curso com seu ID de documento.
    """
    try:
        docs = db.collection(COLECAO_CURSOS).stream()
        return [{"id": doc.id, **doc.to_dict()} for doc in docs]

    except Exception:
        logger.exception("Erro ao buscar cursos.")
        return []


def criar_curso(nome: str, modalidade: str) -> None:
    """Cadastra um novo curso no Firestore.

    Args:
        nome: nome oficial do curso (ex: "Sistemas de Informação").
        modalidade: formato de ensino (ex: "Presencial", "EAD", "Híbrido").
    """
    try:
        novo_curso = {
            "nome": nome,
            "modalidade": modalidade,
            "ativo": True,  # Permite ocultar o curso futuramente sem perder o histórico
        }
        db.collection(COLECAO_CURSOS).add(novo_curso)

    except Exception:
        logger.exception("Erro ao criar curso '%s'.", nome)