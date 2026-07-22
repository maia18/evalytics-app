from fpdf import FPDF
from models.avaliacoes.core.feedback import mostrar_feedback
from datetime import datetime

def gerar_pdf(page):
    try:
        # Inicializa o PDF em formato A4, retrato (Portrait)
        pdf = FPDF(orientation="P", unit="mm", format="A4")
        pdf.add_page()
        
        # --- CABEÇALHO ---
        pdf.set_font("helvetica", "B", 16)
        # O RGB (25, 118, 210) equivale ao seu azul primário #1976D2
        pdf.set_text_color(25, 118, 210) 
        pdf.cell(0, 10, "Evalytics - Avaliação Institucional", ln=True, align="C")
        
        pdf.set_font("helvetica", "B", 12)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 10, "Relatório Consolidado de Eixos", ln=True, align="C")
        
        pdf.ln(5) # Quebra de linha (respiro)
        
        # --- METADADOS ---
        pdf.set_font("helvetica", "I", 10)
        pdf.set_text_color(100, 100, 100)
        data_geracao = datetime.now().strftime("%d/%m/%Y às %H:%M")
        pdf.cell(0, 10, f"Documento gerado em: {data_geracao}", ln=True, align="R")
        
        pdf.ln(10)
        
        # --- CONTEÚDO (MOCK DATA) ---
        pdf.set_font("helvetica", "", 12)
        pdf.set_text_color(0, 0, 0)
        
        pdf.multi_cell(0, 8, txt=(
            "Este relatório apresenta os resultados preliminares "
            "coletados através dos formulários de avaliação docente e de infraestrutura. "
            "Os dados abaixo representam a consolidação bruta do semestre selecionado."
        ))
        
        pdf.ln(10)
        
        # Tabela Simples (Cabeçalho)
        pdf.set_font("helvetica", "B", 11)
        pdf.set_fill_color(240, 240, 240)
        pdf.cell(40, 10, "Semestre", border=1, fill=True, align="C")
        pdf.cell(50, 10, "Infraestrutura", border=1, fill=True, align="C")
        pdf.cell(50, 10, "Didática", border=1, fill=True, align="C")
        pdf.cell(50, 10, "Inovação", border=1, fill=True, align="C")
        pdf.ln()
        
        # Tabela Simples (Dados)
        pdf.set_font("helvetica", "", 11)
        pdf.cell(40, 10, "2025.2", border=1, align="C")
        pdf.cell(50, 10, "4.8", border=1, align="C")
        pdf.cell(50, 10, "4.5", border=1, align="C")
        pdf.cell(50, 10, "4.7", border=1, align="C")
        pdf.ln()

        # --- SALVANDO O ARQUIVO ---
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"relatorio_evalytics_{timestamp}.pdf"
        
        # Gera fisicamente o arquivo na raiz do projeto
        pdf.output(nome_arquivo)
        
        # Retorna o feedback visual na tela do Flet
        mostrar_feedback(page, f"PDF gerado com sucesso: {nome_arquivo}", sucesso=True)
        
    except Exception as erro:
        mostrar_feedback(page, f"Erro ao gerar o documento PDF: {erro}", sucesso=False)