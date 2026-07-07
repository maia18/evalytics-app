from database.supabase_client import supabase


def listar():
    return (
        supabase
        .table("professores")
        .select("*")
        .order("nome")
        .execute()
        .data
    )


def inserir(dados):
    return (
        supabase
        .table("professores")
        .insert(dados)
        .execute()
    )


def atualizar(id, dados):
    return (
        supabase
        .table("professores")
        .update(dados)
        .eq("id", id)
        .execute()
    )


def remover(id):
    return (
        supabase
        .table("professores")
        .delete()
        .eq("id", id)
        .execute()
    )


def listar_dict():
    professores = listar()

    return {
        p["id"]: p["nome"]
        for p in professores
    }


def listar_nome_para_id():
    return {
        p["nome"]: p["id"]
        for p in listar()
    }