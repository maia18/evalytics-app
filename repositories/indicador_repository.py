from database.supabase_client import supabase


def listar():
    return (
        supabase
        .table("indicadores")
        .select("*")
        .order("eixo")
        .order("id")
        .execute()
        .data
    )


def listar_por_eixo(eixo: int):
    return (
        supabase
        .table("indicadores")
        .select("*")
        .eq("eixo", eixo)
        .order("id")
        .execute()
        .data
    )