from repositories.disciplina_repository import (
    listar,
    inserir,
    atualizar,
    remover,
    listar_dict,
)


def listar_disciplinas():
    return listar()


def listar_disciplina_dict():
    return listar_dict()


def adicionar_disciplina(codigo, nome, curso, semestre):

    return inserir({

        "codigo": codigo,

        "nome": nome,

        "curso": curso,

        "semestre": semestre,

    })


def atualizar_disciplina(
    disciplina_id,
    codigo,
    nome,
    curso,
    semestre,
):

    return atualizar(

        disciplina_id,

        {

            "codigo": codigo,

            "nome": nome,

            "curso": curso,

            "semestre": semestre,

        }

    )


def remover_disciplina(disciplina_id):
    return remover(disciplina_id)