import csv

import flet as ft

from typing import Optional

from models.avaliacoes.core.feedback import mostrar_feedback
from models.avaliacoes.core.filename_generator import gerar_nome_arquivo


def preparar_dados_csv(
    resultados: list[dict],
) -> list[list[str]]:
    """
    Converte as respostas individuais exibidas na tabela
    para o formato utilizado pelo arquivo CSV.
    """

    dados = [
        [
            "ID_Avaliacao",
            "Data",
            "Curso",
            "Eixo",
            "Indicador",
            "Nota",
            "Comentario",
        ]
    ]

    for resultado in resultados:
        dados.append(
            [
                str(resultado.get("id", "")),
                str(resultado.get("data", "")),
                str(
                    resultado.get(
                        "curso",
                        "Curso não informado",
                    )
                ),
                str(
                    resultado.get(
                        "eixo",
                        "Não informado",
                    )
                ),
                str(
                    resultado.get(
                        "indicador",
                        "Não informado",
                    )
                ),
                str(resultado.get("nota", "")),
                str(
                    resultado.get(
                        "comentario",
                        "",
                    )
                    or ""
                ),
            ]
        )

    return dados


def exportar_csv(
    page: ft.Page,
    resultados: Optional[list[dict]] = None,
) -> None:
    """
    Exporta as respostas reais atualmente carregadas
    na tabela de acompanhamento.
    """

    if resultados is None:
        resultados = []

    if not resultados:
        mostrar_feedback(
            page,
            "Não existem dados para exportar.",
            sucesso=False,
        )
        return

    nome_arquivo = gerar_nome_arquivo()

    try:
        dados_exportacao = preparar_dados_csv(
            resultados
        )

        with open(
            nome_arquivo,
            mode="w",
            newline="",
            encoding="utf-8-sig",
        ) as arquivo_csv:

            escritor = csv.writer(
                arquivo_csv,
                delimiter=";",
            )

            escritor.writerows(
                dados_exportacao
            )

        mostrar_feedback(
            page,
            f"Arquivo CSV exportado com sucesso: {nome_arquivo}",
            sucesso=True,
        )

    except Exception as erro:
        mostrar_feedback(
            page,
            f"Erro ao exportar: {erro}",
            sucesso=False,
        )