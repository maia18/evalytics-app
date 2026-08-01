import logging as lg
from typing import Optional
from database.services.firebase_config import db

logger = lg.getLogger(__name__)
COLECAO_AVALIACOES = "avaliacoes_institucionais"

'''
Mapeia a chave de nota (como armazenada no Firestore) para a chave de saída do resumo
    O uso de uma tupla constante garante que você não itere sobre campos indesejados.
'''
CAMPOS_NOTAS = (
    "infraestrutura",
    "didatica",
    "atendimento",
    "material",
    "inovacao",
)

def obter_medias_dashboard() -> Optional[dict[str, float]]:
    """
    Calcula a média de cada indicador de avaliação institucional para o dashboard.
    Retorna None se não houver avaliações registradas ou em caso de erro.
    """
    try:
        docs = db.collection(COLECAO_AVALIACOES).stream()
        
        ''' 
        Cria um dicionário inicial zerado para cada campo usando Dictionary Comprehension.
            Ex: {'infraestrutura': 0, 'didatica': 0, ...}
        '''
        soma = {campo: 0 for campo in CAMPOS_NOTAS}
        total_avaliacoes = 0

        for doc in docs:
            dados = doc.to_dict()
            notas = dados.get("notas")
            
            # Se houver uma chave 'notas' preenchida no documento, ele entra no cálculo.
            if notas:
                for campo in CAMPOS_NOTAS:
                    soma[campo] += notas.get(campo, 0) # Adiciona a nota atual do campo à soma total. Usa 0 como fallback de segurança.
                total_avaliacoes += 1

        '''
        Cláusula de guarda essencial: impede um erro fatal de "Divisão por Zero" caso a coleção esteja vazia ou ninguém tenha preenchido o formulário.
        '''
        if total_avaliacoes == 0:
            return None

        '''
        Divide a soma total pelo número de avaliações, usando round(..., 1) para manter a interface visual limpa (ex: 4.3 em vez de 4.3333333).
        '''
        return {
            campo: round(soma[campo] / total_avaliacoes, 1)
            for campo in CAMPOS_NOTAS
        }
    except Exception:
        logger.exception("Erro ao buscar médias do dashboard.")
        return None