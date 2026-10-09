import logging
from components.core.auth.auth_state import auth_state
from utils.services.notifications.notificacoes_service import adicionar_notificacao

logger = logging.getLogger(__name__)

def criar_notificacao_curso(titulo: str, descricao: str) -> None:
    """Cria uma notificação para o usuário autenticado relacionada aos cursos."""
    
    usuario = auth_state.usuario
    usuario_id = None

    if usuario:
        usuario_id = usuario.get("user_id") or usuario.get("localId")

    if not usuario_id:
        logger.warning(
            "Ação de curso realizada, mas não foi possível "
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
            "Ação de curso realizada, mas não foi possível "
            "criar a notificação."
        )