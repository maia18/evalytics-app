import logging
import firebase_admin
from pathlib import Path
from firebase_admin import credentials, firestore

logger = logging.getLogger(__name__)

# Caminho das credenciais privadas do Firebase Admin SDK.
DIRETORIO_ATUAL = Path(__file__).resolve().parent
CAMINHO_CREDENCIAIS = DIRETORIO_ATUAL / "firebase_credentials.json"

try:
    # Inicializa o Firebase Admin SDK apenas uma vez.
    if not firebase_admin._apps:
        cred = credentials.Certificate(str(CAMINHO_CREDENCIAIS))
        firebase_admin.initialize_app(cred)

    # Conexão com o Firestore.
    db = firestore.client(database_id="default")

except Exception:
    logger.exception("Erro na conexão com o Firebase.")
    raise