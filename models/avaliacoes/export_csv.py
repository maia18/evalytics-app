import csv
from models.avaliacoes.filename_generator import gerar_nome_arquivo
from models.avaliacoes.feedback import mostrar_feedback

def exportar_csv(page, dados_exportacao=None):
    
    """
    Exporta dados simulados ou recebidos para CSV.
    """
    
    if dados_exportacao is None:
        dados_exportacao = [
            ["ID_Resposta", "Data_Hora", "Curso", "Eixo_Avaliado", "Nota_Geral", "Comentario"],
            ["RES-001", "2026-07-10 14:30", "Engenharia", "Didática", "4.5", "Ótima metodologia."],
            ["RES-002", "2026-07-10 15:45", "Engenharia", "Infraestrutura", "3.0", "Laboratórios precisam de atualização."],
            ["RES-003", "2026-07-11 09:15", "Administração", "Didática", "5.0", ""],
            ["RES-004", "2026-07-11 10:20", "Engenharia", "Inovação", "4.8", "Uso excelente de simulações em Python."],
        ]

    nome_arquivo = gerar_nome_arquivo()

    try:
        with open(nome_arquivo, mode="w", newline="", encoding="utf-8") as arquivo_csv:
            escritor = csv.writer(arquivo_csv, delimiter=";")
            escritor.writerows(dados_exportacao)

        mostrar_feedback(page, f"Arquivo CSV exportado com sucesso: {nome_arquivo}", sucesso=True)
    except Exception as erro:
        mostrar_feedback(page, f"Erro ao exportar: {erro}", sucesso=False)
