from configurations.firebase_config import db
from services.indicadores_service import listar_indicadores

def calcular_medias_eixos():
    try:
        todos_indicadores = listar_indicadores()
        # Garante que mapeamos todos os eixos esperados (1, 2, 3)
        mapa_eixo = {ind['id']: ind.get('eixo', 1) for ind in todos_indicadores}
        
        avaliacoes = db.collection("avaliacoes").stream()
        
        # Inicializa com 0.0 para todos os eixos esperados
        acumulador = {1: [], 2: [], 3: []} 
        
        for av in avaliacoes:
            respostas = av.to_dict().get("respostas", {})
            for ind_id, nota in respostas.items():
                eixo_id = mapa_eixo.get(ind_id)
                if eixo_id in acumulador:
                    acumulador[eixo_id].append(float(nota))
        
        # Calcula médias
        medias_finais = {eixo: (sum(n)/len(n) if n else 0.0) for eixo, n in acumulador.items()}
        return medias_finais
    except Exception as e:
        print(f"Erro: {e}")
        return {1: 0.0, 2: 0.0, 3: 0.0}