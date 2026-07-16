""" Conexão central com Firestore """
import os
import firebase_admin
from firebase_admin import credentials, firestore

diretorio_atual = os.path.dirname(os.path.abspath(__file__))
caminho_credenciais = os.path.join(diretorio_atual, "credentials.json")

cred = credentials.Certificate(caminho_credenciais)

# Inicializa o app Firebase apenas uma vez
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

# Cliente Firestore disponível para outros módulos
db = firestore.client()