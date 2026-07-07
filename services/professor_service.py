from repositories.professor_repository import (
    listar,
    inserir,
    atualizar,
    remover,
    listar_dict,
)


def listar_professores():
    return listar()


def listar_professor_dict():
    return listar_dict()


def adicionar_professor(nome, departamento, email):
    try:
        return inserir({
            "nome": nome,
            "departamento": departamento,
            "email": email,
            "ativo": True,
        })
    except Exception as e:
        print(f"ERRO NO SUPABASE: {e}")
        return None

def atualizar_professor(professor_id, nome, departamento, email):

    return atualizar(
        professor_id,
        {
            "nome": nome,
            "departamento": departamento,
            "email": email,
        }
    )


def remover_professor(professor_id):
    return remover(professor_id)