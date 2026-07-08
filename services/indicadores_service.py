from database.firebase_client import db

COLECAO = "indicadores"

def criar_indicador(eixo: str, pergunta: str, ativo: bool = True):
    """Cria uma nova pergunta/indicador no Firebase."""
    doc_ref = db.collection(COLECAO).document()
    
    dados = {
        "eixo": eixo,
        "pergunta": pergunta,
        "ativo": ativo
    }
    
    doc_ref.set(dados)
    return doc_ref.id

def listar_indicadores():
    """Busca todos os indicadores cadastrados."""
    indicadores = []
    docs = db.collection(COLECAO).stream()
    
    for doc in docs:
        dados = doc.to_dict()
        dados["id"] = doc.id
        indicadores.append(dados)
        
    return indicadores

def atualizar_indicador(indicador_id: str, dados_atualizados: dict):
    """Atualiza os dados de um indicador específico."""
    doc_ref = db.collection(COLECAO).document(indicador_id)
    doc_ref.set(dados_atualizados, merge=True)
    return True

def deletar_indicador(indicador_id: str):
    """Apaga um indicador permanentemente."""
    db.collection(COLECAO).document(indicador_id).delete()
    return True