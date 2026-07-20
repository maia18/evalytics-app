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
    
except FileNotFoundError:
    print(f"\n❌ ERRO CRÍTICO: Arquivo de credenciais não encontrado!")
    print(f"   Caminho esperado: {caminho_credenciais}")
    print(f"\n   Solução: Solicite o arquivo 'firebase_credentials.json' à equipe de desenvolvimento")
    print(f"            e coloque-o na pasta: {diretorio_atual}")
    raise
except Exception as e:
    print(f"\n❌ Erro na Conexão com Firebase: {e}")
    raise