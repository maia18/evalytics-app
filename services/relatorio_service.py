from services.avaliacoes_service import listar_avaliacoes
from services.professores_service import listar_professores
from services.disciplinas_service import listar_disciplinas
from services.indicadores_service import listar_indicadores

def gerar_relatorio_geral():
    """
    Puxa todos os dados do Firebase e cruza as informações em memória
    para gerar um relatório consolidado de médias por professor.
    """
    # 1. Busca todos os dados "crus" das coleções
    avaliacoes = listar_avaliacoes()
    professores = {p["id"]: p for p in listar_professores()}
    disciplinas = {d["id"]: d for d in listar_disciplinas()}
    indicadores = {i["id"]: i for i in listar_indicadores()}

    # 2. Estrutura para calcular as médias (Agrupando por Professor)
    # Formato: {"id_prof": {"nome": "João", "soma_notas": 20, "qtd_notas": 4}}
    resultado_professores = {}

    for avaliacao in avaliacacoes:
        prof_id = avaliacao.get("professor_id")
        
        # Ignora se o professor foi deletado do banco, mas a avaliação ficou
        if prof_id not in professores:
            continue

        if prof_id not in resultado_professores:
            resultado_professores[prof_id] = {
                "nome": professores[prof_id].get("nome", "Desconhecido"),
                "departamento": professores[prof_id].get("departamento", "N/A"),
                "soma_notas": 0,
                "qtd_notas": 0
            }

        # Soma as notas dessa avaliação
        for resposta in avaliacao.get("respostas", []):
            nota = resposta.get("nota")
            if isinstance(nota, (int, float)):
                resultado_professores[prof_id]["soma_notas"] += nota
                resultado_professores[prof_id]["qtd_notas"] += 1

    # 3. Finaliza calculando a média real
    relatorio_final = []
    for prof_id, dados in resultado_professores.items():
        media = 0
        if dados["qtd_notas"] > 0:
            media = dados["soma_notas"] / dados["qtd_notas"]
            
        relatorio_final.append({
            "professor_id": prof_id,
            "nome_professor": dados["nome"],
            "departamento": dados["departamento"],
            "media_geral": round(media, 2),
            "total_avaliacoes_indicadores": dados["qtd_notas"]
        })

    # Ordena o relatório da maior nota para a menor
    relatorio_final.sort(key=lambda x: x["media_geral"], reverse=True)
    
    return relatorio_final