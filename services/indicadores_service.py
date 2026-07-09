from config.firebase_config import db

def listar_indicadores():
    """Busca todos os indicadores cadastrados na nuvem."""
    try:
        docs = db.collection("indicadores").stream()
        return [{"id": doc.id, **doc.to_dict()} for doc in docs]
    except Exception as e:
        print(f"Erro ao buscar indicadores: {e}")
        return []

def criar_indicador(nome, categoria):
    """Salva um novo indicador de avaliação no Firebase."""
    try:
        novo_indicador = {
            "nome": nome,
            "categoria": categoria,
            "ativo": True
        }
        db.collection("indicadores").add(novo_indicador)
        print("Indicador criado com sucesso!")
    except Exception as e:
        print(f"Erro ao criar indicador: {e}")
        
def atualizar_indicador(id_indicador, novo_nome):
    """Atualiza o nome de um indicador existente no Firebase."""
    try:
        db.collection("indicadores").document(id_indicador).update({
            "nome": novo_nome
        })
    except Exception as e:
        print(f"Erro ao atualizar indicador: {e}")