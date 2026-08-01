import flet as ft
from typing import Optional
import csv
from models.avaliacoes.core.feedback import mostrar_feedback
from models.avaliacoes.core.filename_generator import gerar_nome_arquivo

'''
Dados de exemplo usados quando nenhum dado real é fornecido
    TODO: substituir pela leitura real da coleção de avaliações assim que a
    camada de acesso a dados (ex.: firestore_avaliacoes.py) estiver disponível
'''
DADOS_EXEMPLO_EXPORTACAO: list[list[str]] = [
    ["ID_Resposta", "Data_Hora", "Curso", "Eixo_Avaliado", "Nota_Geral", "Comentario"],
    ["RES-001", "2026-07-10 14:30", "Engenharia", "Didática", "4.5", "Ótima metodologia."],
    ["RES-002", "2026-07-10 15:45", "Engenharia", "Infraestrutura", "3.0", "Laboratórios precisam de atualização."],
    ["RES-003", "2026-07-11 09:15", "Administração", "Didática", "5.0", ""],
    ["RES-004", "2026-07-11 10:20", "Engenharia", "Inovação", "4.8", "Uso excelente de simulações em Python."],
]

# Exporta os dados informados (ou os dados de exemplo) para um arquivo CSV
def exportar_csv(page: ft.Page, dados_exportacao: Optional[list[list[str]]] = None) -> None:
    if dados_exportacao is None:
        dados_exportacao = DADOS_EXEMPLO_EXPORTACAO
        
    # Chama o módulo utilitário para gerar um nome de arquivo único
    nome_arquivo = gerar_nome_arquivo()

    try:
        
        # O bloco 'with' garante que o arquivo seja fechado automaticamente e em segurança após a escrita.
        with open(nome_arquivo, mode="w", newline="", encoding="utf-8") as arquivo_csv:

            # O separador ';' é padrão em Excel brasileiro
            escritor = csv.writer(arquivo_csv, delimiter=";")
            escritor.writerows(dados_exportacao)

        mostrar_feedback(page, f"Arquivo CSV exportado com sucesso: {nome_arquivo}", sucesso=True) # Dispara notificação visual para o usuário confirmando o sucesso do download/criação do arquivo
        
    except Exception as erro:
        mostrar_feedback(page, f"Erro ao exportar: {erro}", sucesso=False) # Notifica o usuário em caso de permissão negada ou outro erro de sistema