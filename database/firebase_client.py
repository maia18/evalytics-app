import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os

# Caminho para o ficheiro de credenciais
cred_path = "firebase_credentials.json"

def get_db():
    # Verifica se o ficheiro existe para evitar erros
    if not os.path.exists(cred_path):
        raise FileNotFoundError(f"Ficheiro {cred_path} não encontrado! Verifique se está na pasta raiz do projeto.")

    # Verifica se o Firebase já foi inicializado (importante para evitar erros de duplicação)
    if not firebase_admin._apps:
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
    
    # Retorna o cliente do Firestore (a nossa ligação à base de dados)
    return firestore.client()

# Exporta a variável 'db' para ser usada nos outros serviços
db = get_db()