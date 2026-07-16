from fpdf import FPDF
import plotly.graph_objects as go
import os

# Classe personalizada para o relatório acadêmico
class RelatorioAcademico(FPDF):
    def header(self):
        # Define o cabeçalho do documento
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "RELATORIO DE AVALIACAO INSTITUCIONAL", ln=True, align="C")
        
        # Linha horizontal abaixo do título
        self.line(20, 26, 190, 26) 
        self.ln(10)

    def footer(self):
        # Define o rodapé com número da página
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Pagina {self.page_no()}", align="C")

# Função principal para gerar o PDF
def gerar_pdf_resultados(medias, nomes_eixos):
    """
    Gera um relatório em PDF com:
    1. Gráfico de radar mostrando as médias por eixo.
    2. Texto introdutório explicativo.
    3. Tabela com os resultados numéricos.
    
    Parâmetros:
    - medias: dicionário {id_eixo: média}
    - nomes_eixos: dicionário {id_eixo: nome do eixo}
    
    Retorna:
    - Caminho do arquivo PDF gerado.
    """

    # 1. Criação do gráfico de radar
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=[medias[i] for i in sorted(medias.keys())],  # valores das médias
        theta=[nomes_eixos[i] for i in sorted(medias.keys())],  # nomes dos eixos
        fill='toself',
        fillcolor='rgba(33, 150, 243, 0.3)',  # azul transparente
        line_color='rgb(33, 150, 243)',       # cor da linha
        marker=dict(size=8)                   # pontos nos vértices
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 5])), 
        showlegend=False
    )
    fig.write_image("radar_temp.png")  # salva gráfico temporário

    # 2. Configuração do documento PDF
    pdf = RelatorioAcademico()
    pdf.set_left_margin(25)
    pdf.set_right_margin(25)
    pdf.add_page()
    
    # 3. Texto introdutório
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Analise de Desempenho", ln=True)
    pdf.set_font("Arial", "", 12)
    texto_intro = (
        "Este relatorio apresenta os dados consolidados das avaliações institucionais. "
        "O gráfico abaixo ilustra o desempenho em cada eixo temático, permitindo uma "
        "visualização clara dos pontos de excelência e das áreas que necessitam de atenção pedagógica."
    )
    pdf.multi_cell(0, 7, texto_intro, align='J')  # texto justificado
    
    pdf.ln(5)
    pdf.image("radar_temp.png", x=55, w=100)  # insere gráfico
    pdf.ln(10)

    # 4. Tabela de resultados
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Medias por Eixo:", ln=True)
    pdf.set_font("Arial", "", 12)
    for eixo_id, nota in medias.items():
        pdf.cell(0, 8, f"{nomes_eixos[eixo_id]}: {nota:.2f} / 5.0", ln=True)

    # 5. Exporta o PDF final
    caminho = "relatorio_final.pdf"
    pdf.output(caminho)
    
    # Remove o gráfico temporário para não acumular arquivos
    if os.path.exists("radar_temp.png"):
        os.remove("radar_temp.png")
        
    return caminho