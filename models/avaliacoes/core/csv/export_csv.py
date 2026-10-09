import csv
import logging
import flet as ft
from typing import Optional
from models.avaliacoes.core.feedback import mostrar_feedback
from models.avaliacoes.core.filename_generator import gerar_nome_arquivo
from .csv_data_service import preparar_dados_csv

logger = logging.getLogger(__name__)

def exportar_csv(page: ft.Page, resultados: Optional[list[dict]] = None) -> None:
    """Exporta as respostas reais das avaliações atualmente selecionadas pelos filtros."""
    
    if resultados is None:
        resultados = []

    if not resultados:
        mostrar_feedback(page, "Não existem dados para exportar.", sucesso=False)
        return

    nome_arquivo = gerar_nome_arquivo()

    try:
        dados_exportacao = preparar_dados_csv(resultados)

        if len(dados_exportacao) <= 1:
            mostrar_feedback(page, "Não existem respostas para exportar.", sucesso=False)
            return

        with open(nome_arquivo, mode="w", newline="", encoding="utf-8-sig") as arquivo_csv:
            escritor = csv.writer(arquivo_csv, delimiter=";")
            escritor.writerows(dados_exportacao)

        mostrar_feedback(
            page, 
            f"Arquivo CSV exportado com sucesso: {nome_arquivo}", 
            sucesso=True
        )

    except Exception as erro:
        logger.exception("Erro ao exportar CSV.")
        mostrar_feedback(page, f"Erro ao exportar: {erro}", sucesso=False)