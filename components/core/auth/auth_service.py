import logging
import requests
from typing import (
    Optional, 
    Dict, 
    Any,
)

logger = logging.getLogger(__name__)

def renovar_token_firebase(api_key: str, refresh_token: str) -> Optional[Dict[str, Any]]:
    """Comunica com o Google Identity Toolkit para renovar a sessão utilizando o refresh token."""
    
    url = f"https://securetoken.googleapis.com/v1/token?key={api_key}"
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }

    try:
        response = requests.post(url, data=payload, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        return None
        
    except Exception as erro:
        logger.exception("Erro na comunicação com a API de autenticação: %s", erro)
        return None


def obter_dados_usuario_firebase(api_key: str, id_token: str) -> dict[str, Any]:
    """Recupera e-mail/nome ao restaurar uma sessão a partir do refresh token."""
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:lookup?key={api_key}"
    try:
        resposta = requests.post(url, json={"idToken": id_token}, timeout=10)
        resposta.raise_for_status()
        usuarios = resposta.json().get("users") or []
        return usuarios[0] if usuarios else {}
    except Exception:
        logger.exception("Não foi possível recuperar o perfil Firebase da sessão.")
        return {}
