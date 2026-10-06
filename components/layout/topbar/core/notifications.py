from datetime import datetime
from typing import Any

import flet as ft

from components.core.auth import auth_state
from utils.services.notificacoes_service import (
    listar_notificacoes as listar_notificacoes_db,
    contar_notificacoes_nao_lidas,
    marcar_todas_como_lidas as marcar_todas_como_lidas_db,
)


def _obter_usuario_id() -> str | None:
    """Obtém o ID do usuário atualmente autenticado."""

    usuario = auth_state.usuario

    if not usuario:
        return None

    return (
        usuario.get("user_id")
        or usuario.get("localId")
    )


def _obter_icone(tipo: str) -> str:
    """Converte o tipo da notificação em um ícone da TopBar."""

    icones = {
        "avaliacao": ft.Icons.RATE_REVIEW_OUTLINED,
        "indicador": ft.Icons.TUNE_OUTLINED,
        "curso": ft.Icons.SCHOOL_OUTLINED,
        "relatorio": ft.Icons.DESCRIPTION_OUTLINED,
        "teste": ft.Icons.NOTIFICATIONS_OUTLINED,
    }

    return icones.get(
        tipo,
        ft.Icons.NOTIFICATIONS_OUTLINED,
    )


def _formatar_tempo(data_criacao: Any) -> str:
    """Converte a data da notificação para uma descrição simples de tempo."""

    if not data_criacao:
        return ""

    try:
        if hasattr(data_criacao, "replace"):
            agora = datetime.now(
                data_criacao.tzinfo
            ) if data_criacao.tzinfo else datetime.now()

            diferenca = agora - data_criacao

            segundos = int(diferenca.total_seconds())

            if segundos < 60:
                return "agora"

            minutos = segundos // 60

            if minutos < 60:
                return (
                    f"há {minutos} minuto"
                    if minutos == 1
                    else f"há {minutos} minutos"
                )

            horas = minutos // 60

            if horas < 24:
                return (
                    f"há {horas} hora"
                    if horas == 1
                    else f"há {horas} horas"
                )

            dias = horas // 24

            if dias == 1:
                return "ontem"

            return (
                f"há {dias} dia"
                if dias == 1
                else f"há {dias} dias"
            )

    except Exception:
        pass

    return ""


def listar_notificacoes() -> list[dict[str, Any]]:
    """Lista as notificações do usuário no formato esperado pela TopBar."""

    usuario_id = _obter_usuario_id()

    if not usuario_id:
        return []

    notificacoes_db = listar_notificacoes_db(
        usuario_id
    )

    notificacoes = []

    for notificacao in notificacoes_db:
        notificacoes.append(
            {
                "id": notificacao.get("id"),
                "icone": _obter_icone(
                    notificacao.get("tipo", "")
                ),
                "titulo": notificacao.get(
                    "titulo",
                    "Notificação",
                ),
                "descricao": notificacao.get(
                    "descricao",
                    "",
                ),
                "tempo": _formatar_tempo(
                    notificacao.get("data_criacao")
                ),
                "lida": notificacao.get(
                    "lida",
                    False,
                ),
            }
        )

    return notificacoes


def contar_nao_lidas() -> int:
    """Retorna a quantidade de notificações não lidas do usuário."""

    usuario_id = _obter_usuario_id()

    if not usuario_id:
        return 0

    return contar_notificacoes_nao_lidas(
        usuario_id
    )


def marcar_todas_como_lidas() -> None:
    """Marca todas as notificações do usuário como lidas."""

    usuario_id = _obter_usuario_id()

    if not usuario_id:
        return

    marcar_todas_como_lidas_db(
        usuario_id
    )