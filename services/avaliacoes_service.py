from configurations.firebase_config import db
from datetime import datetime

def salvar_avaliacao(curso_id, curso_nome, respostas):
    """
    Salva o formulário de avaliação preenchido no Firebase.
    'respostas' é um dicionário no formato { id_do_indicador : nota }
    """
    try:
        nova_avaliacao = {
            "curso_id": curso_id,
            "curso_nome": curso_nome,
            # Salva a data e hora exatas em que o botão foi clicado
            "data_avaliacao": datetime.now().isoformat(),
            "respostas": respostas
        }
        
        db.collection("avaliacoes").add(nova_avaliacao)
        print(f"Avaliação do curso {curso_nome} salva com sucesso!")
        return True
        
    except Exception as e:
        print(f"Erro ao salvar a avaliação: {e}")
        return False
    
def listar_avaliacoes():
    """Busca todas as avaliações concluídas no Firebase."""
    try:
        docs = db.collection("avaliacoes").stream()
        return [{"id": doc.id, **doc.to_dict()} for doc in docs]
    except Exception as e:
        print(f"Erro ao buscar avaliações: {e}")
        return []