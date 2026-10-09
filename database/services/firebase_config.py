import os
import logging
import firebase_admin
from pathlib import Path
from firebase_admin import (
    credentials, 
    firestore,
)
logger = logging.getLogger(__name__)

# Chave pública da API do Firebase usada na autenticação REST.
FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY", "")

# Caminho das credenciais do Firebase Admin SDK.
DIRETORIO_ATUAL = Path(__file__).resolve().parent
CAMINHO_CREDENCIAIS = DIRETORIO_ATUAL / "firebase_credentials.json"

try:
    
    '''      
        Garante que a inicialização ocorra apenas uma vez.
            Sem essa checagem, o Firebase lançaria um erro caso este arquivo fosse importado por múltiplos módulos simultaneamente.
        '''
    if not firebase_admin._apps:
        cred = credentials.Certificate(str(CAMINHO_CREDENCIAIS))
        firebase_admin.initialize_app(cred)

    db = firestore.client(database_id="default")

except Exception:
    logger.exception("Erro na conexão com o Firebase.")
    raise # O raise propaga o erro para impedir que a aplicação inicie se o banco estiver indisponível (Fail-fast).

def load_firebase_config() -> dict:
    return {
        "apiKey": FIREBASE_API_KEY,
        "authDomain": "xxxxxxxxxxxxxxxxxxxxx",
        "projectId":  "xxxxxxxxxxxxxxxxxxxxx",
        "storageBucket": "xxxxxxxxxxxxxxxxxxxxx",
        "messagingSenderId": "xxxxxxxxxxxxxxxxxxxxx",
        "appId": "xxxxxxxxxxxxxxxxxxxxx",
    }