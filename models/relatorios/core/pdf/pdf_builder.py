import os
from datetime import datetime
from models.relatorios.core.pdf.pdf_template import RelatorioEvalytics

def construir_documento_pdf(
    caminho_arquivo: str,
    medias_validas: dict[int, float],
    nomes_eixos: dict[int, str],
    semestre: str,
    quantidade_avaliacoes: int,
    texto_cursos: str,
    caminho_imagem_radar: str
) -> None:
    """Constrói o layout do documento PDF e salva no disco."""
    
    pdf = RelatorioEvalytics(orientation="P", unit="mm", format="A4")
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

    pdf.output(caminho_arquivo)