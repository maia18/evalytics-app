import os
import firebase_admin
from firebase_admin import credentials, firestore

"""
# ==============================================================================
# RESOLUÇÃO INTELIGENTE DE CAMINHOS ABSOLUTOS
#   Isso impede que o app quebre se for rodado a partir de uma pasta diferente no terminal (ex: rodar `python src/db.py` vs `python db.py`).
# ==============================================================================
"""

config_dir = os.path.dirname(os.path.abspath(__file__))  # Descobre a pasta atual (ex: /core/config)
raiz_do_projeto = os.path.dirname(config_dir)            # Sobe um nível para a raiz do projeto
caminho_credenciais = os.path.join(raiz_do_projeto, "firebase_credentials.json")

"""
# ==============================================================================
# INICIALIZAÇÃO SEGURA (SINGLETON)
# ==============================================================================
"""

'''
Verifica se o firebase_admin já possui instâncias ativas (len > 0).
    Sem isso, salvar o código no modo Hot Reloading (Recarregamento rápido) causaria um erro de "Default app already exists".
'''
if not firebase_admin._apps:
    cred = credentials.Certificate(caminho_credenciais)
    firebase_admin.initialize_app(cred)

db = firestore.client() # Exporta o cliente Firestore instanciado para ser importado pelos repositórios.