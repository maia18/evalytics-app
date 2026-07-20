import os
import firebase_admin
from firebase_admin import credentials, firestore

# 1. Resolve o caminho de forma robusta, independentemente de onde o script principal for rodado
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
caminho_credenciais = os.path.join(diretorio_atual, "firebase_credentials.json")

try:
    # 2. Garante que a inicialização ocorra apenas uma vez
    if not firebase_admin._apps:
        cred = credentials.Certificate(caminho_credenciais)
        firebase_admin.initialize_app(cred)
    
    # 3. Cria e exporta o cliente Firestore
    db = firestore.client()
    
except Exception as e:
    print(f"\n❌ Erro na Conexão com Firebase: {e}")
    raise