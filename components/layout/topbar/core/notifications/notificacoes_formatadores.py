import flet as ft
from typing import Any
from datetime import datetime

def obter_icone(tipo: str) -> str:
    """Converte o tipo da notificação em um ícone da TopBar."""
    icones = {
        "avaliacao": ft.Icons.RATE_REVIEW_OUTLINED,
        "indicador": ft.Icons.TUNE_OUTLINED,
        "curso": ft.Icons.SCHOOL_OUTLINED,
        "relatorio": ft.Icons.DESCRIPTION_OUTLINED,
        "teste": ft.Icons.NOTIFICATIONS_OUTLINED,
    }

    return icones.get(tipo, ft.Icons.NOTIFICATIONS_OUTLINED)

def formatar_tempo(data_criacao: Any) -> str:
    """Converte a data da notificação para uma descrição simples de tempo."""
    if not data_criacao:
        return ""

    try:
        if hasattr(data_criacao, "replace"):
            agora = datetime.now(data_criacao.tzinfo) if data_criacao.tzinfo else datetime.now()
            diferenca = agora - data_criacao
            segundos = int(diferenca.total_seconds())

            if segundos < 60:
                return "agora"

            minutos = segundos // 60
            if minutos < 60:
                return f"há {minutos} minuto" if minutos == 1 else f"há {minutos} minutos"

            horas = minutos // 60
            if horas < 24:
                return f"há {horas} hora" if horas == 1 else f"há {horas} horas"

            dias = horas // 24
            if dias == 1:
                return "ontem"

            return f"há {dias} dia" if dias == 1 else f"há {dias} dias"

    except Exception:
        pass

    return ""