from database.supabase_client import supabase


def listar():

    return (
        supabase
        .table("respostas")
        .select("*")
        .execute()
        .data
    )


def inserir(dados):

    return (
        supabase
        .table("respostas")
        .insert(dados)
        .execute()
    )


def listar_por_avaliacao(avaliacao_id):

    return (
        supabase
        .table("respostas")
        .select("*")
        .eq("avaliacao_id", avaliacao_id)
        .execute()
        .data
    )


def remover_por_avaliacao(avaliacao_id):

    return (
        supabase
        .table("respostas")
        .delete()
        .eq("avaliacao_id", avaliacao_id)
        .execute()
    )