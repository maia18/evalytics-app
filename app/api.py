
import json
import logging
import os
import re
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import firebase_admin
from dotenv import load_dotenv
from fastapi import (
    Depends,
    FastAPI,
    File,
    Form,
    Header,
    HTTPException,
    UploadFile,
)
from firebase_admin import auth, firestore, storage
from pydantic import BaseModel, Field, ValidationError


# ============================================================
# CONFIGURAÇÕES
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("evalytics.api")

PROJECT_ID = os.getenv("FIREBASE_PROJECT_ID")
BUCKET_NAME = os.getenv("FIREBASE_STORAGE_BUCKET")

if not PROJECT_ID:
    raise RuntimeError(
        "FIREBASE_PROJECT_ID não definido no arquivo .env."
    )

if not BUCKET_NAME:
    raise RuntimeError(
        "FIREBASE_STORAGE_BUCKET não definido no arquivo .env."
    )

MAX_FILE_SIZE = (
    int(os.getenv("MAX_FILE_SIZE_MB", "10"))
    * 1024
    * 1024
)

MAX_FILES_PER_EVALUATION = int(
    os.getenv("MAX_FILES_PER_EVALUATION", "100")
)

MAX_FILES_PER_INDICATOR = int(
    os.getenv("MAX_FILES_PER_INDICATOR", "20")
)

if (
    MAX_FILE_SIZE <= 0
    or MAX_FILES_PER_EVALUATION <= 0
    or MAX_FILES_PER_INDICATOR <= 0
):
    raise RuntimeError(
        "Os limites de tamanho e quantidade de arquivos "
        "devem ser maiores que zero."
    )


# ============================================================
# TIPOS DE ARQUIVO PERMITIDOS
# ============================================================

ALLOWED_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".pdf",
    ".doc",
    ".docx",
    ".xls",
    ".xlsx",
    ".ppt",
    ".pptx",
    ".txt",
    ".csv",
    ".odt",
    ".ods",
    ".odp",
}

ALLOWED_MIME_TYPES = {
    "image/png",
    "image/jpeg",
    "image/webp",
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.ms-excel",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "application/vnd.ms-powerpoint",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    "text/plain",
    "text/csv",
    "application/vnd.oasis.opendocument.text",
    "application/vnd.oasis.opendocument.spreadsheet",
    "application/vnd.oasis.opendocument.presentation",
    "application/octet-stream",
}


# ============================================================
# FIREBASE ADMIN
# ============================================================

if not firebase_admin._apps:
    firebase_admin.initialize_app(
        options={
            "projectId": PROJECT_ID,
            "storageBucket": BUCKET_NAME,
        }
    )

db = firestore.client()
bucket = storage.bucket()


# ============================================================
# APLICAÇÃO FASTAPI
# ============================================================

app = FastAPI(
    title="Evalytics Evidence API",
    version="1.2.0",
    description=(
        "API para avaliações institucionais e gerenciamento "
        "de evidências do Evalytics."
    ),
)


# ============================================================
# MODELOS
# ============================================================

class EvidenceManifestItem(BaseModel):
    upload_id: str = Field(min_length=1, max_length=80)
    indicador_id: str = Field(min_length=1, max_length=200)
    filename: str = Field(min_length=1, max_length=255)


class EvaluationPayload(BaseModel):
    curso_id: str = Field(min_length=1, max_length=200)
    curso_nome: str = Field(min_length=1, max_length=300)
    respostas: dict[str, Any]
    justificativas: dict[str, str] = Field(default_factory=dict)


# ============================================================
# AUTENTICAÇÃO
# ============================================================

def require_user(
    authorization: str | None = Header(default=None),
) -> dict:
    """
    Valida o token de autenticação do Firebase enviado pelo cliente.
    """

    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Token de autenticação ausente.",
        )

    esquema, separador, token = authorization.partition(" ")

    if (
        not separador
        or esquema.lower() != "bearer"
        or not token.strip()
    ):
        raise HTTPException(
            status_code=401,
            detail="Cabeçalho de autenticação inválido.",
        )

    try:
        decoded_token = auth.verify_id_token(token.strip())

        if not decoded_token.get("uid"):
            raise ValueError("Token sem identificador de usuário.")

        return decoded_token

    except Exception as exc:
        logger.warning(
            "Token Firebase inválido ou expirado."
        )

        raise HTTPException(
            status_code=401,
            detail="Sessão inválida. Entre novamente.",
        ) from exc


def get_user_id(user: dict) -> str:
    """Obtém o UID do usuário autenticado."""

    uid = user.get("uid")

    if not uid:
        raise HTTPException(
            status_code=401,
            detail="Não foi possível identificar o usuário.",
        )

    return str(uid)


