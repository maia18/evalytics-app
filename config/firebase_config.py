import firebase_admin
from firebase_admin import credentials, firestore

# O if garante que o Firebase não tente se inicializar duas vezes (o que daria erro)
if not firebase_admin._apps:
    # IMPORTANTE: Coloque aqui o caminho do seu arquivo JSON de chaves do Firebase
    # Exemplo: cred = credentials.Certificate("meu_projeto_firebase_keys.json")
    cred = credentials.Certificate("firebase_credentials.json")
    firebase_admin.initialize_app(cred)

# Aqui está a famosa variável 'db' que o erro estava pedindo!
db = firestore.client()