from firebase_admin import firestore
from database.services.conexao import db

def injetar_dados_teste():
    avaliacao_simulada = {
        "semestre": "Atual",
        "notas": {
            "infraestrutura": 4.8,
            "didatica": 4.5,
            "atendimento": 4.0,
            "material": 4.2,
            "inovacao": 4.7
        },
        "timestamp": firestore.SERVER_TIMESTAMP
    }
    db.collection("avaliacoes_institucionais").add(avaliacao_simulada)