# ============================================================
# VALIDAÇÃO E SANITIZAÇÃO
# ============================================================

def safe_filename(name: str) -> str:
    """Remove caminhos e caracteres problemáticos do nome."""

    base = Path(name.replace("\\", "/")).name

    base = re.sub(
        r"[^A-Za-z0-9._() -]",
        "_",
        base,
    ).strip(" .")

    return (base or "evidencia")[:180]


def safe_path_segment(value: str) -> str:
    """Produz um segmento seguro para o caminho no Storage."""

    segment = re.sub(
        r"[^A-Za-z0-9_-]",
        "_",
        str(value),
    ).strip("_")

    if not segment:
        raise HTTPException(
            status_code=400,
            detail="Identificador de indicador inválido.",
        )

    return segment[:120]


def validate_file(
    upload: UploadFile,
    content: bytes,
) -> str:
    """
    Valida extensão, conteúdo vazio, tamanho e MIME declarado.
    Retorna o MIME normalizado.

    Observação: o MIME declarado não comprova, por si só,
    o formato real do conteúdo.
    """

    original_name = upload.filename or ""
    extension = Path(original_name).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=415,
            detail=(
                f"Formato não permitido: "
                f"{extension or 'sem extensão'}."
            ),
        )

    if not content:
        raise HTTPException(
            status_code=400,
            detail=f"O arquivo {original_name} está vazio.",
        )

    if len(content) > MAX_FILE_SIZE:
        limite_mb = MAX_FILE_SIZE // (1024 * 1024)

        raise HTTPException(
            status_code=413,
            detail=(
                f"O arquivo {original_name} excede "
                f"o limite de {limite_mb} MB."
            ),
        )

    mime = (
        upload.content_type or "application/octet-stream"
    ).lower().split(";", 1)[0].strip()

    if mime not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=415,
            detail=f"Tipo de conteúdo não permitido: {mime}.",
        )

    return mime


def validate_manifest(
    manifest: list[EvidenceManifestItem],
    files: list[UploadFile],
) -> None:
    """Valida correspondência, identificadores e limites dos anexos."""

    if len(files) != len(manifest):
        raise HTTPException(
            status_code=400,
            detail=(
                "A lista de arquivos não corresponde "
                "aos metadados enviados."
            ),
        )

    if len(files) > MAX_FILES_PER_EVALUATION:
        raise HTTPException(
            status_code=413,
            detail=(
                f"O limite de {MAX_FILES_PER_EVALUATION} "
                "arquivos por avaliação foi excedido."
            ),
        )

    upload_ids = [item.upload_id for item in manifest]

    if len(upload_ids) != len(set(upload_ids)):
        raise HTTPException(
            status_code=400,
            detail="Identificadores de upload duplicados.",
        )

    quantidade_por_indicador: dict[str, int] = {}

    for upload, item in zip(files, manifest):
        quantidade_por_indicador[item.indicador_id] = (
            quantidade_por_indicador.get(item.indicador_id, 0) + 1
        )

        if (
            quantidade_por_indicador[item.indicador_id]
            > MAX_FILES_PER_INDICATOR
        ):
            raise HTTPException(
                status_code=413,
                detail=(
                    f"O limite de {MAX_FILES_PER_INDICATOR} "
                    f"arquivos para o indicador "
                    f"{item.indicador_id} foi excedido."
                ),
            )

        nome_upload = upload.filename or ""
        nome_manifesto = item.filename

        if (
            Path(nome_upload).suffix.lower()
            != Path(nome_manifesto).suffix.lower()
        ):
            raise HTTPException(
                status_code=400,
                detail=(
                    "A extensão do arquivo não corresponde "
                    "ao manifesto de evidências."
                ),
            )


# ============================================================
# ACESSO ÀS AVALIAÇÕES
# ============================================================

def get_owned_evaluation(
    evaluation_id: str,
    uid: str,
):
    """
    Retorna uma avaliação apenas quando pertence ao usuário
    autenticado.
    """

    ref = db.collection("avaliacoes").document(evaluation_id)
    snapshot = ref.get()

    if not snapshot.exists:
        raise HTTPException(
            status_code=404,
            detail="Avaliação não encontrada.",
        )

    data = snapshot.to_dict() or {}

    if data.get("usuario_id") != uid:
        raise HTTPException(
            status_code=403,
            detail="Você não tem acesso a esta avaliação.",
        )

    return ref, data


# ============================================================
# SAÚDE DA API
# ============================================================

@app.get("/health")
def health():
    return {"status": "ok"}


