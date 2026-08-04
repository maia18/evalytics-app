import json
import logging
from pathlib import Path
from typing import Optional

from database.indicadores import INDICADORES

logger = logging.getLogger(__name__)

CAMINHO_ARQUIVO_INDICADORES = Path(__file__).resolve().parent / "indicadores.py"


def persistir_indicadores() -> None:
    """Grava o estado atual de INDICADORES de volta no arquivo de banco de dados.

    NOTA ARQUITETURAL: usar um arquivo .py como banco de dados (reescrito via
    json.dumps a cada alteração) é frágil — sem transações, sem lock de
    concorrência, e um valor None em qualquer campo quebra a reimportação do
    arquivo na próxima inicialização. O projeto já possui uma camada real de
    banco (Firestore); migrar os indicadores para lá é recomendado. Note também
    que existe uma coleção Firestore "indicadores" separada (indicadores_service.py),
    não sincronizada com este arquivo — ver observação arquitetural.
    """
    try:
        conteudo = f"INDICADORES = {json.dumps(INDICADORES, indent=4, ensure_ascii=False)}\n"
        CAMINHO_ARQUIVO_INDICADORES.write_text(conteudo, encoding="utf-8")
    except Exception:
        logger.exception("Erro ao persistir indicadores em disco.")
        raise


def buscar_indicador(titulo: str, eixo: int) -> Optional[dict]:
    """Busca linearmente o indicador correspondente ao título e eixo informados."""
    for item in INDICADORES:
        if item.get("titulo") == titulo and item.get("eixo") == eixo:
            return item
    return None


def contar_indicadores_por_eixo(eixo: int) -> int:
    """Conta quantos indicadores existem para um determinado eixo."""
    return sum(1 for item in INDICADORES if item.get("eixo") == eixo)


def listar_indicadores_por_eixo(eixo: Optional[int]) -> list[dict]:
    """Retorna todos os indicadores pertencentes a um eixo específico."""
    return [item for item in INDICADORES if item.get("eixo") == eixo]


def adicionar_indicador(titulo: str, eixo: Optional[int], descricao: str) -> None:
    """Cria e persiste um novo indicador, com 5 critérios vazios por padrão."""
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
    """Atualiza título e descrição de um indicador existente. Retorna True se encontrado."""
    item = buscar_indicador(titulo_atual, eixo)
    if item is None:
        return False

    item["titulo"] = novo_titulo
    item["descricao"] = nova_descricao
    persistir_indicadores()
    return True


def atualizar_criterios(titulo: str, eixo: int, novos_criterios: dict) -> bool:
    """Substitui os critérios de avaliação de um indicador. Retorna True se encontrado."""
    item = buscar_indicador(titulo, eixo)
    if item is None:
        return False

    item["criterios"] = novos_criterios
    persistir_indicadores()
    return True


def excluir_indicador(titulo: str, eixo: int) -> bool:
    """Remove permanentemente um indicador. Retorna True se encontrado e removido."""
    for idx, item in enumerate(INDICADORES):
        if item.get("titulo") == titulo and item.get("eixo") == eixo:
            INDICADORES.pop(idx)
            persistir_indicadores()
            return True
    return False