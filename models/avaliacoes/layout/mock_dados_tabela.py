import flet as ft

# Dados de exemplo exibidos na tabela.
# TODO: substituir pela leitura real da coleção de avaliações assim que a
# camada de acesso a dados correspondente estiver disponível.
LINHAS_EXEMPLO: list[dict] = [
    {
        "id": "RES-004", 
        "data": "Hoje, 10:20", 
        "curso": "Engenharia", 
        "eixo": "Inovação",
        "nota": "4.8", 
        "cor_nota": ft.Colors.GREEN_700,
        "comentario": "Uso excelente de simulações em Python.",
    },
    {
        "id": "RES-003", 
        "data": "Hoje, 09:15", 
        "curso": "Administração", 
        "eixo": "Didática",
        "nota": "5.0", 
        "cor_nota": ft.Colors.GREEN_700,
        "comentario": None,
    },
    {
        "id": "RES-002", 
        "data": "Ontem, 15:45", 
        "curso": "Engenharia", 
        "eixo": "Infraestrutura",
        "nota": "3.0", 
        "cor_nota": ft.Colors.ORANGE_700,
        "comentario": "Laboratórios precisam de atualização.",
    }
]