import json
import logging
from pathlib import Path
from typing import Optional
from database.indicadores import INDICADORES # Importa a lista em memória que guarda o estado atual dos indicadores durante a execução do app.

logger = logging.getLogger(__name__)
CAMINHO_ARQUIVO_INDICADORES = Path(__file__).resolve().parent / "indicadores.py" # Resolve o caminho absoluto para o arquivo que será usado como banco de dados em texto.

def persistir_indicadores() -> None:
    """
    Grava o estado atual da lista INDICADORES de volta no arquivo físico em disco.

    NOTA ARQUITETURAL: usar um arquivo .py como banco de dados (reescrito via json.dumps a cada alteração) é frágil — sem transações, sem lock de concorrência, e um valor None em qualquer campo quebra a reimportação do arquivo na próxima inicialização. O projeto já possui uma camada real de banco (Firestore); migrar os indicadores para lá é altamente recomendado numa próxima etapa.
    """
    
    try:
        conteudo = f"INDICADORES = {json.dumps(INDICADORES, indent=4, ensure_ascii=False)}\n" # Converte a lista de dicionários Python para uma string JSON formatada (indent=4) e garante a acentuação correta.
        
        CAMINHO_ARQUIVO_INDICADORES.write_text(conteudo, encoding="utf-8") # Sobrescreve o arquivo inteiro com o novo conteúdo.
    except Exception:
        logger.exception("Erro ao persistir indicadores em disco.")
        raise

# Busca linearmente e retorna o indicador correspondente ao título e eixo informados, se existir.
def buscar_indicador(titulo: str, eixo: int) -> Optional[dict]:
    for item in INDICADORES:
        if item.get("titulo") == titulo and item.get("eixo") == eixo:
            return item
    return None

# Conta de forma otimizada quantos indicadores existem para um determinado eixo usando generator expression.
def contar_indicadores_por_eixo(eixo: int) -> int:
    return sum(1 for item in INDICADORES if item.get("eixo") == eixo)

# Filtra e retorna todos os indicadores pertencentes a um eixo específico usando List Comprehension.
def listar_indicadores_por_eixo(eixo: Optional[int]) -> list[dict]:
    return [item for item in INDICADORES if item.get("eixo") == eixo]

# Cria, formata e persiste um novo indicador na memória e no disco
def adicionar_indicador(titulo: str, eixo: Optional[int], descricao: str) -> None:
    novo_item = {
        "titulo": titulo,
        "eixo": eixo,
        "descricao": descricao,
        "status": "ATIVO",
        "criterios": {str(i): "" for i in range(1, 6)}, # Gera 5 chaves de critérios (1 a 5) vazias por padrão.
    }
    INDICADORES.append(novo_item)
    persistir_indicadores()

# Atualiza metadados básicos (título e descrição) de um indicador existente. Retorna True em caso de sucesso
def atualizar_indicador(titulo_atual: str, eixo: int, novo_titulo: str, nova_descricao: str) -> bool:
    item = buscar_indicador(titulo_atual, eixo)
    if item is None:
        return False
        
    item["titulo"] = novo_titulo
    item["descricao"] = nova_descricao
    persistir_indicadores()
    return True

# Substitui o bloco de critérios de avaliação de um indicador. Retorna True se encontrado
def atualizar_criterios(titulo: str, eixo: int, novos_criterios: dict) -> bool:
    item = buscar_indicador(titulo, eixo)
    if item is None:
        return False
        
    item["criterios"] = novos_criterios
    persistir_indicadores()
    return True

# Remove um indicador permanentemente do banco buscando pelo índice. Retorna True se removido
def excluir_indicador(titulo: str, eixo: int) -> bool:
    for idx, item in enumerate(INDICADORES):
        if item.get("titulo") == titulo and item.get("eixo") == eixo:
            INDICADORES.pop(idx)
            persistir_indicadores()
            return True
    return False