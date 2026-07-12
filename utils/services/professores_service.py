from configurations.firebase_config import db

COLECAO = "professores" # Nome da coleção no Firebase

def criar_professor(nome: str, departamento: str, ativo: bool = True):
    
    """Cria um novo professor no Firebase e retorna o ID gerado."""
    
    # Cria uma referência vazia (o Firebase gera um ID único automático)
    doc_ref = db.collection(COLECAO).document()
    
    # Monta os dados
    dados = {
        "nome": nome,
        "departamento": departamento,
        "ativo": ativo
    }
    
    # Salva no banco
    doc_ref.set(dados)
    return doc_ref.id

def listar_professores():
    
    """Busca todos os professores e retorna uma lista de dicionários."""
    
    professores = []
    
    # O .stream() traz todos os documentos da coleção
    docs = db.collection(COLECAO).stream()
    
    for doc in docs:
        # Pega os dados do documento e injeta o ID real dele
        dados = doc.to_dict()
        dados["id"] = doc.id
        professores.append(dados)
        
    return professores

def atualizar_professor(professor_id: str, dados_atualizados: dict):
    
    """Atualiza os dados de um professor específico."""
    
    doc_ref = db.collection(COLECAO).document(professor_id)
    
    # O 'merge=True' é importante para atualizar apenas os campos enviados
    doc_ref.set(dados_atualizados, merge=True)
    return True

def deletar_professor(professor_id: str):
    
    """Apaga um professor permanentemente."""
    
    db.collection(COLECAO).document(professor_id).delete()
    return True