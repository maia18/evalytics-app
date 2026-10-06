import logging

from datetime import datetime

from database.services.firebase_config import db
from components.core.auth import auth_state
from utils.services.notificacoes_service import adicionar_notificacao


logger = logging.getLogger(__name__)

COLECAO_AVALIACOES = "avaliacoes"


def salvar_avaliacao(
    curso_id: str,
    curso_nome: str,
    respostas: dict,
) -> bool:
    """Salva o formulário de avaliação preenchido no Firestore."""

    try:
        nova_avaliacao = {
            "curso_id": curso_id,
            "curso_nome": curso_nome,
            "data_avaliacao": datetime.now().isoformat(),
            "respostas": respostas,
        }

        db.collection(COLECAO_AVALIACOES).add(
            nova_avaliacao
        )

        # ---------------------------------------------------------
        # Cria a notificação somente após salvar a avaliação
        # ---------------------------------------------------------

        usuario = auth_state.usuario

        usuario_id = None

        if usuario:
            usuario_id = (
                usuario.get("user_id")
                or usuario.get("localId")
            )

        if usuario_id:
            notificacao_id = adicionar_notificacao(
                tipo="avaliacao",
                titulo="Nova avaliação registrada",
                descricao=(
                    f"A avaliação do curso '{curso_nome}' "
                    "foi registrada com sucesso."
                ),
                usuario_id=usuario_id,
            )

            if not notificacao_id:
                logger.warning(
                    "A avaliação foi salva, mas não foi possível "
                    "criar a notificação."
                )

        else:
            logger.warning(
                "A avaliação foi salva, mas não foi possível "
                "identificar o usuário para criar a notificação."
            )

        return True

    except Exception:
        logger.exception(
            "Erro ao salvar a avaliação do curso '%s'.",
            curso_nome,
        )
        return False


def listar_avaliacoes() -> list[dict]:
    """Busca todas as avaliações concluídas armazenadas no Firestore."""

    try:
        docs = db.collection(COLECAO_AVALIACOES).stream()

        return [
            {
                "id": doc.id,
                **doc.to_dict(),
            }
            for doc in docs
        ]

    except Exception:
        logger.exception(
            "Erro ao buscar avaliações."
        )
        return []
