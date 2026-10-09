import logging as lg
from typing import Optional
from firebase_admin import firestore
from database.services.firebase_config import db

logger = lg.getLogger(__name__)
COLECAO_NOTIFICACOES = "notificacoes"

def adicionar_notificacao(
    tipo: str,
    titulo: str,
    descricao: str,
    usuario_id: str,
) -> Optional[str]:
    try:
        nova_notificacao = {
            "tipo": tipo,
            "titulo": titulo,
            "descricao": descricao,
            "data_criacao": firestore.SERVER_TIMESTAMP,
            "lida": False,
            "usuario_id": usuario_id,
        }

        _, doc_ref = db.collection(COLECAO_NOTIFICACOES).add(
            nova_notificacao
        )

        return doc_ref.id

    except Exception:
        logger.exception("Erro ao adicionar notificação.")
        return None

def listar_notificacoes(usuario_id: str) -> list[dict]:
    try:
        docs = (
            db.collection(COLECAO_NOTIFICACOES)
            .where("usuario_id", "==", usuario_id)
            .stream()
        )

        lista_notificacoes = []

        for doc in docs:
            dado = doc.to_dict()
            dado["id"] = doc.id
            lista_notificacoes.append(dado)

        return lista_notificacoes

    except Exception:
        logger.exception("Erro ao obter notificações.")
        return []

def contar_notificacoes_nao_lidas(usuario_id: str) -> int:
    try:
        docs = (
            db.collection(COLECAO_NOTIFICACOES)
            .where("usuario_id", "==", usuario_id)
            .where("lida", "==", False)
            .stream()
        )

        return sum(1 for _ in docs)

    except Exception:
        logger.exception(
            "Erro ao contar notificações não lidas."
        )
        return 0

def marcar_notificacao_como_lida(
    notificacao_id: str,
) -> bool:
    try:
        (
            db.collection(COLECAO_NOTIFICACOES)
            .document(notificacao_id)
            .update({
                "lida": True,
            })
        )

        return True

    except Exception:
        logger.exception(
            "Erro ao marcar notificação como lida."
        )
        return False

def marcar_todas_como_lidas(
    usuario_id: str,
) -> bool:
    try:
        docs = (
            db.collection(COLECAO_NOTIFICACOES)
            .where("usuario_id", "==", usuario_id)
            .where("lida", "==", False)
            .stream()
        )

        batch = db.batch()
        quantidade = 0

        for doc in docs:
            batch.update(
                doc.reference,
                {"lida": True},
            )
            quantidade += 1

        if quantidade > 0:
            batch.commit()

        return True

    except Exception:
        logger.exception(
            "Erro ao marcar todas as notificações como lidas."
        )
        return False