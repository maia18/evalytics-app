import json
import logging
from pathlib import Path
from typing import Optional

from database.indicadores import INDICADORES

logger = logging.getLogger(__name__)

# Define onde salvar as modificações (sobrescreverá o próprio arquivo fonte de origem dos dados)
CAMINHO_ARQUIVO_INDICADORES = Path(__file__).resolve().parent / "indicadores.py"

def persistir_indicadores() -> None:
    """Grava o estado atual de INDICADORES de volta no arquivo de texto.

    NOTA ARQUITETURAL: O uso de arquivo .py reescrito por json.dumps é frágil para concorrência.
    É uma abordagem válida de prototipagem, mas recomenda-se migrar este módulo para usar o Firestore 
    da mesma forma que os arquivos da primeira seção.
    """
    try:
        # Formata como string e injeta a variável no topo para ser importada como módulo Python válido depois.
        conteudo = f"INDICADORES = {json.dumps(INDICADORES, indent=4, ensure_ascii=False)}\n"
        CAMINHO_ARQUIVO_INDICADORES.write_text(conteudo, encoding="utf-8")
    except Exception:
        logger.exception("Erro ao persistir indicadores em disco.")
        raise

def buscar_indicador(titulo: str, eixo: int) -> Optional[dict]:
    """Busca um indicador específico varrendo a lista em memória."""
    for item in INDICADORES:
        if item.get("titulo") == titulo and item.get("eixo") == eixo:
            return item
    return None

def contar_indicadores_por_eixo(eixo: int) -> int:
    """Calcula quantidade usando Generators eficientes em memória."""
    return sum(1 for item in INDICADORES if item.get("eixo") == eixo)

def listar_indicadores_por_eixo(eixo: Optional[int]) -> list[dict]:
    """Filtra indicadores de uma categoria (eixo) com List Comprehension."""
    return [item for item in INDICADORES if item.get("eixo") == eixo]

def adicionar_indicador(titulo: str, eixo: Optional[int], descricao: str) -> None:
    """Adiciona na lista de memória e comanda o salvamento no arquivo físico."""
    novo_item = {
        "titulo": titulo,
        "eixo": eixo,
        "descricao": descricao,
        "status": "ATIVO",
        "criterios": {str(i): "" for i in range(1, 6)},
    }
    INDICADORES.append(novo_item)
    persistir_indicadores()

def atualizar_indicador(titulo_atual: str, eixo: int, novo_titulo: str, nova_descricao: str) -> bool:
    """Altera campos textuais básicos se o indicador existir."""
    item = buscar_indicador(titulo_atual, eixo)
    if item is None:
        return False

    item["titulo"] = novo_titulo
    item["descricao"] = nova_descricao
    persistir_indicadores()
    return True

def atualizar_criterios(titulo: str, eixo: int, novos_criterios: dict) -> bool:
    """Altera apenas o bloco contendo a definição das notas dos critérios."""
    item = buscar_indicador(titulo, eixo)
    if item is None:
        return False

    item["criterios"] = novos_criterios
    persistir_indicadores()
    return True

def excluir_indicador(titulo: str, eixo: int) -> bool:
    """Remove definitivamente o indicador via POP da lista e reescreve o arquivo físico."""
    for idx, item in enumerate(INDICADORES):
        if item.get("titulo") == titulo and item.get("eixo") == eixo:
            INDICADORES.pop(idx)
            persistir_indicadores()
            return True
    return False