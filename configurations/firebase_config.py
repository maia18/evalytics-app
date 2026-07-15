""" Importa a biblioteca Firebase Admin para gerenciar serviços do Firebase """
import firebase_admin

from firebase_admin import credentials, firestore # Importa módulos específicos: credenciais e cliente Firestore

try:
    # Carrega as credenciais a partir do arquivo JSON (chave de serviço)
    cred = credentials.Certificate("database/credentials.json")
    
    """ 
    Verifica se já existe uma instância inicializada do Firebase.
    Se não houver, inicializa a aplicação com as credenciais
    """
    
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
        
    # Cria o cliente Firestore para interagir com o banco de dados
    db = firestore.client()
    
except Exception as e:
    # Captura qualquer erro crítico na conexão e exibe no console
    print(f"Erro Crítico na Conexão: {e}")
