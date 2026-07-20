from firebase_admin import firestore
from database.services.firebase_config import db

# Adiciona curso na coleção 'cursos'
def adicionar_curso_db(codigo, nome, depto, coord):
    try:
        novo_curso = {
            "codigo": codigo,
            "nome": nome,
            "departamento": depto,
            "coordenador": coord,
            "timestamp": firestore.SERVER_TIMESTAMP
        }
        _, doc_ref = db.collection("cursos").add(novo_curso)
        return doc_ref.id
    except Exception as e:
        print(f"Erro ao adicionar curso: {e}")
        return None

# Retorna lista de cursos com IDs
def obter_cursos_db():
    try:
        docs = db.collection("cursos").stream()
        lista_cursos = []
        for doc in docs:
            dado = doc.to_dict()
            dado["id"] = doc.id
            lista_cursos.append(dado)
        return lista_cursos
    except Exception as e:
        print(f"Erro ao obter cursos: {e}")
        return []

# Atualiza curso existente
def atualizar_curso_db(doc_id, nome, depto, coord):
    try:
        db.collection("cursos").document(doc_id).update({
            "nome": nome,
            "departamento": depto,
            "coordenador": coord
        })
        return True
    except Exception as e:
        print(f"Erro ao atualizar curso: {e}")
        return False

# Exclui curso pelo ID
def excluir_curso_db(doc_id):
    try:
        db.collection("cursos").document(doc_id).delete()
        return True
    except Exception as e:
        print(f"Erro ao excluir curso: {e}")
        return False