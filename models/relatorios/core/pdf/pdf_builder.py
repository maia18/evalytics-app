import os
from datetime import datetime
from pathlib import Path
from fpdf.enums import XPos, YPos
from models.relatorios.core.pdf.pdf_template import RelatorioEvalytics


NOMES_EIXOS_PADRAO = {
    1: "Organização Didático-Pedagógica",
    2: "Corpo Docente e Tutorial",
    3: "Infraestrutura",
}


def _texto(valor) -> str:
    if valor is None:
        return ""
    if hasattr(valor, "strftime"):
        return valor.strftime("%d/%m/%Y %H:%M")
    return str(valor)


def _multi_cell(pdf, altura: float, texto: str) -> None:
    """Escreve um parágrafo e reposiciona o cursor para a próxima linha."""
    pdf.multi_cell(
        w=0,
        h=altura,
        text=texto,
        new_x=XPos.LMARGIN,
        new_y=YPos.NEXT,
    )


def _adicionar_copias_avaliacoes(pdf, avaliacoes: list[dict]) -> None:
    if not avaliacoes:
        pdf.add_page()
        pdf.set_font("helvetica", "B", 13)
        _multi_cell(pdf, 7, "Cópia das avaliações")
        pdf.set_font("helvetica", "", 10)
        _multi_cell(pdf, 5, "Não foi possível localizar os detalhes das avaliações selecionadas.")
        return

    for indice, avaliacao in enumerate(avaliacoes):
        pdf.add_page()
        pdf.set_text_color(17, 24, 39)
        pdf.set_font("helvetica", "B", 14)
        _multi_cell(pdf, 7, f"Cópia da avaliação {indice + 1}")
        pdf.set_font("helvetica", "", 9)
        pdf.set_text_color(70, 70, 70)
        _multi_cell(pdf, 5, f"Curso: {_texto(avaliacao.get('curso_nome'))}")
        _multi_cell(pdf, 5, f"Data: {_texto(avaliacao.get('data_avaliacao')) or 'Não informada'}")
        _multi_cell(pdf, 5, f"Identificador: {_texto(avaliacao.get('id'))}")
        origem_perguntas = (
            "Perguntas e critérios: cópia armazenada com esta avaliação"
            if avaliacao.get("perguntas_historicas")
            else "Perguntas e critérios: reconstruídos do catálogo atual (avaliação antiga sem cópia histórica)"
        )
        pdf.set_font("helvetica", "I", 8)
        _multi_cell(pdf, 4.5, origem_perguntas)
        pdf.ln(2)

        respostas = avaliacao.get("respostas", {})
        justificativas = avaliacao.get("justificativas", {})
        evidencias = avaliacao.get("evidencias", {})
        eixo_atual = None

        for numero, pergunta in enumerate(avaliacao.get("perguntas", []), start=1):
            try:
                eixo_id = int(pergunta.get("eixo"))
            except (TypeError, ValueError):
                eixo_id = None

            if eixo_id != eixo_atual:
                eixo_atual = eixo_id
                nome_eixo = NOMES_EIXOS_PADRAO.get(eixo_id, f"Eixo {eixo_id or 'não informado'}")
                if pdf.get_y() > pdf.page_break_trigger - 24:
                    pdf.add_page()
                pdf.set_fill_color(230, 239, 250)
                pdf.set_text_color(25, 80, 140)
                pdf.set_font("helvetica", "B", 11)
                pdf.cell(0, 7, nome_eixo, border=0, ln=True, fill=True)
                pdf.ln(2)

            indicador_id = str(pergunta.get("id", ""))
            chave_resposta = next(
                (chave for chave in respostas if str(chave) == indicador_id), None
            )
            resposta = respostas.get(chave_resposta) if chave_resposta is not None else None
            resposta_texto = _texto(resposta).strip()
            titulo = _texto(pergunta.get("titulo")) or "Pergunta sem título"
            pdf.set_text_color(17, 24, 39)
            pdf.set_font("helvetica", "B", 9)
            _multi_cell(pdf, 4.5, f"{numero}. {titulo}")

            descricao = _texto(pergunta.get("descricao")).strip()
            if descricao:
                pdf.set_font("helvetica", "I", 8)
                pdf.set_text_color(90, 90, 90)
                _multi_cell(pdf, 4, descricao)

            criterios = pergunta.get("criterios", {})
            if isinstance(criterios, dict) and criterios:
                pdf.set_font("helvetica", "", 8)
                pdf.set_text_color(40, 40, 40)
                for nivel, criterio in sorted(criterios.items(), key=lambda item: str(item[0])):
                    marcador = "[X]" if resposta_texto == str(nivel) else "[ ]"
                    _multi_cell(pdf, 4, f"{marcador} Nível {nivel}: {_texto(criterio)}")

            if resposta_texto:
                criterio_selecionado = criterios.get(resposta_texto, "") if isinstance(criterios, dict) else ""
                pdf.set_font("helvetica", "B", 8)
                pdf.set_text_color(25, 118, 70)
                _multi_cell(pdf, 4.5, f"Resposta registrada: nível {resposta_texto}")
                if criterio_selecionado:
                    pdf.set_font("helvetica", "", 8)
                    _multi_cell(pdf, 4, _texto(criterio_selecionado))
            else:
                pdf.set_font("helvetica", "B", 8)
                pdf.set_text_color(150, 70, 30)
                _multi_cell(pdf, 4.5, "Resposta registrada: sem resposta")

            chave_justificativa = next(
                (chave for chave in justificativas if str(chave) == indicador_id), None
            ) if isinstance(justificativas, dict) else None
            justificativa = _texto(justificativas.get(chave_justificativa)).strip() if chave_justificativa is not None else ""
            if justificativa:
                pdf.set_font("helvetica", "B", 8)
                pdf.set_text_color(50, 50, 50)
                _multi_cell(pdf, 4.5, "Justificativa:")
                pdf.set_font("helvetica", "", 8)
                _multi_cell(pdf, 4, justificativa)

            chave_evidencia = next(
                (chave for chave in evidencias if str(chave) == indicador_id), None
            ) if isinstance(evidencias, dict) else None
            anexos = evidencias.get(chave_evidencia, []) if chave_evidencia is not None else []
            for anexo in anexos if isinstance(anexos, list) else []:
                if isinstance(anexo, dict):
                    nome = _texto(anexo.get("nome"))
                    url = _texto(anexo.get("url"))
                    pdf.set_font("helvetica", "", 8)
                    _multi_cell(pdf, 4, f"Evidência: {nome} {url}".strip())

            pdf.ln(3)

        ids_perguntas = {
            str(pergunta.get("id", ""))
            for pergunta in avaliacao.get("perguntas", [])
        }

        respostas_sem_pergunta = [
            (indicador_id, resposta)
            for indicador_id, resposta in respostas.items()
            if str(indicador_id) not in ids_perguntas
        ] if isinstance(respostas, dict) and avaliacao.get("perguntas_historicas") is False and eixo_atual is None else []

        if respostas_sem_pergunta:
            if pdf.get_y() > pdf.page_break_trigger - 20:
                pdf.add_page()
            pdf.set_font("helvetica", "B", 9)
            pdf.set_text_color(150, 70, 30)
            _multi_cell(pdf, 5, "Respostas sem pergunta recuperável no catálogo atual")
            pdf.set_font("helvetica", "", 8)
            for indicador_id, resposta in respostas_sem_pergunta:
                _multi_cell(
                    pdf,
                    4,
                    f"Indicador {indicador_id}: resposta registrada {_texto(resposta)}",
                )


