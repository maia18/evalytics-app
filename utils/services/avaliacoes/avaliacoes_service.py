import json
import logging
import mimetypes
import os
import uuid

from contextlib import ExitStack
from pathlib import Path

import requests

from components.core.auth.auth_state import auth_state


logger = logging.getLogger(__name__)

API_URL = os.getenv("EVALYTICS_API_URL", "").rstrip("/")

TIMEOUT_UPLOAD = 120
TAMANHO_MAXIMO_ARQUIVO = 10 * 1024 * 1024
QUANTIDADE_MAXIMA_ARQUIVOS_POR_INDICADOR = 20

EXTENSOES_PERMITIDAS = {
    "png", "jpg", "jpeg", "webp",
    "pdf",
    "doc", "docx",
    "xls", "xlsx",
    "ppt", "pptx",
    "txt", "csv",
    "odt", "ods", "odp",
}


def _obter_headers() -> dict[str, str]:
    """Obtém o token de autenticação da sessão atual."""

    token = auth_state.id_token

    if not token:
        raise ValueError(
            "Sessão expirada ou usuário não autenticado."
        )

    return {
        "Authorization": f"Bearer {token}",
    }


def _preparar_anexos(
    anexos: dict | None,
) -> tuple[list[dict], list[dict]]:
    """
    Valida os anexos e prepara o manifesto do upload.

    A chave do dicionário é o ID do indicador.
    """

    manifest = []
    arquivos = []

    anexos = anexos or {}

    for indicador_id, lista_anexos in anexos.items():
        indicador_id = str(indicador_id)

        if not isinstance(lista_anexos, list):
            raise ValueError(
                f"Lista de anexos inválida para o indicador "
                f"{indicador_id}."
            )

        if len(lista_anexos) > QUANTIDADE_MAXIMA_ARQUIVOS_POR_INDICADOR:
            raise ValueError(
                f"O indicador {indicador_id} excede o limite "
                f"de {QUANTIDADE_MAXIMA_ARQUIVOS_POR_INDICADOR} arquivos."
            )

        for anexo in lista_anexos:
            caminho_original = anexo.get("caminho")
            nome_original = anexo.get("nome")

            if not caminho_original or not nome_original:
                raise ValueError(
                    "Um anexo não possui nome ou caminho válido."
                )

            caminho = str(Path(caminho_original).resolve())
            nome = Path(nome_original).name
            extensao = Path(nome).suffix.lower().lstrip(".")

            if extensao not in EXTENSOES_PERMITIDAS:
                raise ValueError(
                    f"Formato não permitido: {nome}."
                )

            if not os.path.isfile(caminho):
                raise FileNotFoundError(
                    f"O arquivo não foi encontrado: {nome}."
                )

            tamanho = os.path.getsize(caminho)

            if tamanho <= 0:
                raise ValueError(
                    f"O arquivo '{nome}' está vazio."
                )

            if tamanho > TAMANHO_MAXIMO_ARQUIVO:
                raise ValueError(
                    f"O arquivo '{nome}' excede o limite de 10 MB."
                )

            upload_id = str(uuid.uuid4())

            manifest.append(
                {
                    "upload_id": upload_id,
                    "indicador_id": indicador_id,
                    "filename": nome,
                }
            )

            arquivos.append(
                {
                    "upload_id": upload_id,
                    "caminho": caminho,
                    "nome": nome,
                    "tamanho": tamanho,
                    "indicador_id": indicador_id,
                }
            )

    return manifest, arquivos


def salvar_avaliacao(
    curso_id: str,
    curso_nome: str,
    respostas: dict,
    justificativas: dict | None = None,
    anexos: dict | None = None,
) -> bool:
    """
    Envia a avaliação e as evidências ao backend FastAPI.

    O backend deve persistir os dados no Firestore e os arquivos
    no Firebase Storage.
    """

    if not API_URL:
        logger.error(
            "EVALYTICS_API_URL não foi configurada."
        )
        return False

    try:
        headers = _obter_headers()

        manifest, arquivos = _preparar_anexos(anexos)

        dados_avaliacao = {
            "curso_id": curso_id,
            "curso_nome": curso_nome,
            "respostas": respostas,
            "justificativas": justificativas or {},
        }

        dados_formulario = {
            "avaliacao": json.dumps(
                dados_avaliacao,
                ensure_ascii=False,
            ),
            "evidencias": json.dumps(
                manifest,
                ensure_ascii=False,
            ),
        }

        with ExitStack() as stack:
            arquivos_multipart = []

            for arquivo in arquivos:
                stream = stack.enter_context(
                    open(arquivo["caminho"], "rb")
                )

                tipo_mime = (
                    mimetypes.guess_type(arquivo["nome"])[0]
                    or "application/octet-stream"
                )

                arquivos_multipart.append(
                    (
                        "files",
                        (
                            arquivo["nome"],
                            stream,
                            tipo_mime,
                        ),
                    )
                )

            resposta = requests.post(
                f"{API_URL}/avaliacoes",
                headers=headers,
                data=dados_formulario,
                files=arquivos_multipart,
                timeout=TIMEOUT_UPLOAD,
            )

        resposta.raise_for_status()

        logger.info(
            "Avaliação do curso '%s' enviada com sucesso. "
            "Arquivos enviados: %s.",
            curso_nome,
            len(arquivos),
        )

        return True

    except requests.Timeout:
        logger.error(
            "Tempo limite excedido ao enviar a avaliação."
        )
        return False

    except requests.HTTPError:
        logger.exception(
            "O backend recusou o envio da avaliação. "
            "Status HTTP: %s.",
            (
                resposta.status_code
                if "resposta" in locals()
                else "indisponível"
            ),
        )
        return False

    except requests.RequestException:
        logger.exception(
            "Falha de comunicação com o backend."
        )
        return False

    except Exception:
        logger.exception(
            "Erro ao enviar a avaliação do curso '%s'.",
            curso_nome,
        )
        return False


def listar_avaliacoes() -> list[dict]:
    """Consulta as avaliações pela API autenticada."""

    if not API_URL:
        logger.error(
            "EVALYTICS_API_URL não foi configurada."
        )
        return []

    try:
        resposta = requests.get(
            f"{API_URL}/avaliacoes",
            headers=_obter_headers(),
            timeout=30,
        )

        resposta.raise_for_status()
        dados = resposta.json()

        if isinstance(dados, list):
            return dados

        if isinstance(dados, dict):
            return dados.get("avaliacoes", [])

        return []

    except requests.RequestException:
        logger.exception(
            "Erro de comunicação ao consultar avaliações."
        )
        return []

    except Exception:
        logger.exception(
            "Erro ao consultar avaliações pela API."
        )
        return []