import logging
import os
from datetime import datetime
from typing import Optional

from fpdf import FPDF
import plotly.graph_objects as go

from models.avaliacoes.core.feedback import mostrar_feedback

logger = logging.getLogger(__name__)

CAMINHO_IMAGEM_TEMP = "radar_temp.png"

class RelatorioEvalytics(FPDF):
    """Documento PDF customizado que estende o FPDF original. 
    Define um cabeçalho e rodapé padrão que serão injetados automaticamente em todas as páginas."""

    def header(self) -> None:
        """Imprime o cabeçalho no topo da página atual."""
        self.set_font("helvetica", "B", 16)
        self.set_text_color(25, 118, 210)
        self.cell(0, 10, "Evalytics - Avaliação Institucional", ln=True, align="C")

        self.set_font("helvetica", "B", 12)
        self.set_text_color(0, 0, 0)
        self.cell(0, 10, "Relatório Consolidado de Eixos", ln=True, align="C")

        # Linha fina divisória abaixo dos títulos
        self.line(20, 30, 190, 30)
        self.ln(10)

    def footer(self) -> None:
        """Posiciona a quebra a -15mm do final e imprime o número da página centralizado."""
        self.set_y(-15)
        self.set_font("helvetica", "I", 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, f"Página {self.page_no()}", align="C")


def gerar_pdf_completo(page, medias: dict, nomes_eixos: dict, semestre: str = "2025.2") -> Optional[str]:
    """Orquestrador da geração: Desenha o gráfico, injeta as métricas, compila o arquivo e emite o aviso."""
    try:
        # Passo 1: Geração do Gráfico via Plotly
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            # Extrai os dados garantindo que eles estão ordenados pelas mesmas chaves numéricas
            r=[medias[i] for i in sorted(medias.keys())],
            theta=[nomes_eixos[i] for i in sorted(medias.keys())],
            fill='toself', fillcolor='rgba(33, 150, 243, 0.3)', line_color='rgb(33, 150, 243)', marker=dict(size=8),
        ))
        # Trava a escala do radar (teia de aranha) para o limite máximo de nota 5
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 5])), showlegend=False)
        
        # Salva silenciosamente a imagem compilada pelo Plotly em disco
        fig.write_image(CAMINHO_IMAGEM_TEMP)

        # Passo 2: Montagem textual do Documento
        pdf = RelatorioEvalytics(orientation="P", unit="mm", format="A4")
        pdf.set_left_margin(20)
        pdf.set_right_margin(20)
        pdf.add_page()

        pdf.set_font("helvetica", "I", 10)
        pdf.set_text_color(100, 100, 100)
        data_geracao = datetime.now().strftime("%d/%m/%Y às %H:%M")
        pdf.cell(0, 5, f"Documento gerado em: {data_geracao}", ln=True, align="R")
        pdf.ln(5)

        # Escreve parágrafo justificado (J) com a multi_cell
        pdf.set_font("helvetica", "", 12)
        pdf.set_text_color(0, 0, 0)
        texto_intro = (
            "Este relatório apresenta os resultados preliminares coletados através dos "
            "formulários de avaliação. O gráfico abaixo ilustra o desempenho em cada eixo "
            "temático, permitindo uma visualização clara dos pontos de excelência e das "
            "áreas que necessitam de atenção pedagógica."
        )
        pdf.multi_cell(0, 7, txt=texto_intro, align='J')
        pdf.ln(5)

        # Passo 3: Injeção do Gráfico
        # Largura útil da página A4 com margens de 20mm é 170mm; w=100 e x=55 centraliza a imagem matematicamente (170-100)/2 + 20.
        pdf.image(CAMINHO_IMAGEM_TEMP, x=55, w=100)
        pdf.ln(10)

        # Passo 4: Tabela de Médias
        pdf.set_font("helvetica", "B", 11)
        pdf.set_fill_color(240, 240, 240)

        largura_semestre = 30
        qtde_eixos = len(medias) if len(medias) > 0 else 1
        largura_coluna_eixo = 140 / qtde_eixos

        # Cabeçalhos da Tabela
        pdf.cell(largura_semestre, 10, "Semestre", border=1, fill=True, align="C")
        for eixo_id in sorted(medias.keys()):
            pdf.cell(largura_coluna_eixo, 10, nomes_eixos[eixo_id].upper(), border=1, fill=True, align="C")
        pdf.ln()

        # Dados da Tabela
        pdf.set_font("helvetica", "", 11)
        pdf.cell(largura_semestre, 10, semestre, border=1, align="C")
        for eixo_id in sorted(medias.keys()):
            pdf.cell(largura_coluna_eixo, 10, f"{medias[eixo_id]:.2f}", border=1, align="C")
        pdf.ln()

        # Exportação Final
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"relatorio_evalytics_{timestamp}.pdf"
        pdf.output(nome_arquivo)

        # Cleanup: Remove a imagem temporária do computador para não deixar lixo
        if os.path.exists(CAMINHO_IMAGEM_TEMP):
            os.remove(CAMINHO_IMAGEM_TEMP)

        mostrar_feedback(page, f"PDF gerado com sucesso: {nome_arquivo}", sucesso=True)
        return nome_arquivo

    except Exception:
        # Cleanup Garantido: Se o Plotly ou FPDF quebrar, limpa a imagem inacabada para não corromper execuções futuras
        if os.path.exists(CAMINHO_IMAGEM_TEMP):
            os.remove(CAMINHO_IMAGEM_TEMP) 

        logger.exception("Erro ao gerar o documento PDF.")
        mostrar_feedback(page, "Erro ao gerar o documento PDF.", sucesso=False)
        return None