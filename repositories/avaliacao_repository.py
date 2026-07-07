from database.supabase_client import supabase


def listar(desc=False):

    consulta = (

        supabase
        .table("avaliacoes")
        .select("*")

    )

    consulta = consulta.order(
        "id",
        desc=desc
    )

    return consulta.execute().data


def inserir(dados):

    return (

        supabase
        .table("avaliacoes")
        .insert(dados)
        .execute()

    )


def remover(avaliacao_id):

    return (

        supabase
        .table("avaliacoes")
        .delete()
        .eq("id", avaliacao_id)
        .execute()

    )