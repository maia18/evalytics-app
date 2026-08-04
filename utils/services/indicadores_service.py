import logging

from database.services.firebase_config import db

logger = logging.getLogger(__name__)

# ATENÇÃO: coleção Firestore independente de database/indicadores.py (o arquivo
# local usado pela tela de Configurações e pelo Formulário). Os dois back-ends
# de indicadores não são sincronizados entre si — ver observação arquitetural.
COLECAO_INDICADORES = "indicadores"


def listar_indicadores() -> list[dict]:
    """Busca todos os indicadores de avaliação cadastrados no Firestore.

    Returns:
        Lista de dicionários, cada um representando um indicador com seu ID de documento.
    """
    try:
        docs = db.collection(COLECAO_INDICADORES).stream()
        return [{"id": doc.id, **doc.to_dict()} for doc in docs]

    except Exception:
        logger.exception("Erro ao buscar indicadores.")
        return []


def criar_indicador(nome: str, categoria: str) -> None:
    """Cadastra um novo indicador (pergunta/critério) no Firestore.

    Args:
        nome: texto descritivo do indicador (ex: "Clareza na exposição do conteúdo").
        categoria: eixo ao qual o indicador pertence (ex: "Didática", "Infraestrutura").
    """
    try:
        novo_indicador = {
            "nome": nome,
            "categoria": categoria,
            "ativo": True,  # Soft delete: permite desativar sem perder histórico de relatórios
        }
        db.collection(COLECAO_INDICADORES).add(novo_indicador)

    except Exception:
        logger.exception("Erro ao criar indicador '%s'.", nome)


def atualizar_indicador(id_indicador: str, novo_nome: str) -> None:
    """Atualiza o nome/texto de um indicador já existente.

    Args:
        id_indicador: ID do documento Firestore do indicador.
        novo_nome: novo texto que substituirá o valor atual.
    """
    try:
        # .update() (em vez de .set()) modifica só o campo informado e falha
        # propositalmente se o documento não existir, evitando registros "fantasmas"
        db.collection(COLECAO_INDICADORES).document(id_indicador).update({"nome": novo_nome})

    except Exception:
        logger.exception("Erro ao atualizar indicador '%s'.", id_indicador)