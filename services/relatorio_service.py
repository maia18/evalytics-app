from database.supabase_client import supabase

def obter_resumo_dashboard():
    """Busca o total de professores, disciplinas e avaliações no banco."""
    try:
        # Pega as contagens diretamente das tabelas
        prof_res = supabase.table('professores').select('id', count='exact').execute()
        disc_res = supabase.table('disciplinas').select('id', count='exact').execute()
        aval_res = supabase.table('avaliacoes').select('id', count='exact').execute()
        
        return {
            "professores": prof_res.count if prof_res else 0,
            "disciplinas": disc_res.count if disc_res else 0,
            "avaliacoes": aval_res.count if aval_res else 0
        }
    except Exception as e:
        print(f"Erro ao obter resumo: {e}")
        return {"professores": 0, "disciplinas": 0, "avaliacoes": 0}

def gerar_relatorio_ultima_avaliacao():
    """Busca a última avaliação concluída e calcula suas médias."""
    try:
        # 1. Pega a última avaliação com os nomes do professor e disciplina
        aval_res = supabase.table('avaliacoes')\
            .select('*, professores(nome), disciplinas(nome)')\
            .eq('status', 'concluida')\
            .order('created_at', desc=True)\
            .limit(1).execute()
        
        if not aval_res.data:
            return None
            
        ultima_aval = aval_res.data[0]
        avaliacao_id = ultima_aval['id']
        
        # 2. Pega as respostas dessa avaliação cruzando com o eixo do indicador
        resp_res = supabase.table('respostas')\
            .select('nota, indicadores(eixo_id)')\
            .eq('avaliacao_id', avaliacao_id).execute()
        
        respostas = resp_res.data
        if not respostas:
            return {
                "avaliacao": ultima_aval,
                "media_geral": 0,
                "total_respostas": 0,
                "medias_por_eixo": {}
            }
            
        # 3. Calcula as médias
        total_notas = 0
        por_eixo = {}
        
        for r in respostas:
            nota = r['nota']
            eixo_id = r['indicadores']['eixo_id']
            
            total_notas += nota
            if eixo_id not in por_eixo:
                por_eixo[eixo_id] = {"soma": 0, "count": 0}
                
            por_eixo[eixo_id]["soma"] += nota
            por_eixo[eixo_id]["count"] += 1
            
        media_geral = total_notas / len(respostas)
        
        medias_eixo = {
            eixo: round(dados["soma"] / dados["count"], 2)
            for eixo, dados in por_eixo.items()
        }
        
        return {
            "avaliacao": ultima_aval,
            "media_geral": round(media_geral, 2),
            "total_respostas": len(respostas),
            "medias_por_eixo": medias_eixo
        }
        
    except Exception as e:
        print(f"Erro ao gerar relatorio: {e}")
        return None
    
def gerar_relatorio_avaliacao(avaliacao_id: str):
    """Busca os dados e calcula as médias para uma avaliação específica."""
    try:
        # Busca a avaliação específica
        aval_res = supabase.table('avaliacoes')\
            .select('*, professores(nome), disciplinas(nome)')\
            .eq('id', avaliacao_id).execute()
        
        if not aval_res.data:
            return None
            
        avaliacao = aval_res.data[0]
        
        # Busca as respostas vinculadas a esta avaliação
        resp_res = supabase.table('respostas')\
            .select('nota, indicadores(eixo_id)')\
            .eq('avaliacao_id', avaliacao_id).execute()
        
        respostas = resp_res.data
        if not respostas:
            return {
                "avaliacao": avaliacao,
                "media_geral": 0,
                "total_respostas": 0,
                "medias_por_eixo": {}
            }
            
        # Calcula as médias
        total_notas = 0
        por_eixo = {}
        
        for r in respostas:
            nota = r['nota']
            eixo_id = r['indicadores']['eixo_id']
            
            total_notas += nota
            if eixo_id not in por_eixo:
                por_eixo[eixo_id] = {"soma": 0, "count": 0}
                
            por_eixo[eixo_id]["soma"] += nota
            por_eixo[eixo_id]["count"] += 1
            
        media_geral = total_notas / len(respostas)
        
        medias_eixo = {
            eixo: round(dados["soma"] / dados["count"], 2)
            for eixo, dados in por_eixo.items()
        }
        
        return {
            "avaliacao": avaliacao,
            "media_geral": round(media_geral, 2),
            "total_respostas": len(respostas),
            "medias_por_eixo": medias_eixo
        }
        
    except Exception as e:
        print(f"Erro ao gerar relatorio especifico: {e}")
        return None