""" Importações """  
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # Ajusta o path para permitir importações relativas ao projeto

""" Importa o cliente Firestore e a configuração de conexão """
from firebase_admin import firestore
from configurations.firebase_config import db

# ==========================================
# FUNÇÕES DE MANIPULAÇÃO DO BANCO DE DADOS
# ==========================================

def injetar_dados_teste():

    """
    Função temporária para criar um documento no Firestore.
    Útil para validar se o Python consegue escrever na nuvem.
    """
    
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
    
    try:
        # Cria documento na coleção 'avaliacoes_institucionais'
        db.collection("avaliacoes_institucionais").add(avaliacao_simulada)
        print("✅ Dados de teste injetados com sucesso no Firestore!")
    except Exception as e:
        print(f"❌ Erro ao salvar dados: {e}")

def obter_medias_dashboard():
    
    """
    Função que será usada pelo dashboard.py para montar gráficos.
    Calcula médias das avaliações armazenadas no Firestore.
    """
    
    try:
        # Puxa os documentos da coleção
        docs = db.collection("avaliacoes_institucionais").stream()
        
        # Acumuladores para somar notas
        soma = {"infra": 0, "didatica": 0, "atend": 0, "mat": 0, "inov": 0}
        total_avaliacoes = 0
        
        for doc in docs:
            dados = doc.to_dict()
            if "notas" in dados:
                soma["infra"] += dados["notas"].get("infraestrutura", 0)
                soma["didatica"] += dados["notas"].get("didatica", 0)
                soma["atend"] += dados["notas"].get("atendimento", 0)
                soma["mat"] += dados["notas"].get("material", 0)
                soma["inov"] += dados["notas"].get("inovacao", 0)
                total_avaliacoes += 1
                
        if total_avaliacoes == 0:
            return None # Retorna None se não houver dados
            
        # Calcula a média real baseada em todos os documentos do banco
        medias = {
            "infraestrutura": round(soma["infra"] / total_avaliacoes, 1),
            "didatica": round(soma["didatica"] / total_avaliacoes, 1),
            "atendimento": round(soma["atend"] / total_avaliacoes, 1),
            "material": round(soma["mat"] / total_avaliacoes, 1),
            "inovacao": round(soma["inov"] / total_avaliacoes, 1),
        }
        return medias
        
    except Exception as e:
        print(f"Erro ao buscar dados: {e}")
        return None
    
# ==========================================
# GESTÃO DE CURSOS (CRUD)
# ==========================================

def adicionar_curso_db(codigo, nome, depto, coord):
    
    """
    Adiciona um novo curso na coleção 'cursos'.
    Retorna o ID único gerado pelo Firebase.
    """
    
    try:
        # Adiciona um novo documento na coleção "cursos"
        novo_curso = {
            "codigo": codigo,
            "nome": nome,
            "departamento": depto,
            "coordenador": coord,
            "timestamp": firestore.SERVER_TIMESTAMP
        }
        
        # Retorna o ID único que o Firebase gerou para este documento
        _, doc_ref = db.collection("cursos").add(novo_curso)
        return doc_ref.id
    except Exception as e:
        print(f"Erro ao adicionar curso no banco: {e}")
        return None

def obter_cursos_db():
    
    """
    Retorna lista de cursos armazenados no Firestore.
    Cada curso inclui o ID do documento para futuras operações.
    """
    
    try:
        docs = db.collection("cursos").stream()
        lista_cursos = []
        for doc in docs:
            dado = doc.to_dict()
            dado["id"] = doc.id # Guardamos o ID do Firebase para usar na edição/exclusão
            lista_cursos.append(dado)
        return lista_cursos
    except Exception as e:
        print(f"Erro ao obter cursos do banco: {e}")
        return []

def atualizar_curso_db(doc_id, nome, depto, coord):
    
    """
    Atualiza os dados de um curso existente.
    """
    
    try:
        db.collection("cursos").document(doc_id).update({
            "nome": nome,
            "departamento": depto,
            "coordenador": coord
        })
        return True
    except Exception as e:
        print(f"Erro ao atualizar curso no banco: {e}")
        return False

def excluir_curso_db(doc_id):
    
    """
    Exclui um curso do Firestore pelo seu ID.
    """
    
    try:
        db.collection("cursos").document(doc_id).delete()
        return True
    except Exception as e:
        print(f"Erro ao excluir curso no banco: {e}")
        return False