# ============================================================
# LISTAGEM DE AVALIAÇÕES
# ============================================================

@app.get("/avaliacoes")
def list_evaluations(
    user: dict = Depends(require_user),
):
    uid = get_user_id(user)

    documentos = (
        db.collection("avaliacoes")
        .where("usuario_id", "==", uid)
        .stream()
    )

    avaliacoes = []

    for documento in documentos:
        dados = documento.to_dict() or {}
        dados["id"] = documento.id
        avaliacoes.append(dados)

    avaliacoes.sort(
        key=lambda item: item.get("data_avaliacao", ""),
        reverse=True,
    )

    return {"avaliacoes": avaliacoes}


# ============================================================
# CRIAÇÃO DE AVALIAÇÃO E UPLOAD DAS EVIDÊNCIAS
# ============================================================

@app.post("/avaliacoes", status_code=201)
async def create_evaluation(
    avaliacao: str = Form(...),
    evidencias: str = Form("[]"),
    files: list[UploadFile] = File(default=[]),
    user: dict = Depends(require_user),
):
    uid = get_user_id(user)

    # --------------------------------------------------------
    # Interpretar e validar os dados recebidos
    # --------------------------------------------------------

    try:
        payload = EvaluationPayload.model_validate_json(avaliacao)

        manifest_data = json.loads(evidencias)

        if not isinstance(manifest_data, list):
            raise ValueError(
                "O manifesto de evidências deve ser uma lista."
            )

        manifest = [
            EvidenceManifestItem.model_validate(item)
            for item in manifest_data
        ]

    except (ValueError, ValidationError, TypeError) as exc:
        raise HTTPException(
            status_code=400,
            detail=(
                "Dados da avaliação ou lista de "
                "evidências inválidos."
            ),
        ) from exc

    # --------------------------------------------------------
    # Validar os arquivos e o manifesto
    # --------------------------------------------------------

    validate_manifest(manifest, files)

    evaluation_ref = None
    uploaded_paths: list[str] = []

    try:
        now = datetime.now(timezone.utc).isoformat()

        evaluation_ref = db.collection("avaliacoes").document()

        evaluation_document = {
            "curso_id": payload.curso_id,
            "curso_nome": payload.curso_nome,
            "data_avaliacao": now,
            "respostas": payload.respostas,
            "justificativas": payload.justificativas,
            "usuario_id": uid,
            "evidencias": [],
        }

        # Cria o documento inicial da avaliação.
        evaluation_ref.set(evaluation_document)

        evidence_documents = []

        # A ordem de files deve ser a mesma do manifesto.
        for upload, item in zip(files, manifest, strict=True):
            # Lê no máximo um byte acima do limite para detectar
            # arquivos grandes sem carregá-los integralmente.
            content = await upload.read(MAX_FILE_SIZE + 1)

            mime = validate_file(upload, content)

            filename = safe_filename(item.filename)
            extension = Path(filename).suffix.lower()

            indicador_path = safe_path_segment(item.indicador_id)
            evidence_id = str(uuid.uuid4())

            object_path = (
                f"evidencias/{uid}/"
                f"{evaluation_ref.id}/"
                f"{indicador_path}/"
                f"{evidence_id}{extension}"
            )

            blob = bucket.blob(object_path)

            blob.metadata = {
                "ownerUid": uid,
                "evaluationId": evaluation_ref.id,
                "indicatorId": item.indicador_id,
                "originalFilename": filename,
            }

            # Registra antes do upload para que a rotina de
            # limpeza também tente remover eventuais uploads
            # parcialmente concluídos.
            uploaded_paths.append(object_path)

            blob.upload_from_string(
                content,
                content_type=mime,
            )

            evidence_documents.append(
                {
                    "id": evidence_id,
                    "upload_id": item.upload_id,
                    "indicador_id": item.indicador_id,
                    "nome": filename,
                    "caminho_storage": object_path,
                    "content_type": mime,
                    "tamanho_bytes": len(content),
                    "criado_em": now,
                }
            )

        # Salva os metadados depois de concluir os uploads.
        evaluation_ref.update(
            {"evidencias": evidence_documents}
        )

        logger.info(
            "Avaliação %s criada para o usuário %s. "
            "Evidências: %s",
            evaluation_ref.id,
            uid,
            len(evidence_documents),
        )

        return {
            "id": evaluation_ref.id,
            "evidencias": evidence_documents,
        }

    except HTTPException:
        _cleanup_partial_evaluation(
            evaluation_ref,
            uploaded_paths,
        )
        raise

    except Exception as exc:
        _cleanup_partial_evaluation(
            evaluation_ref,
            uploaded_paths,
        )

        logger.exception(
            "Erro ao salvar avaliação e evidências."
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Não foi possível salvar a avaliação "
                "e suas evidências."
            ),
        ) from exc

    finally:
        for upload in files:
            try:
                await upload.close()
            except Exception:
                logger.warning(
                    "Não foi possível fechar um arquivo recebido."
                )


