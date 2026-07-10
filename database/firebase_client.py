import os
import firebase_admin
from firebase_admin import credentials, firestore

# Aponta para o seu arquivo de chaves local
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"

def get_db():
    """Inicializa o app do Firebase e retorna o cliente do Firestore."""
    if not firebase_admin._apps:
        cred = credentials.Certificate("credentials.json")
        firebase_admin.initialize_app(cred)
    
    return firestore.client()

# Exporta a variável 'db' para ser importada pelos seus services
db = get_db()