def construir_documento_pdf(
    caminho_arquivo: str,
    medias_validas: dict[int, float],
    nomes_eixos: dict[int, str],
    semestre: str,
    quantidade_avaliacoes: int,
    texto_cursos: str,
    caminho_imagem_radar: str,
    avaliacoes_detalhadas: list[dict] | None = None,
) -> None:
    """Constrói o layout do documento PDF e salva no disco."""
    
    pdf = RelatorioEvalytics(orientation="P", unit="mm", format="A4")
    diretorio_fontes = Path(__file__).resolve().parents[4] / "assets" / "fonts"
    pdf.add_font("DejaVu", "", str(diretorio_fontes / "DejaVuSans.ttf"))
    pdf.add_font("DejaVu", "B", str(diretorio_fontes / "DejaVuSans-Bold.ttf"))
    pdf.add_font("DejaVu", "I", str(diretorio_fontes / "DejaVuSans-Oblique.ttf"))
    pdf.add_font("DejaVu", "BI", str(diretorio_fontes / "DejaVuSans-BoldOblique.ttf"))
    pdf.set_left_margin(20)
    pdf.set_right_margin(20)
    pdf.add_page()

    # Data de geração
    pdf.set_font("helvetica", "I", 8)
    pdf.set_text_color(100, 100, 100)
    data_geracao = datetime.now().strftime("%d/%m/%Y às %H:%M")
    pdf.cell(0, 4, f"Documento gerado em: {data_geracao}", ln=True, align="R")
    pdf.ln(2)

    # Título
    pdf.set_font("helvetica", "B", 18)
    pdf.set_text_color(17, 24, 39)
    pdf.cell(0, 8, "Relatório de Avaliação Institucional", ln=True, align="C")
    
    pdf.set_font("helvetica", "", 10)
    pdf.set_text_color(95, 99, 104)
    pdf.cell(0, 5, "Evalytics", ln=True, align="C")
    pdf.ln(4)

    # Introdução
    pdf.set_font("helvetica", "", 9)
    pdf.set_text_color(0, 0, 0)
    texto_intro = (
        "Este relatório apresenta os resultados das avaliações institucionais coletadas através "
        "da plataforma Evalytics. Os dados apresentados correspondem aos filtros selecionados na tela "
        "de Relatórios."
    )
    pdf.multi_cell(0, 4.5, txt=texto_intro, align="J")
    pdf.ln(3)

    # Informações do relatório
    pdf.set_font("helvetica", "B", 11)
    pdf.set_text_color(17, 24, 39)
    pdf.cell(0, 6, "Informações do relatório", ln=True)
    pdf.ln(1)

    largura_rotulo, largura_valor, altura_linha = 40, 130, 6
    pdf.set_fill_color(245, 245, 245)

    # Tabela de Informações
    for rotulo, valor in [
        ("Semestre", str(semestre)),
        ("Curso(s)", texto_cursos),
        ("Avaliações", str(quantidade_avaliacoes))
    ]:
        pdf.set_font("helvetica", "B", 9)
        pdf.cell(largura_rotulo, altura_linha, rotulo, border=1, fill=True, align="L")
        pdf.set_font("helvetica", "", 9)
        pdf.cell(largura_valor, altura_linha, valor, border=1, align="L")
        pdf.ln()

    pdf.ln(5)

    # Gráfico Radar
    if os.path.exists(caminho_imagem_radar):
        pdf.set_font("helvetica", "B", 11)
        pdf.set_text_color(17, 24, 39)
        pdf.cell(0, 6, "Desempenho por eixo avaliativo", ln=True, align="C")
        pdf.ln(1)
        pdf.image(caminho_imagem_radar, x=67, w=76)
        pdf.ln(3)

    # Tabela de Médias
    pdf.set_font("helvetica", "B", 11)
    pdf.set_text_color(17, 24, 39)
    pdf.cell(0, 6, "Médias por eixo avaliativo", ln=True)
    pdf.ln(1)

    largura_eixo, largura_nota, altura_tabela = 140, 30, 7

    pdf.set_font("helvetica", "B", 9)
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(largura_eixo, altura_tabela, "Eixo avaliativo", border=1, fill=True, align="C")
    pdf.cell(largura_nota, altura_tabela, "Média", border=1, fill=True, align="C")
    pdf.ln()

    pdf.set_font("helvetica", "", 9)
    for eixo_id in sorted(medias_validas.keys()):
        nome_eixo = nomes_eixos.get(eixo_id, f"Eixo {eixo_id}")
        nota = medias_validas[eixo_id]
        pdf.cell(largura_eixo, altura_tabela, nome_eixo, border=1, align="L")
        pdf.cell(largura_nota, altura_tabela, f"{nota:.2f}", border=1, align="C")
        pdf.ln()

    # Resumo
    media_geral = sum(medias_validas.values()) / len(medias_validas)
    pdf.ln(4)
    pdf.set_font("helvetica", "B", 11)
    pdf.set_text_color(17, 24, 39)
    pdf.cell(0, 6, "Resumo dos resultados", ln=True)

    pdf.set_font("helvetica", "", 9)
    pdf.cell(0, 5, f"Média geral dos eixos respondidos: {media_geral:.2f}", ln=True)
    pdf.cell(0, 5, f"Eixos considerados: {len(medias_validas)}", ln=True)
    pdf.cell(0, 5, f"Avaliações analisadas: {quantidade_avaliacoes}", ln=True)

    _adicionar_copias_avaliacoes(pdf, avaliacoes_detalhadas or [])

    pdf.output(caminho_arquivo)
