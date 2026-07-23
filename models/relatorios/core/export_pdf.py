from fpdf import FPDF
import plotly.graph_objects as go
import os
from datetime import datetime

# Importa o componente visual que exibirá a barra de sucesso ou erro (Snackbar) na interface do usuário
from models.avaliacoes.core.feedback import mostrar_feedback

# === CLASSE PERSONALIZADA FPDF ===
# Herdar da classe base FPDF permite sobrescrever os métodos de cabeçalho e rodapé
# para que eles sejam inseridos automaticamente em todas as páginas geradas!
class RelatorioEvalytics(FPDF):
    def header(self):
        """Define o cabeçalho padrão repetido no topo de cada página."""
        # Configura a fonte e a cor azul primária do tema (#1976D2)
        self.set_font("helvetica", "B", 16)
        self.set_text_color(25, 118, 210) 
        self.cell(0, 10, "Evalytics - Avaliação Institucional", ln=True, align="C")
        
        # Subtítulo em preto
        self.set_font("helvetica", "B", 12)
        self.set_text_color(0, 0, 0)
        self.cell(0, 10, "Relatório Consolidado de Eixos", ln=True, align="C")
        
        # Desenha uma linha horizontal decorativa logo abaixo do título
        self.line(20, 30, 190, 30) 
        self.ln(10) # Pula 10mm de espaço (respiro) vertical

    def footer(self):
        """Define o rodapé padrão repetido na base de cada página."""
        self.set_y(-15) # Posiciona o cursor a exatos 15mm do final (fundo) da página
        self.set_font("helvetica", "I", 8)
        self.set_text_color(100, 100, 100) # Texto em cinza discreto
        self.cell(0, 10, f"Página {self.page_no()}", align="C")


# === FUNÇÃO PRINCIPAL ===
def gerar_pdf_completo(page, medias: dict, nomes_eixos: dict, semestre: str = "2025.2"):
    """
    Gera um relatório acadêmico em PDF, orquestrando a criação de um gráfico 
    de radar dinâmico (Plotly), uma tabela de resultados e o feedback visual no Flet.
    
    Args:
        page: A página atual do Flet para injetar o alerta de sucesso/erro.
        medias (dict): Dicionário no formato {id_eixo: média_numerica}.
        nomes_eixos (dict): Dicionário de mapeamento {id_eixo: "Nome do Eixo"}.
        semestre (str): Identificador do semestre para a tabela.
        
    Returns:
        str/None: O caminho do arquivo PDF gerado ou None em caso de falha.
    """
    try:
        # === 1. Criação do Gráfico de Radar (Plotly) ===
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=[medias[i] for i in sorted(medias.keys())],
            theta=[nomes_eixos[i] for i in sorted(medias.keys())],
            fill='toself',
            fillcolor='rgba(33, 150, 243, 0.3)',
            line_color='rgb(33, 150, 243)',
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 5])), 
            showlegend=False
        )
        
        # Salva o gráfico como uma imagem PNG temporária
        fig.write_image("radar_temp.png")  

        # === 2. Configuração do Documento PDF ===
        # Instancia a classe personalizada com as medidas corretas
        pdf = RelatorioEvalytics(orientation="P", unit="mm", format="A4")
        pdf.set_left_margin(20)
        pdf.set_right_margin(20)
        pdf.add_page() # Engatilha a criação do cabeçalho
        
        # === 3. Metadados do Documento ===
        pdf.set_font("helvetica", "I", 10)
        pdf.set_text_color(100, 100, 100)
        data_geracao = datetime.now().strftime("%d/%m/%Y às %H:%M")
        pdf.cell(0, 5, f"Documento gerado em: {data_geracao}", ln=True, align="R")
        pdf.ln(5)
        
        # === 4. Texto Introdutório ===
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
        
        # === 5. Inserção do Gráfico ===
        # A largura útil da página A4 com margens de 20mm é 170mm. 
        # Colocando a imagem com w=100 e x=55 garantimos que ela fique perfeitamente centralizada.
        pdf.image("radar_temp.png", x=55, w=100)  
        pdf.ln(10)

        # === 6. Tabela Dinâmica de Resultados ===
        pdf.set_font("helvetica", "B", 11)
        pdf.set_fill_color(240, 240, 240)
        
        # Cálculos para a tabela ocupar exatamente a largura útil da tela (170mm)
        largura_semestre = 30
        qtde_eixos = len(medias) if len(medias) > 0 else 1 # Evita divisão por zero
        largura_coluna_eixo = 140 / qtde_eixos 
        
        # --- Linha de Cabeçalho da Tabela ---
        pdf.cell(largura_semestre, 10, "Semestre", border=1, fill=True, align="C")
        for eixo_id in sorted(medias.keys()):
            # O .upper() garante que os títulos das colunas fiquem padronizados
            pdf.cell(largura_coluna_eixo, 10, nomes_eixos[eixo_id].upper(), border=1, fill=True, align="C")
        pdf.ln()
        
        # --- Linha de Dados da Tabela ---
        pdf.set_font("helvetica", "", 11)
        pdf.cell(largura_semestre, 10, semestre, border=1, align="C")
        for eixo_id in sorted(medias.keys()):
            # Formata a nota para sempre ter 2 casas decimais (ex: 4.80)
            pdf.cell(largura_coluna_eixo, 10, f"{medias[eixo_id]:.2f}", border=1, align="C")
        pdf.ln()

        # === 7. Exportação Final ===
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"relatorio_evalytics_{timestamp}.pdf"
        
        pdf.output(nome_arquivo)
        
        # === 8. Limpeza e Feedback Visual ===
        if os.path.exists("radar_temp.png"):
            os.remove("radar_temp.png")
            
        mostrar_feedback(page, f"PDF gerado com sucesso: {nome_arquivo}", sucesso=True)
        return nome_arquivo
        
    except Exception as erro:
        # Garante que o arquivo temporário será apagado mesmo se o código quebrar no meio
        if os.path.exists("radar_temp.png"):
            os.remove("radar_temp.png")
            
        mostrar_feedback(page, f"Erro ao gerar o documento PDF: {erro}", sucesso=False)
        return None