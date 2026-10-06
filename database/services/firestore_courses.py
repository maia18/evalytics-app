import logging as lg

from typing import Optional

from firebase_admin import firestore

from database.services.firebase_config import db
from components.core.auth import auth_state
from utils.services.notificacoes_service import adicionar_notificacao


logger = lg.getLogger(__name__)

COLECAO_CURSOS = "cursos"


def _criar_notificacao_curso(
    titulo: str,
    descricao: str,
) -> None:
    """Cria uma notificação para o usuário autenticado."""

    usuario = auth_state.usuario

    usuario_id = None

    if usuario:
        usuario_id = (
            usuario.get("user_id")
            or usuario.get("localId")
        )

    if not usuario_id:
        logger.warning(
            "Curso foi salvo, mas não foi possível "
            "identificar o usuário para criar a notificação."
        )
        return

    notificacao_id = adicionar_notificacao(
        tipo="curso",
        titulo=titulo,
        descricao=descricao,
        usuario_id=usuario_id,
    )

    if not notificacao_id:
        logger.warning(
            "Curso foi salvo, mas não foi possível "
            "criar a notificação."
        )


def adicionar_curso_db(
    codigo: str,
    nome: str,
    depto: str,
    coord: str,
) -> Optional[str]:
    """
    Adiciona um curso na coleção de cursos.

    Retorna o ID do documento criado,
    ou None em caso de erro.
    """

    try:
        novo_curso = {
            "codigo": codigo,
            "nome": nome,
            "departamento": depto,
            "coordenador": coord,
            "timestamp": firestore.SERVER_TIMESTAMP,
        }

        _, doc_ref = db.collection(
            COLECAO_CURSOS
        ).add(novo_curso)

        logger.info(
            "Curso '%s' adicionado com sucesso.",
            nome,
        )

        _criar_notificacao_curso(
            titulo="Novo curso cadastrado",
            descricao=(
                f"O curso '{nome}' "
                "foi cadastrado com sucesso."
            ),
        )

        return doc_ref.id

    except Exception:
        logger.exception(
            "Erro ao adicionar curso."
        )
        return None


def obter_cursos_db() -> list[dict]:
    """
    Retorna a lista de cursos cadastrados,
    cada um incluindo seu ID de documento.
    """

    try:
        docs = db.collection(
            COLECAO_CURSOS
        ).stream()

        lista_cursos = []

        for doc in docs:
            dado = doc.to_dict()

            dado["id"] = doc.id

            lista_cursos.append(dado)

        return lista_cursos

    except Exception:
        logger.exception(
            "Erro ao obter cursos."
        )
        return []


def atualizar_curso_db(
    doc_id: str,
    nome: str,
    depto: str,
    coord: str,
) -> bool:
    """
    Atualiza um curso existente.

    Retorna True em caso de sucesso.
    """

    try:
        db.collection(
            COLECAO_CURSOS
        ).document(doc_id).update(
            {
                "nome": nome,
                "departamento": depto,
                "coordenador": coord,
            }
        )

        logger.info(
            "Curso '%s' atualizado com sucesso.",
            nome,
        )

        _criar_notificacao_curso(
            titulo="Curso atualizado",
            descricao=(
                f"As informações do curso '{nome}' "
                "foram atualizadas."
            ),
        )

        return True

    except Exception:
        logger.exception(
            "Erro ao atualizar curso."
        )
        return False


def excluir_curso_db(
    doc_id: str,
) -> bool:
    """
    Exclui um curso pelo ID do documento.
        Retorna True em caso de sucesso.
    """

    try:
        curso_ref = db.collection(
            COLECAO_CURSOS
        ).document(doc_id)

        # Recupera os dados antes da exclusão
        curso = curso_ref.get()

        if not curso.exists:
            logger.warning(
                "Curso '%s' não encontrado para exclusão.",
                doc_id,
            )
            return False

        dados_curso = curso.to_dict() or {}
        nome_curso = dados_curso.get(
            "nome",
            doc_id,
        )

        # Exclui o curso
        curso_ref.delete()

        logger.info(
            "Curso '%s' excluído com sucesso.",
            nome_curso,
        )

        # Cria a notificação usando o nome real
        _criar_notificacao_curso(
            titulo="Curso removido",
            descricao=(
                f"O curso '{nome_curso}' "
                "foi removido com sucesso."
            ),
        )

        return True

    except Exception:
        logger.exception(
            "Erro ao excluir curso."
        )
        return False