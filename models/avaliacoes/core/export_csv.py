import csv

import flet as ft

from typing import Optional

from models.avaliacoes.core.feedback import mostrar_feedback
from models.avaliacoes.core.filename_generator import gerar_nome_arquivo


NOMES_EIXOS = {
    1: "Organização Didático-Pedagógica",
    2: "Corpo Docente e Tutorial",
    3: "Infraestrutura",
}


def preparar_dados_csv(
    resultados: list[dict],
) -> list[list[str]]:
    """
    Converte os resultados consolidados para o formato
    utilizado pelo arquivo CSV.
    """

    dados = [
        [
            "ID_Avaliacao",
            "Data",
            "Curso",
            "Eixo 1",
            "Eixo 2",
            "Eixo 3",
            "Media Geral",
        ]
    ]

    for resultado in resultados:

        dados.append(
            [
                str(resultado.get("id", "")),
                str(resultado.get("data_avaliacao", "")),
                str(
                    resultado.get(
                        "curso_nome",
                        "Curso não informado",
                    )
                ),
                f'{resultado.get("eixo_1", 0.0):.2f}',
                f'{resultado.get("eixo_2", 0.0):.2f}',
                f'{resultado.get("eixo_3", 0.0):.2f}',
                f'{resultado.get("media_geral", 0.0):.2f}',
            ]
        )

    return dados


def exportar_csv(
    page: ft.Page,
    resultados: Optional[list[dict]] = None,
) -> None:
    """
    Exporta os resultados reais para CSV.

    O arquivo recebe exatamente os resultados que estão
    sendo exibidos após a aplicação dos filtros.
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