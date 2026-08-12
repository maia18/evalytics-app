import os
import firebase_admin
from firebase_admin import credentials, firestore

# 1. Calcula o caminho real e absoluto da raiz do projeto (C:\evalytics-app)
config_dir = os.path.dirname(os.path.abspath(__file__))  # pasta 'config'
raiz_do_projeto = os.path.dirname(config_dir)            # pasta 'evalytics-app'
caminho_credenciais = os.path.join(raiz_do_projeto, "firebase_credentials.json")

# 2. Inicializa o Firebase apenas se ainda não foi inicializado
if not firebase_admin._apps:
    # ATENÇÃO: Aqui usamos a variável com o caminho blindado, sem as aspas do nome do arquivo
    cred = credentials.Certificate(caminho_credenciais)
    firebase_admin.initialize_app(cred)

# 3. Exporta o banco de dados para o resto do app usar
db = firestore.client()