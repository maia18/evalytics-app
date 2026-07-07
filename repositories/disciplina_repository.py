from database.supabase_client import supabase


def listar():
    return (
        supabase
        .table("disciplinas")
        .select("*")
        .order("nome")
        .execute()
        .data
    )


def inserir(dados):
    return (
        supabase
        .table("disciplinas")
        .insert(dados)
        .execute()
    )


def atualizar(id, dados):
    return (
        supabase
        .table("disciplinas")
        .update(dados)
        .eq("id", id)
        .execute()
    )


def remover(id):
    return (
        supabase
        .table("disciplinas")
        .delete()
        .eq("id", id)
        .execute()
    )


def listar_dict():
    disciplinas = listar()

    return {
        d["id"]: d["nome"]
        for d in disciplinas
    }


def listar_nome_para_id():
    return {
        d["nome"]: d["id"]
        for d in listar()
    }