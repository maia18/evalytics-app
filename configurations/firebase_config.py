import firebase_admin # type: ignore
from firebase_admin import credentials, firestore # type: ignore

try:
    cred = credentials.Certificate("database/credentials.json")
    
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
        
    db = firestore.client()
    
except Exception as e:
    print(f"Erro Crítico na Conexão: {e}")