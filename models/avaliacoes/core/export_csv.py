import csv
import logging
from typing import Optional

import flet as ft

from database.services.firebase_config import db
from models.avaliacoes.core.feedback import mostrar_feedback
from models.avaliacoes.core.filename_generator import gerar_nome_arquivo
from utils.services.indicadores.indicadores_repository import listar_indicadores


logger = logging.getLogger(__name__)


COLECAO_AVALIACOES = "avaliacoes"


NOMES_EIXOS = {
    1: "Organização Didático-Pedagógica",
    2: "Corpo Docente e Tutorial",
    3: "Infraestrutura",
}


def _formatar_data(data) -> str:
    """
    Converte a data da avaliação para um formato adequado ao CSV.
    """

    if not data:
        return ""

    try:
        return data.strftime("%d/%m/%Y %H:%M")
    except AttributeError:
        return str(data)


def _obter_mapa_indicadores() -> dict[str, dict]:
    """
    Carrega os indicadores cadastrados e cria um mapa pelo ID.
    """

    try:
        indicadores = listar_indicadores()

        return {
            str(indicador.get("id")): indicador
            for indicador in indicadores
            if indicador.get("id")
        }

    except Exception:
        logger.exception(
            "Erro ao carregar indicadores para exportação CSV."
        )
        return {}


def preparar_dados_csv(
    resultados: list[dict],
) -> list[list[str]]:
    """
    Converte as avaliações reais do Firestore para o formato CSV.

    O CSV contém uma linha para cada resposta de cada avaliação.
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

    if not resultados:
        return dados

    mapa_indicadores = _obter_mapa_indicadores()

    # ------------------------------------------------------
    # IDs das avaliações atualmente filtradas
    # ------------------------------------------------------

    ids_avaliacoes = {
        str(resultado.get("id"))
        for resultado in resultados
        if resultado.get("id")
    }

    if not ids_avaliacoes:
        return dados

    # ------------------------------------------------------
    # Busca avaliações reais
    # ------------------------------------------------------

    try:
        documentos = db.collection(COLECAO_AVALIACOES).stream()

        for documento in documentos:

            avaliacao_id = documento.id

            if avaliacao_id not in ids_avaliacoes:
                continue

            dados_avaliacao = documento.to_dict() or {}

            data_avaliacao = _formatar_data(
                dados_avaliacao.get("data_avaliacao")
            )

            curso_nome = dados_avaliacao.get(
                "curso_nome",
                "Curso não informado",
            )

            respostas = dados_avaliacao.get(
                "respostas",
                {},
            )

            if not isinstance(respostas, dict):
                continue

            # --------------------------------------------------
            # Cada indicador gera uma linha no CSV
            # --------------------------------------------------

            for indicador_id, nota in respostas.items():

                indicador = mapa_indicadores.get(
                    str(indicador_id),
                    {},
                )

                titulo_indicador = indicador.get(
                    "titulo",
                    "Indicador não encontrado",
                )

                eixo_id = indicador.get("eixo")

                try:
                    eixo_id = int(eixo_id)
                except (TypeError, ValueError):
                    eixo_id = None

                nome_eixo = NOMES_EIXOS.get(
                    eixo_id,
                    f"Eixo {eixo_id}"
                    if eixo_id is not None
                    else "Não informado",
                )

                # --------------------------------------------------
                # Nota
                # --------------------------------------------------

                try:
                    nota_formatada = f"{float(nota):.1f}"
                except (TypeError, ValueError):
                    nota_formatada = str(nota)

                # --------------------------------------------------
                # Comentário
                # --------------------------------------------------

                comentario = ""

                # Atualmente as avaliações podem não possuir
                # comentários individuais. Mantemos vazio quando
                # esse dado não existir.
                comentarios = dados_avaliacao.get(
                    "comentarios",
                    {},
                )

                if isinstance(comentarios, dict):
                    comentario = (
                        comentarios.get(indicador_id)
                        or comentarios.get(str(indicador_id))
                        or ""
                    )

                # --------------------------------------------------
                # Linha final
                # --------------------------------------------------

                dados.append(
                    [
                        avaliacao_id,
                        data_avaliacao,
                        str(curso_nome),
                        nome_eixo,
                        str(titulo_indicador),
                        nota_formatada,
                        str(comentario),
                    ]
                )

    except Exception:
        logger.exception(
            "Erro ao preparar dados reais para exportação CSV."
        )
        raise

    return dados


def exportar_csv(
    page: ft.Page,
    resultados: Optional[list[dict]] = None,
) -> None:
    """
    Exporta as respostas reais das avaliações atualmente
    selecionadas pelos filtros.
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

        # ------------------------------------------------------
        # Verifica se realmente existem respostas
        # ------------------------------------------------------

        if len(dados_exportacao) <= 1:
            mostrar_feedback(
                page,
                "Não existem respostas para exportar.",
                sucesso=False,
            )
            return

        # ------------------------------------------------------
        # Geração do arquivo
        # ------------------------------------------------------

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

        logger.exception(
            "Erro ao exportar CSV."
        )

        mostrar_feedback(
            page,
            f"Erro ao exportar: {erro}",
            sucesso=False,
        )