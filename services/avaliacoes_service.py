from database.firebase_client import db
from datetime import datetime

COLECAO = "avaliacoes"

def criar_avaliacao(professor_id: str, disciplina_id: str, respostas: list):
    """
    Salva uma avaliação completa.
    'respostas' deve ser uma lista de dicionários, por exemplo:
    [{"indicador_id": "abc12", "nota": 5}, {"indicador_id": "xyz98", "nota": 4}]
    """
    doc_ref = db.collection(COLECAO).document()
    
    dados = {
        "professor_id": professor_id,
        "disciplina_id": disciplina_id,
        "respostas": respostas,
        # Salva o momento exato em que o aluno enviou a avaliação
        "data_criacao": datetime.now().isoformat() 
    }
    
    doc_ref.set(dados)
    return doc_ref.id

def listar_avaliacoes():
    """Busca todas as avaliações já respondidas."""
    avaliacoes = []
    
    # Podemos ordenar pela data de criação decrescente se quisermos
    docs = db.collection(COLECAO).order_by("data_criacao", direction="DESCENDING").stream()
    
    for doc in docs:
        dados = doc.to_dict()
        dados["id"] = doc.id
        avaliacoes.append(dados)
        
    return avaliacoes