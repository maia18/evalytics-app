import logging
import firebase_admin
from pathlib import Path
from firebase_admin import (
    credentials, 
    firestore,
)
from google.cloud.firestore import Client

logger = logging.getLogger(__name__)

'''
Resolve o caminho de forma robusta, independentemente de onde o script principal for rodado
    O Path(__file__).resolve().parent garante que o script sempre procure a chave JSON na mesma pasta deste arquivo, não importando de qual terminal você rode o app.
'''
DIRETORIO_ATUAL = Path(__file__).resolve().parent
CAMINHO_CREDENCIAIS = DIRETORIO_ATUAL / "firebase_credentials.json"
try:
    '''      
    Garante que a inicialização ocorra apenas uma vez.
        Sem essa checagem, o Firebase lançaria um erro caso este arquivo fosse importado por múltiplos módulos simultaneamente:
        (Ex: ValueError: The default Firebase app already exists)
    '''
    if not firebase_admin._apps:

        #cred = credentials.Certificate(str(CAMINHO_CREDENCIAIS))
        # Força explicitamente o projectId do projeto ativo
        #firebase_admin.initialize_app(cred, {
        #    "projectId": "avaliacao-mec"
        #})
        cred = credentials.Certificate("database/services/firebase_credentials.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client(database_id="default")
    

except Exception:
    logger.exception("Erro na conexão com o Firebase.")
    raise # O raise propaga o erro para impedir que a aplicação inicie se o banco estiver indisponível (Fail-fast).

def load_firebase_config():
  return {
    #   "apiKey": "xxxxxxxxxxxxxxxxxxxxxx",
    #   "authDomain": "xxxxxxxxxxxxxxxxxxxxx",
    #   "projectId":  "xxxxxxxxxxxxxxxxxxxxx",
    #   "storageBucket": "xxxxxxxxxxxxxxxxxxxxx",
    #   "messagingSenderId": "xxxxxxxxxxxxxxxxxxxxx",
    #   "appId": "xxxxxxxxxxxxxxxxxxxxx",
      
    "apiKey": "AIzaSyAqGHhj3-BihICWHvD70smkjcbP2D8Sxnk",
    "authDomain": "avaliacao-mec.firebaseapp.com",
    "projectId":  "avaliacao-mec",
    "storageBucket": "avaliacao-mec.firebasestorage.app",
    "messagingSenderId": "881399469316",
    "appId": "1:881399469316:web:0f9f60c4660bc21e58ac51",	
  }