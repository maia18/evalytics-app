from database.services.firebase_config import db

COLECAO = "disciplinas" # Nome da coleção no Firebase

def criar_disciplina(nome: str, codigo: str, carga_horaria: int):
    
    """Cria uma nova disciplina no Firebase e retorna o ID gerado."""
    
    doc_ref = db.collection(COLECAO).document()
    
    dados = {
        "nome": nome,
        "codigo": codigo,
        "carga_horaria": carga_horaria
    }
    
    doc_ref.set(dados)
    return doc_ref.id

def listar_disciplinas():
    
    """Busca todas as disciplinas e retorna uma lista de dicionários."""
    
    disciplinas = []
    docs = db.collection(COLECAO).stream()
    
    for doc in docs:
        dados = doc.to_dict()
        dados["id"] = doc.id
        disciplinas.append(dados)
        
    return disciplinas

def atualizar_disciplina(disciplina_id: str, dados_atualizados: dict):
    
    """Atualiza os dados de uma disciplina específica."""
    
    doc_ref = db.collection(COLECAO).document(disciplina_id)
    doc_ref.set(dados_atualizados, merge=True)
    return True

def deletar_disciplina(disciplina_id: str):
    
    """Apaga uma disciplina permanentemente."""
    
    db.collection(COLECAO).document(disciplina_id).delete()
    return True