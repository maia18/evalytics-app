import flet as ft
import logging as lg
from database.services.firebase_config import db # Importa a instância ativa do banco de dados

logger = lg.getLogger(__name__)
COLECAO_AVALIACOES = "avaliacoes_institucionais"

def _definir_cor_nota(nota_str: str) -> str:
    """Função utilitária (privada) que define a cor da nota baseada no seu valor numérico."""
    
    try:
        nota = float(nota_str)
        if nota >= 4.0:
            return ft.Colors.GREEN_700
        elif nota >= 3.0:
            return ft.Colors.ORANGE_700
        else:
            return ft.Colors.RED_700
    except ValueError:
        return ft.Colors.GREY_700

def obter_respostas_tabela() -> list[dict]:
    """Busca os dados brutos das avaliações no Firestore e os formata exatamente como a tabela de interface espera."""
    
    try:
        '''
        Busca os documentos. 
            Se quiser ordenar do mais recente para o mais antigo: 
                Troque .stream() por .order_by("timestamp", direction="DESCENDING").stream() (Isso exigirá a criação de um índice no console do Firebase).
        '''
        docs = db.collection(COLECAO_AVALIACOES).stream()
        linhas = []

        for doc in docs:
            dados = doc.to_dict()
            
            '''1. Tratamento da Data'''
            timestamp = dados.get("timestamp") # O Firestore geralmente retorna um objeto datetime (com fuso horário) ou um Timestamp.
            if timestamp:
                data_formatada = timestamp.strftime("%d/%m/%Y, %H:%M") # Converte para uma string amigável: Ex: "10/07/2026, 14:30"
            else:
                data_formatada = "Data desconhecida"

            '''2. Tratamento da Nota'''
            nota_bruta = dados.get("nota_geral", 0.0)
            nota_formatada = f"{nota_bruta:.1f}" # Supondo que a nota venha como float no banco. Formata para ter sempre 1 casa decimal (ex: 4.0).

            '''3. Montagem do Dicionário (Mapeamento do Banco -> Interface)'''
            linha = {
                "id": doc.id[:7].upper(), # Pega os primeiros 7 caracteres do ID real do Firestore para criar um ID legível na tabela
                "data": data_formatada,
                # Usa .get() com valor padrão (fallback) caso o campo não exista no documento
                "curso": dados.get("curso", "Não informado"),
                "eixo": dados.get("eixo_avaliado", "Geral"),
                "nota": nota_formatada,
                "cor_nota": _definir_cor_nota(nota_formatada),
                "comentario": dados.get("comentario", None),
            }
            
            linhas.append(linha)

        return linhas

    except Exception:
        logger.exception("Erro ao buscar dados das avaliações para a tabela.")
        return [] # Retorna uma lista vazia em caso de erro, garantindo que o Flet não crashe ao tentar renderizar a tabela.