def _cleanup_partial_evaluation(
    evaluation_ref,
    uploaded_paths: list[str],
) -> None:
    """Tenta remover arquivos e documento de uma operação incompleta."""

    for path in uploaded_paths:
        try:
            bucket.blob(path).delete()
        except Exception:
            logger.exception(
                "Falha ao remover upload parcial: %s",
                path,
            )

    if evaluation_ref is not None:
        try:
            evaluation_ref.delete()
        except Exception:
            logger.exception(
                "Falha ao remover avaliação incompleta: %s",
                evaluation_ref.id,
            )


# ============================================================
# LISTAGEM DE EVIDÊNCIAS DE UMA AVALIAÇÃO
# ============================================================

@app.get("/avaliacoes/{evaluation_id}/evidencias")
def list_evidence(
    evaluation_id: str,
    user: dict = Depends(require_user),
):
    uid = get_user_id(user)

    _, data = get_owned_evaluation(evaluation_id, uid)

    return {
        "evidencias": data.get("evidencias", [])
    }


# ============================================================
# URL TEMPORÁRIA PARA ACESSAR UMA EVIDÊNCIA
# ============================================================

@app.get(
    "/avaliacoes/{evaluation_id}/evidencias/"
    "{evidence_id}/url"
)
def get_evidence_url(
    evaluation_id: str,
    evidence_id: str,
    user: dict = Depends(require_user),
):
    uid = get_user_id(user)

    _, data = get_owned_evaluation(evaluation_id, uid)

    evidence = next(
        (
            item
            for item in data.get("evidencias", [])
            if item.get("id") == evidence_id
        ),
        None,
    )

    if not evidence:
        raise HTTPException(
            status_code=404,
            detail="Evidência não encontrada.",
        )

    storage_path = evidence.get("caminho_storage")

    if not storage_path:
        raise HTTPException(
            status_code=500,
            detail="O caminho da evidência não está cadastrado.",
        )

    try:
        blob = bucket.blob(storage_path)

        if not blob.exists():
            raise HTTPException(
                status_code=404,
                detail="Arquivo não encontrado no Storage.",
            )

        url = blob.generate_signed_url(
            version="v4",
            expiration=timedelta(minutes=5),
            method="GET",
        )

        return {
            "url": url,
            "expira_em_segundos": 300,
        }

    except HTTPException:
        raise

    except Exception as exc:
        logger.exception(
            "Não foi possível gerar a URL da evidência %s.",
            evidence_id,
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Não foi possível gerar o link "
                "temporário da evidência."
            ),
        ) from exc


# ============================================================
# EXCLUSÃO DE UMA EVIDÊNCIA
# ============================================================

@app.delete(
    "/avaliacoes/{evaluation_id}/evidencias/{evidence_id}"
)
def delete_evidence(
    evaluation_id: str,
    evidence_id: str,
    user: dict = Depends(require_user),
):
    uid = get_user_id(user)

    evaluation_ref, data = get_owned_evaluation(
        evaluation_id,
        uid,
    )

    evidence_list = data.get("evidencias", [])

    evidence = next(
        (
            item
            for item in evidence_list
            if item.get("id") == evidence_id
        ),
        None,
    )

    if not evidence:
        raise HTTPException(
            status_code=404,
            detail="Evidência não encontrada.",
        )

    storage_path = evidence.get("caminho_storage")

    if not storage_path:
        raise HTTPException(
            status_code=500,
            detail="O caminho da evidência não está cadastrado.",
        )

    # Exclui o arquivo e, em seguida, atualiza o Firestore.
    # As duas operações não formam uma transação única.
    try:
        bucket.blob(storage_path).delete()

        updated_evidence = [
            item
            for item in evidence_list
            if item.get("id") != evidence_id
        ]

        evaluation_ref.update(
            {"evidencias": updated_evidence}
        )

        logger.info(
            "Evidência %s removida da avaliação %s.",
            evidence_id,
            evaluation_id,
        )

        return {"ok": True}

    except Exception as exc:
        logger.exception(
            "Erro ao excluir evidência %s.",
            evidence_id,
        )

        raise HTTPException(
            status_code=500,
            detail="Não foi possível excluir a evidência.",
        ) from exc
