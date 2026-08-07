import logging as lg
from pathlib import Path
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore import Client

logger = lg.getLogger(__name__)

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
        cred = credentials.Certificate(str(CAMINHO_CREDENCIAIS))
        firebase_admin.initialize_app(cred)

    '''Cria e exporta o cliente Firestore'''
    db: Client = firestore.client() # A variável 'db' se torna o ponto de entrada principal para ler e gravar dados

except Exception:
    logger.exception("Erro na conexão com o Firebase.")
    
    raise # O raise propaga o erro para impedir que a aplicação inicie se o banco estiver indisponível (Fail-fast).