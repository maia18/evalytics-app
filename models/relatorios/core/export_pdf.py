from fpdf import FPDF
# Importa o componente visual que exibirá a barra de sucesso ou erro (Snackbar) na interface do usuário
from models.avaliacoes.core.feedback import mostrar_feedback
from datetime import datetime

def gerar_pdf(page):
    """
    Gera e salva fisicamente um relatório em formato PDF contendo as métricas de avaliação.
    Utiliza a biblioteca FPDF para desenhar a estrutura do documento e o Flet para o feedback visual.
    
    Args:
        page: A página atual do Flet, necessária para injetar o aviso de sucesso/erro na tela.
    """
    try:
        # Inicializa o motor do PDF especificando:
        # orientation="P" (Portrait/Retrato)
        # unit="mm" (unidade de medida em milímetros para desenhar na tela)
        # format="A4" (Tamanho padrão de folha)
        pdf = FPDF(orientation="P", unit="mm", format="A4")
        pdf.add_page() # Adiciona a primeira página em branco onde começaremos a desenhar
        
        # === CABEÇALHO ===
        # Configura a fonte: Família (Helvetica), Estilo (B=Bold/Negrito), Tamanho (16)
        pdf.set_font("helvetica", "B", 16)
        
        # O RGB (25, 118, 210) equivale ao azul primário do tema (#1976D2)
        pdf.set_text_color(25, 118, 210) 
        
        # Cria uma célula (bloco de texto). 
        # width=0 significa que ela vai ocupar toda a largura da página até a margem direita.
        # ln=True força uma quebra de linha após a célula. align="C" centraliza o texto.
        pdf.cell(0, 10, "Evalytics - Avaliação Institucional", ln=True, align="C")
        
        # Muda a fonte para o subtítulo (tamanho menor e cor preta)
        pdf.set_font("helvetica", "B", 12)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 10, "Relatório Consolidado de Eixos", ln=True, align="C")
        
        # Pula 5 milímetros verticalmente (um respiro visual)
        pdf.ln(5) 
        
        # === METADADOS DO DOCUMENTO ===
        # Usa estilo Itálico ("I") e uma cor cinza (100, 100, 100)
        pdf.set_font("helvetica", "I", 10)
        pdf.set_text_color(100, 100, 100)
        
        # Captura o momento exato em que o botão foi clicado e formata a data/hora
        data_geracao = datetime.now().strftime("%d/%m/%Y às %H:%M")
        
        # Alinha à direita ("R")
        pdf.cell(0, 10, f"Documento gerado em: {data_geracao}", ln=True, align="R")
        
        pdf.ln(10) # Pula 10 milímetros antes do corpo do texto
        
        # === CONTEÚDO PRINCIPAL (MOCK DATA) ===
        # Fonte regular (""), tamanho 12, texto preto
        pdf.set_font("helvetica", "", 12)
        pdf.set_text_color(0, 0, 0)
        
        # multi_cell permite que textos longos quebrem de linha automaticamente se passarem da margem.
        pdf.multi_cell(0, 8, txt=(
            "Este relatório apresenta os resultados preliminares "
            "coletados através dos formulários de avaliação docente e de infraestrutura. "
            "Os dados abaixo representam a consolidação bruta do semestre selecionado."
        ))
        
        pdf.ln(10)
        
        # === CONSTRUÇÃO DA TABELA ===
        # --- Linha de Cabeçalho da Tabela ---
        pdf.set_font("helvetica", "B", 11)
        pdf.set_fill_color(240, 240, 240) # Fundo cinza claro para destacar o cabeçalho
        
        # Desenha as células estipulando larguras fixas (40, 50, 50, 50 mm).
        # border=1 desenha a caixa ao redor. fill=True aplica a cor de fundo definida acima.
        pdf.cell(40, 10, "Semestre", border=1, fill=True, align="C")
        pdf.cell(50, 10, "Infraestrutura", border=1, fill=True, align="C")
        pdf.cell(50, 10, "Didática", border=1, fill=True, align="C")
        pdf.cell(50, 10, "Inovação", border=1, fill=True, align="C")
        pdf.ln() # Quebra a linha para desenhar os dados abaixo
        
        # --- Linha de Dados da Tabela ---
        pdf.set_font("helvetica", "", 11) # Retira o negrito
        
        # Desenha as células com as mesmas larguras para alinharem perfeitamente sob o cabeçalho
        pdf.cell(40, 10, "2025.2", border=1, align="C")
        pdf.cell(50, 10, "4.8", border=1, align="C")
        pdf.cell(50, 10, "4.5", border=1, align="C")
        pdf.cell(50, 10, "4.7", border=1, align="C")
        pdf.ln()

        # === EXPORTAÇÃO E FEEDBACK ===
        # Cria um nome único usando a data e hora para evitar sobrescrever arquivos antigos (ex: relatorio_evalytics_20260405_153022.pdf)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"relatorio_evalytics_{timestamp}.pdf"
        
        # Escreve o documento no disco (na mesma pasta em que o script está sendo rodado)
        pdf.output(nome_arquivo)
        
        # Emite um alerta visual de sucesso verde na interface (Snackbar)
        mostrar_feedback(page, f"PDF gerado com sucesso: {nome_arquivo}", sucesso=True)
        
    except Exception as erro:
        # Se algo falhar (ex: arquivo aberto, falta de permissão), exibe um alerta de erro vermelho
        mostrar_feedback(page, f"Erro ao gerar o documento PDF: {erro}", sucesso=False)