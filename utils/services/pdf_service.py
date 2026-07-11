from fpdf import FPDF
import plotly.graph_objects as go
import os

class RelatorioAcademico(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "RELATORIO DE AVALIACAO INSTITUCIONAL", ln=True, align="C")
        
        self.line(20, 26, 190, 26) 
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Pagina {self.page_no()}", align="C")

def gerar_pdf_resultados(medias, nomes_eixos):
    # 1. Gera o gráfico de radar (o elemento visual central)
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=[medias[i] for i in sorted(medias.keys())],
        theta=[nomes_eixos[i] for i in sorted(medias.keys())],
        fill='toself',
        fillcolor='rgba(33, 150, 243, 0.3)', # Preenchimento azul transparente
        line_color='rgb(33, 150, 243)',
        marker=dict(size=8) # Adiciona pontos nos vértices
    ))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 5])), showlegend=False)
    fig.write_image("radar_temp.png")

    # 2. Configura o documento com margens padrão
    pdf = RelatorioAcademico()
    pdf.set_left_margin(25)
    pdf.set_right_margin(25)
    pdf.add_page()
    
    # 3. Corpo do texto justificado para elegância visual
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Analise de Desempenho", ln=True)
    pdf.set_font("Arial", "", 12)
    texto_intro = "Este relatorio apresenta os dados consolidados das avaliações institucionais. O gráfico abaixo ilustra o desempenho em cada eixo temático, permitindo uma visualização clara dos pontos de excelência e das áreas que necessitam de atenção pedagógica."
    pdf.multi_cell(0, 7, texto_intro, align='J') # Texto justificado
    
    pdf.ln(5)
    pdf.image("radar_temp.png", x=55, w=100)
    pdf.ln(10)

    # 4. Tabela de resultados (semelhante ao estilo de dados cadastrais)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Medias por Eixo:", ln=True)
    pdf.set_font("Arial", "", 12)
    for eixo_id, nota in medias.items():
        pdf.cell(0, 8, f"{nomes_eixos[eixo_id]}: {nota:.2f} / 5.0", ln=True)

    caminho = "relatorio_final.pdf"
    pdf.output(caminho)
    
    if os.path.exists("radar_temp.png"):
        os.remove("radar_temp.png")
        
    return caminho