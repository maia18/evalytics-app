from fpdf import FPDF
import plotly.graph_objects as go
import os

# Classe personalizada para o relatório acadêmico
# Herdar da classe base FPDF permite sobrescrever os métodos de cabeçalho e rodapé
# para que eles sejam inseridos automaticamente em todas as páginas geradas!
class RelatorioAcademico(FPDF):
    def header(self):
        """Define o cabeçalho padrão repetido no topo de cada página."""
        # Configura a fonte: Família (Arial), Estilo (B=Bold), Tamanho (14)
        self.set_font("Arial", "B", 14)
        # ln=True quebra a linha, align="C" centraliza o texto
        self.cell(0, 10, "RELATORIO DE AVALIACAO INSTITUCIONAL", ln=True, align="C")
        
        # Desenha uma linha horizontal decorativa logo abaixo do título
        # Coordenadas: (x1=20, y1=26) até (x2=190, y2=26)
        self.line(20, 26, 190, 26) 
        self.ln(10) # Pula 10mm de espaço (respiro) vertical

    def footer(self):
        """Define o rodapé padrão repetido na base de cada página."""
        # set_y(-15) posiciona o cursor a exatos 15mm do final (fundo) da página
        self.set_y(-15)
        self.set_font("Arial", "I", 8) # Fonte em Itálico ("I")
        # A função self.page_no() retorna o número da página atual dinamicamente
        self.cell(0, 10, f"Pagina {self.page_no()}", align="C")

# Função principal para gerar o PDF
def gerar_pdf_resultados(medias, nomes_eixos):
    """
    Gera um relatório acadêmico em PDF, orquestrando a criação de um gráfico 
    de radar dinâmico (Plotly) e a estruturação do documento final (FPDF).
    
    Args:
        medias (dict): Dicionário no formato {id_eixo: média_numerica}.
        nomes_eixos (dict): Dicionário de mapeamento {id_eixo: "Nome do Eixo"}.
        
    Returns:
        str: O caminho do arquivo PDF salvo no disco.
    """

    # === 1. Criação do Gráfico de Radar (Plotly) ===
    fig = go.Figure()
    
    # Adiciona a camada de dados do gráfico polar (radar)
    fig.add_trace(go.Scatterpolar(
        # Ordenar pelas chaves (sorted) garante que as médias e os nomes coincidam perfeitamente nos vértices
        r=[medias[i] for i in sorted(medias.keys())],  # Eixo Radial: os valores das notas
        theta=[nomes_eixos[i] for i in sorted(medias.keys())],  # Eixo Angular: os rótulos (nomes dos eixos)
        fill='toself', # Preenche a área interna do polígono para melhor visualização de área
        fillcolor='rgba(33, 150, 243, 0.3)',  # Azul primário com 30% de opacidade
        line_color='rgb(33, 150, 243)',       # Cor sólida para as bordas externas
        marker=dict(size=8)                   # Aumenta as "bolinhas" nos vértices para destacar os pontos
    ))
    
    # Atualiza as configurações visuais estruturais do gráfico
    fig.update_layout(
        # Força o eixo radial a ir de 0 a 5. Isso é crucial para que as notas fiquem 
        # visualmente proporcionais em relação à nota máxima possível (5.0).
        polar=dict(radialaxis=dict(visible=True, range=[0, 5])), 
        showlegend=False # Esconde a legenda, pois as pontas do radar já servem como rótulos
    )
    
    # Salva o gráfico como uma imagem PNG temporária no disco para que o PDF possa importá-la
    fig.write_image("radar_temp.png")  

    # === 2. Configuração do Documento PDF ===
    pdf = RelatorioAcademico()
    # Aumenta as margens laterais para o texto não ficar muito espremido próximo às bordas do papel
    pdf.set_left_margin(25)
    pdf.set_right_margin(25)
    
    # A primeira chamada ao add_page() engatilha automaticamente o método header() da classe
    pdf.add_page()
    
    # === 3. Corpo do Texto Introdutório ===
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Analise de Desempenho", ln=True)
    pdf.set_font("Arial", "", 12) # Retorna para a fonte normal sem negrito
    
    texto_intro = (
        "Este relatorio apresenta os dados consolidados das avaliações institucionais. "
        "O gráfico abaixo ilustra o desempenho em cada eixo temático, permitindo uma "
        "visualização clara dos pontos de excelência e das áreas que necessitam de atenção pedagógica."
    )
    
    # multi_cell é ideal para parágrafos longos, realizando quebra de linha automática. 
    # align='J' garante o alinhamento justificado do bloco de texto.
    pdf.multi_cell(0, 7, texto_intro, align='J')  
    
    pdf.ln(5)
    
    # Insere a imagem temporária gerada pelo Plotly. 
    # x=55 desloca a imagem para a direita (ajudando a centralizá-la) e w=100 fixa sua largura.
    pdf.image("radar_temp.png", x=55, w=100)  
    pdf.ln(10)

    # === 4. Tabela/Lista de Resultados Numéricos ===
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Medias por Eixo:", ln=True)
    pdf.set_font("Arial", "", 12)
    
    # Itera sobre as médias e imprime o detalhamento linha a linha
    for eixo_id, nota in medias.items():
        # A formatação :.2f garante que a nota seja exibida com duas casas decimais (ex: 4.50)
        pdf.cell(0, 8, f"{nomes_eixos[eixo_id]}: {nota:.2f} / 5.0", ln=True)

    # === 5. Exportação e Limpeza ===
    caminho = "relatorio_final.pdf"
    pdf.output(caminho) # Grava o documento binário final no disco
    
    # Garbade collection manual: Limpeza essencial de arquivos residuais.
    # Evita que o diretório do servidor acumule imagens temporárias (radar_temp.png)
    if os.path.exists("radar_temp.png"):
        os.remove("radar_temp.png")
        
    return caminho