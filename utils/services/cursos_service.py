from database.services.firebase_config import db

def listar_cursos():
    
    """Busca todos os cursos cadastrados na nuvem."""
    
    try:
        docs = db.collection("cursos").stream()
        return [{"id": doc.id, **doc.to_dict()} for doc in docs]
    except Exception as e:
        print(f"Erro ao buscar cursos: {e}")
        return []

def criar_curso(nome, modalidade):
    
    """Salva um novo curso no Firebase."""
    
    try:
        novo_curso = {
            "nome": nome,
            "modalidade": modalidade, # Ex: Presencial, EAD, Híbrido
            "ativo": True
        }
        db.collection("cursos").add(novo_curso)
        print("Curso criado com sucesso!")
    except Exception as e:
        print(f"Erro ao criar curso: {e}")