import logging as lg

import flet as ft

from database.services.firebase_config import db
from utils.services.indicadores.indicadores_repository import listar_indicadores


logger = lg.getLogger(__name__)

COLECAO_AVALIACOES = "avaliacoes"


NOMES_EIXOS = {
    1: "Organização Didático-Pedagógica",
    2: "Corpo Docente e Tutorial",
    3: "Infraestrutura",
}


def _definir_cor_nota(nota: float) -> str:
    """Define a cor visual da nota conforme a escala de avaliação."""

    if nota >= 4.0:
        return ft.Colors.GREEN_700

    if nota >= 3.0:
        return ft.Colors.ORANGE_700

    return ft.Colors.RED_700


def _formatar_data(data) -> str:
    """Converte a data armazenada no Firestore para o formato da tabela."""

    if not data:
        return "Data desconhecida"

    try:
        return data.strftime("%d/%m/%Y, %H:%M")
    except AttributeError:
        return str(data)


def obter_respostas_tabela() -> list[dict]:
    """
    Busca as avaliações reais do Firestore e transforma cada resposta
    de indicador em uma linha da tabela.

    Uma avaliação pode gerar várias linhas, pois cada indicador
    respondido representa uma resposta individual.
    """

    try:
        documentos = (
            db.collection(COLECAO_AVALIACOES)
            .stream()
        )

        indicadores = listar_indicadores()

        mapa_indicadores = {
            indicador.get("id"): indicador
            for indicador in indicadores
            if indicador.get("id")
        }

        linhas = []

        for documento in documentos:
            dados = documento.to_dict() or {}

            avaliacao_id = documento.id

            curso_nome = dados.get(
                "curso_nome",
                "Curso não informado",
            )

            data_avaliacao = dados.get(
                "data_avaliacao"
            )

            data_formatada = _formatar_data(
                data_avaliacao
            )

            respostas = dados.get(
                "respostas",
                {},
            )

            if not isinstance(respostas, dict):
                continue

            for indicador_id, resposta in respostas.items():

                indicador = mapa_indicadores.get(
                    indicador_id,
                    {},
                )

                titulo_indicador = indicador.get(
                    "titulo",
                    "Indicador não encontrado",
                )

                eixo = indicador.get(
                    "eixo"
                )

                nome_eixo = NOMES_EIXOS.get(
                    eixo,
                    f"Eixo {eixo}" if eixo else "Geral",
                )

                try:
                    nota = float(resposta)
                except (TypeError, ValueError):
                    continue

                linhas.append(
                    {
                        "id": avaliacao_id[:7].upper(),
                        "data": data_formatada,
                        "curso": curso_nome,
                        "eixo": nome_eixo,
                        "indicador": titulo_indicador,
                        "nota": f"{nota:.1f}",
                        "cor_nota": _definir_cor_nota(nota),
                        "comentario": None,
                    }
                )

        # Mais recentes primeiro.
        linhas.sort(
            key=lambda item: item["data"],
            reverse=True,
        )

        return linhas

    except Exception:
        logger.exception(
            "Erro ao buscar respostas das avaliações."
        )
        return []