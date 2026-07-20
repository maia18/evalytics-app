from database.services.firebase_config import db
from utils.services.indicadores_service import listar_indicadores

def calcular_medias_eixos():
    
    """
    Função que calcula as médias das avaliações por eixo temático.
    
    Fluxo:
        1. Lista todos os indicadores e mapeia cada indicador ao seu eixo.
        2. Busca todas as avaliações no Firestore.
        3. Agrupa as notas por eixo.
        4. Calcula a média de cada eixo.
    
    Retorna:
    - Dicionário {eixo_id: média}
    """
    
    try:
        # Lista todos os indicadores disponíveis
        todos_indicadores = listar_indicadores()
        
        # Cria um mapa {id_indicador: eixo} garantindo que cada indicador tenha um eixo associado
        # Se não houver eixo definido, assume eixo 1 como padrão
        mapa_eixo = {ind['id']: ind.get('eixo', 1) for ind in todos_indicadores}
        
        # Recupera todas as avaliações armazenadas no Firestore
        avaliacoes = db.collection("avaliacoes").stream()
        
        # Inicializa acumuladores para cada eixo (listas de notas)
        acumulador = {1: [], 2: [], 3: []} 
        
        # Itera sobre cada avaliação
        for av in avaliacoes:
            respostas = av.to_dict().get("respostas", {})
            # Para cada resposta, identifica o eixo e acumula a nota
            for ind_id, nota in respostas.items():
                eixo_id = mapa_eixo.get(ind_id)
                if eixo_id in acumulador:
                    acumulador[eixo_id].append(float(nota))
        
        # Calcula as médias finais por eixo
        medias_finais = {
            eixo: (sum(notas) / len(notas) if notas else 0.0) 
            for eixo, notas in acumulador.items()
        }
        
        return medias_finais
    
    except Exception as e:
        """
        Em caso de erro, imprime a mensagem e retorna médias zeradas
        """
        print(f"Erro: {e}")
        return {1: 0.0, 2: 0.0, 3: 0.0}