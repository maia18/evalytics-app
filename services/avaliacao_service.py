from database.supabase_client import supabase

def listar_avaliacoes():
    """Busca todas as avaliações com os nomes dos professores e disciplinas vinculados."""
    try:
        res = supabase.table('avaliacoes')\
            .select('id, status, created_at, professores(nome), disciplinas(nome)')\
            .order('created_at', desc=True)\
            .execute()
        
        avaliacoes_formatadas = []
        for a in res.data:
            avaliacoes_formatadas.append({
                "id": a["id"],
                "professor": a.get("professores", {}).get("nome", "Desconhecido"),
                "disciplina": a.get("disciplinas", {}).get("nome", "Desconhecido"),
                "status": "Concluída" if a.get("status") == "concluida" else "Em Andamento",
                "data_avaliacao": a.get("created_at", "")[:10] # Extrai apenas a data (YYYY-MM-DD)
            })
            
        return avaliacoes_formatadas
    except Exception as e:
        print(f"Erro ao listar avaliações: {e}")
        return []


def detalhes_avaliacao(avaliacao_id: str):
    """Busca as respostas de uma avaliação específica, cruzando com os indicadores."""
    try:
        res = supabase.table('respostas')\
            .select('nota, comentario, indicadores(titulo, eixo_id)')\
            .eq('avaliacao_id', avaliacao_id)\
            .execute()
        
        detalhes = []
        for r in res.data:
            detalhes.append({
                "eixo": r["indicadores"]["eixo_id"],
                "indicador": r["indicadores"]["titulo"],
                "nota": r["nota"],
                "comentario": r["comentario"]
            })
            
        # Ordena as respostas pelo eixo para facilitar a visualização
        detalhes.sort(key=lambda x: x["eixo"])
        return detalhes
    except Exception as e:
        print(f"Erro ao buscar detalhes da avaliação: {e}")
        return []


def remover_avaliacao(avaliacao_id: str):
    """Remove uma avaliação do banco. O 'ON DELETE CASCADE' do SQL apagará as respostas."""
    try:
        supabase.table('avaliacoes').delete().eq('id', avaliacao_id).execute()
        return True
    except Exception as e:
        print(f"Erro ao remover avaliação: {e}")
        return False