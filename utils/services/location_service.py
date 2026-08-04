import json
import logging
import urllib.request
from typing import Optional

logger = logging.getLogger(__name__)

URL_API_LOCALIZACAO = "http://ip-api.com/json/"
TIMEOUT_SEGUNDOS = 3
LOCALIZACAO_INDISPONIVEL = "Localização indisponível"

# Cache em memória: a localização não muda durante a sessão do app, então
# evitamos repetir a chamada de rede a cada reconstrução da TopBar (que
# acontece a cada navegação de rota, via Navigator.go()).
_localizacao_em_cache: Optional[str] = None


def obter_localizacao() -> str:
    """Descobre a localização aproximada do usuário (Cidade - Estado) via IP.

    O resultado é armazenado em cache após a primeira busca bem-sucedida,
    evitando requisições de rede repetidas a cada renderização da interface.

    Returns:
        "Cidade - Estado" em caso de sucesso, ou uma mensagem de indisponibilidade.
    """
    global _localizacao_em_cache

    if _localizacao_em_cache is not None:
        return _localizacao_em_cache

    try:
        with urllib.request.urlopen(URL_API_LOCALIZACAO, timeout=TIMEOUT_SEGUNDOS) as resposta:
            dados = json.loads(resposta.read().decode())

            if dados.get("status") == "success":
                cidade = dados.get("city", "")
                estado = dados.get("region", "")
                _localizacao_em_cache = f"{cidade} - {estado}"
                return _localizacao_em_cache

    except Exception:
        logger.warning("Não foi possível obter a localização via IP.", exc_info=True)

    return LOCALIZACAO_INDISPONIVEL