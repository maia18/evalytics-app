import os
import logging
import flet as ft
from typing import Optional
from datetime import datetime
from models.avaliacoes.core.feedback import mostrar_feedback
from models.relatorios.core.grafico_radar import salvar_grafico_radar
from .pdf_builder import construir_documento_pdf

logger = logging.getLogger(__name__)
CAMINHO_IMAGEM_TEMP = "radar_temp.png"

def normalizar_nome_curso(nome: str) -> str:
    """Padroniza o nome dos cursos para exibição."""
    if not nome:
        return "Curso não informado"

    nome_limpo = str(nome).strip().lower()
    mapeamento = {
        "eng telecom": "Engenharia de Telecomunicações",
        "engenharia de telecomunicações": "Engenharia de Telecomunicações",
    }

    return mapeamento.get(nome_limpo, str(nome).strip())

def gerar_pdf_completo(
    page: ft.Page,
    medias: dict[int, float | None],
    nomes_eixos: dict[int, str],
    semestre: str = "Todos",
    quantidade_avaliacoes: int = 0,
    cursos: list[str] | None = None,
) -> Optional[str]:
    """Orquestra a validação, estruturação, geração visual do PDF e os alertas na UI."""

    try:
        # ==================================================
        # VALIDAÇÃO DAS MÉDIAS
        # ==================================================
        medias_validas: dict[int, float] = {}

        for eixo_id, nota in medias.items():
            if nota is None:
                continue
            try:
                medias_validas[eixo_id] = float(nota)
            except (TypeError, ValueError):
                continue

        if not medias_validas:
            mostrar_feedback(page, "Não existem dados para gerar o relatório PDF.", sucesso=False)
            return None

        # ==================================================
        # NORMALIZAÇÃO DOS CURSOS
        # ==================================================
        cursos_normalizados = {
            normalizar_nome_curso(curso)
            for curso in (cursos or [])
            if curso and str(curso).strip()
        }

        cursos_validos = sorted(cursos_normalizados)
        texto_cursos = ", ".join(cursos_validos) if cursos_validos else "Todos os cursos"

        # ==================================================
        # GERAÇÃO DO ARQUIVO PDF E GRÁFICO AUXILIAR
        # ==================================================
        salvar_grafico_radar(medias_validas, nomes_eixos, CAMINHO_IMAGEM_TEMP)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"relatorio_evalytics_{timestamp}.pdf"

        # Delega a tarefa de desenho do documento ao pdf_builder
        construir_documento_pdf(
            caminho_arquivo=nome_arquivo,
            medias_validas=medias_validas,
            nomes_eixos=nomes_eixos,
            semestre=semestre,
            quantidade_avaliacoes=quantidade_avaliacoes,
            texto_cursos=texto_cursos,
            caminho_imagem_radar=CAMINHO_IMAGEM_TEMP
        )

        # ==================================================
        # LIMPEZA E FEEDBACK
        # ==================================================
        if os.path.exists(CAMINHO_IMAGEM_TEMP):
            os.remove(CAMINHO_IMAGEM_TEMP)

        mostrar_feedback(page, f"PDF gerado com sucesso: {nome_arquivo}", sucesso=True)
        return nome_arquivo

    except Exception:
        if os.path.exists(CAMINHO_IMAGEM_TEMP):
            os.remove(CAMINHO_IMAGEM_TEMP)

        logger.exception("Erro ao gerar o documento PDF.")
        mostrar_feedback(page, "Erro ao gerar o documento PDF.", sucesso=False)
        return None