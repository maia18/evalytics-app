import json
import logging
import urllib.request
from typing import Optional

logger = logging.getLogger(__name__)

URL_API_LOCALIZACAO = "http://ip-api.com/json/"
TIMEOUT_SEGUNDOS = 3
LOCALIZACAO_INDISPONIVEL = "Localização indisponível"

'''
Variável de Cache em memória.
    Como o app redesenha a TopBar a cada mudança de tela, isso impede que a API seja chamada excessivamente e atinja limites de requisição (Rate Limit).
'''
_localizacao_em_cache: Optional[str] = None

def obter_localizacao() -> str:
    """Descobre a localização aproximada do usuário (Cidade - Estado) via IP consumindo API REST pública."""
    
    global _localizacao_em_cache

    if _localizacao_em_cache is not None:
        return _localizacao_em_cache # Retorna imediatamente se já fez a busca antes com sucesso

    try:
        # Request HTTP usando biblioteca nativa do Python com Timeout de segurança
        with urllib.request.urlopen(URL_API_LOCALIZACAO, timeout=TIMEOUT_SEGUNDOS) as resposta:
            dados = json.loads(resposta.read().decode())

            if dados.get("status") == "success":
                cidade = dados.get("city", "")
                estado = dados.get("region", "")
                
                # Salva o resultado no Cache e devolve
                _localizacao_em_cache = f"{cidade} - {estado}"
                return _localizacao_em_cache

    except Exception:
        logger.warning("Não foi possível obter a localização via IP.", exc_info=True) # Falha silenciosa: a UI continuará rodando mesmo se a internet cair

    return LOCALIZACAO_INDISPONIVEL