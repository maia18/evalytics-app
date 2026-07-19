import firebase_admin # biblioteca Firebase Admin para gerenciar serviços do Firebase
from firebase_admin import credentials, firestore

""" 
Verifica se já existe uma instância inicializada do Firebase.
Se não houver, inicializa a aplicação com as credenciais.
"""
    
try:
    cred = credentials.Certificate("database/firebase_credentials.json") # Carrega as credenciais a partir do arquivo JSON (chave de serviço)
    
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
        
    db = firestore.client() # Cria o cliente Firestore para interagir com o banco de dados
    
except Exception as e:
    print(f"Erro Crítico na Conexão: {e}") # Captura qualquer erro crítico na conexão e exibe no console