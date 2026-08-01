import logging as lg
from typing import Optional
from firebase_admin import firestore
from database.services.firebase_config import db # Importa a instância ativa do banco inicializada no arquivo anterior.

logger = lg.getLogger(__name__)
COLECAO_CURSOS = "cursos"

# Adiciona um curso na coleção de cursos. Retorna o ID do documento criado, ou None em caso de erro.
def adicionar_curso_db(codigo: str, nome: str, depto: str, coord: str) -> Optional[str]:
    try:
        # Cria um dicionário (documento) para ser salvo no NoSQL do Firestore.
        novo_curso = {
            "codigo": codigo,
            "nome": nome,
            "departamento": depto,
            "coordenador": coord,
            "timestamp": firestore.SERVER_TIMESTAMP, # Utiliza o carimbo de tempo do servidor do Google para precisão absoluta, em vez da hora local do PC.
        }
        _, doc_ref = db.collection(COLECAO_CURSOS).add(novo_curso) # O método .add() gera um ID alfanumérico automaticamente. Ele retorna uma tupla (update_time, document_ref).
        return doc_ref.id
    except Exception:
        logger.exception("Erro ao adicionar curso.")
        return None

# Retorna a lista de cursos cadastrados, cada um incluindo seu ID de documento
def obter_cursos_db() -> list[dict]:
    try:
        docs = db.collection(COLECAO_CURSOS).stream() # O .stream() busca todos os documentos de forma eficiente, em formato de gerador (generator).
        lista_cursos = []
        for doc in docs:
            dado = doc.to_dict() # Converte o documento bruto do Firebase para um dicionário Python normal.
            
            '''
            É essencial injetar o ID no dicionário, caso contrário a interface gráfica (Flet) não saberá qual ID enviar de volta na hora de editar ou excluir a linha.
            '''
            dado["id"] = doc.id
            lista_cursos.append(dado)
        return lista_cursos
    except Exception:
        logger.exception("Erro ao obter cursos.")
        return []

# Atualiza um curso existente. Retorna True em caso de sucesso
def atualizar_curso_db(doc_id: str, nome: str, depto: str, coord: str) -> bool:
    try:
        # Busca o documento específico usando o ID e atualiza apenas os campos fornecidos.
        db.collection(COLECAO_CURSOS).document(doc_id).update({
            "nome": nome,
            "departamento": depto,
            "coordenador": coord,
        })
        return True
    except Exception:
        logger.exception("Erro ao atualizar curso.")
        return False

# Exclui um curso pelo ID do documento. Retorna True em caso de sucesso
def excluir_curso_db(doc_id: str) -> bool:
    try:
        db.collection(COLECAO_CURSOS).document(doc_id).delete() # Remove o documento do Firestore permanentemente.
        return True
    except Exception:
        logger.exception("Erro ao excluir curso.")
        return False