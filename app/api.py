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
# CONFIGURAÇÃO
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("evalytics.api")

PROJECT_ID = os.getenv("FIREBASE_PROJECT_ID")
BUCKET_NAME = os.getenv("FIREBASE_STORAGE_BUCKET")

if not PROJECT_ID or not BUCKET_NAME:
    raise RuntimeError(
        "Defina FIREBASE_PROJECT_ID e FIREBASE_STORAGE_BUCKET no .env."
    )

MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE_MB", "10")) * 1024 * 1024
MAX_FILES_PER_EVALUATION = int(
    os.getenv("MAX_FILES_PER_EVALUATION", "100")
)
MAX_FILES_PER_INDICATOR = int(
    os.getenv("MAX_FILES_PER_INDICATOR", "20")
)

if min(
    MAX_FILE_SIZE,
    MAX_FILES_PER_EVALUATION,
    MAX_FILES_PER_INDICATOR,
) <= 0:
    raise RuntimeError("Os limites de arquivos devem ser maiores que zero.")

ALLOWED_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".webp",
    ".pdf", ".doc", ".docx",
    ".xls", ".xlsx", ".ppt", ".pptx",
    ".txt", ".csv", ".odt", ".ods", ".odp",
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
# FIREBASE
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
# FASTAPI E MODELOS
# ============================================================

app = FastAPI(
    title="Evalytics Evidence API",
    version="1.2.0",
    description=(
        "API para avaliações institucionais e gerenciamento "
        "de evidências do Evalytics."
    ),
)


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
        usuario = auth.verify_id_token(token.strip())

        if not usuario.get("uid"):
            raise ValueError("Token sem UID.")

        return usuario

    except Exception as exc:
        logger.warning("Token Firebase inválido ou expirado.")

        raise HTTPException(
            status_code=401,
            detail="Sessão inválida. Entre novamente.",
        ) from exc


def get_user_id(user: dict) -> str:
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
    nome = Path(name.replace("\\", "/")).name
    nome = re.sub(r"[^A-Za-z0-9._() -]", "_", nome).strip(" .")
    return (nome or "evidencia")[:180]


def safe_path_segment(value: str) -> str:
    segmento = re.sub(r"[^A-Za-z0-9_-]", "_", str(value)).strip("_")

    if not segmento:
        raise HTTPException(
            status_code=400,
            detail="Identificador de indicador inválido.",
        )

    return segmento[:120]


def validate_file(upload: UploadFile, content: bytes) -> str:
    nome = upload.filename or ""
    extensao = Path(nome).suffix.lower()

    if extensao not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=415,
            detail=f"Formato não permitido: {extensao or 'sem extensão'}.",
        )

    if not content:
        raise HTTPException(
            status_code=400,
            detail=f"O arquivo {nome} está vazio.",
        )

    if len(content) > MAX_FILE_SIZE:
        limite_mb = MAX_FILE_SIZE // (1024 * 1024)
        raise HTTPException(
            status_code=413,
            detail=f"O arquivo {nome} excede o limite de {limite_mb} MB.",
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
    if len(files) != len(manifest):
        raise HTTPException(
            status_code=400,
            detail="A lista de arquivos não corresponde aos metadados enviados.",
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
        indicador_id = item.indicador_id

        quantidade_por_indicador[indicador_id] = (
            quantidade_por_indicador.get(indicador_id, 0) + 1
        )

        if (
            quantidade_por_indicador[indicador_id]
            > MAX_FILES_PER_INDICATOR
        ):
            raise HTTPException(
                status_code=413,
                detail=(
                    f"O limite de {MAX_FILES_PER_INDICATOR} arquivos "
                    f"para o indicador {indicador_id} foi excedido."
                ),
            )

        extensao_upload = Path(upload.filename or "").suffix.lower()
        extensao_manifesto = Path(item.filename).suffix.lower()

        if extensao_upload != extensao_manifesto:
            raise HTTPException(
                status_code=400,
                detail="A extensão do arquivo não corresponde ao manifesto.",
            )


# ============================================================
# ACESSO ÀS AVALIAÇÕES
# ============================================================

def get_owned_evaluation(evaluation_id: str, uid: str):
    referencia = db.collection("avaliacoes").document(evaluation_id)
    snapshot = referencia.get()

    if not snapshot.exists:
        raise HTTPException(
            status_code=404,
            detail="Avaliação não encontrada.",
        )

    dados = snapshot.to_dict() or {}

    if dados.get("usuario_id") != uid:
        raise HTTPException(
            status_code=403,
            detail="Você não tem acesso a esta avaliação.",
        )

    return referencia, dados


def cleanup_partial_evaluation(
    evaluation_ref,
    uploaded_paths: list[str],
) -> None:
    """Remove os arquivos e o documento de uma operação incompleta."""

    for caminho in uploaded_paths:
        try:
            bucket.blob(caminho).delete()
        except Exception:
            logger.exception("Falha ao remover upload parcial: %s", caminho)

    if evaluation_ref is not None:
        try:
            evaluation_ref.delete()
        except Exception:
            logger.exception(
                "Falha ao remover avaliação incompleta: %s",
                evaluation_ref.id,
            )


# ============================================================
# SAÚDE E LISTAGEM
# ============================================================

@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/avaliacoes")
def list_evaluations(user: dict = Depends(require_user)):
    logger.info("Iniciando listagem de avaliações.")

    uid = get_user_id(user)
    logger.info("UID autenticado obtido.")

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
# CRIAÇÃO DA AVALIAÇÃO E UPLOAD PERMANENTE
# ============================================================

@app.post("/avaliacoes", status_code=201)
async def create_evaluation(
    avaliacao: str = Form(...),
    evidencias: str = Form("[]"),
    files: list[UploadFile] = File(default=[]),
    user: dict = Depends(require_user),
):
    uid = get_user_id(user)

    try:
        payload = EvaluationPayload.model_validate_json(avaliacao)
        manifest_data = json.loads(evidencias)

        if not isinstance(manifest_data, list):
            raise ValueError("O manifesto deve ser uma lista.")

        manifest = [
            EvidenceManifestItem.model_validate(item)
            for item in manifest_data
        ]

    except (ValueError, ValidationError, TypeError) as exc:
        raise HTTPException(
            status_code=400,
            detail="Dados da avaliação ou lista de evidências inválidos.",
        ) from exc

    evaluation_ref = None
    uploaded_paths: list[str] = []

    try:
        validate_manifest(manifest, files)

        now = datetime.now(timezone.utc).isoformat()
        evaluation_ref = db.collection("avaliacoes").document()

        evaluation_ref.set({
            "curso_id": payload.curso_id,
            "curso_nome": payload.curso_nome,
            "data_avaliacao": now,
            "respostas": payload.respostas,
            "justificativas": payload.justificativas,
            "usuario_id": uid,
            "evidencias": [],
        })

        evidence_documents = []

        for upload, item in zip(files, manifest, strict=True):
            content = await upload.read(MAX_FILE_SIZE + 1)
            mime = validate_file(upload, content)

            filename = safe_filename(item.filename)
            extension = Path(filename).suffix.lower()
            indicador_path = safe_path_segment(item.indicador_id)
            evidence_id = str(uuid.uuid4())

            object_path = (
                f"evidencias/{uid}/{evaluation_ref.id}/"
                f"{indicador_path}/{evidence_id}{extension}"
            )

            blob = bucket.blob(object_path)
            blob.metadata = {
                "ownerUid": uid,
                "evaluationId": evaluation_ref.id,
                "indicatorId": item.indicador_id,
                "originalFilename": filename,
            }

            # Registrar antes do upload permite tentar limpar
            # o objeto caso a operação falhe parcialmente.
            uploaded_paths.append(object_path)

            # O arquivo permanece no Firebase Storage após a requisição.
            blob.upload_from_string(content, content_type=mime)

            evidence_documents.append({
                "id": evidence_id,
                "upload_id": item.upload_id,
                "indicador_id": item.indicador_id,
                "nome": filename,
                "caminho_storage": object_path,
                "content_type": mime,
                "tamanho_bytes": len(content),
                "criado_em": now,
            })

        # Registra os metadados após concluir todos os uploads.
        evaluation_ref.update({"evidencias": evidence_documents})

        logger.info(
            "Avaliação %s criada para o usuário %s. Evidências: %s",
            evaluation_ref.id,
            uid,
            len(evidence_documents),
        )

        return {
            "id": evaluation_ref.id,
            "evidencias": evidence_documents,
        }

    except HTTPException:
        cleanup_partial_evaluation(evaluation_ref, uploaded_paths)
        raise

    except Exception as exc:
        cleanup_partial_evaluation(evaluation_ref, uploaded_paths)
        logger.exception("Erro ao salvar avaliação e evidências.")

        raise HTTPException(
            status_code=500,
            detail="Não foi possível salvar a avaliação e suas evidências.",
        ) from exc

    finally:
        for upload in files:
            try:
                await upload.close()
            except Exception:
                logger.warning("Não foi possível fechar um arquivo recebido.")


# ============================================================
# LISTAGEM DE EVIDÊNCIAS
# ============================================================

@app.get("/avaliacoes/{evaluation_id}/evidencias")
def list_evidence(
    evaluation_id: str,
    user: dict = Depends(require_user),
):
    uid = get_user_id(user)
    _, dados = get_owned_evaluation(evaluation_id, uid)

    return {"evidencias": dados.get("evidencias", [])}


# ============================================================
# URL TEMPORÁRIA DE ACESSO
# ============================================================

@app.get("/avaliacoes/{evaluation_id}/evidencias/{evidence_id}/url")
def get_evidence_url(
    evaluation_id: str,
    evidence_id: str,
    user: dict = Depends(require_user),
):
    uid = get_user_id(user)
    _, dados = get_owned_evaluation(evaluation_id, uid)

    evidencia = next(
        (
            item
            for item in dados.get("evidencias", [])
            if item.get("id") == evidence_id
        ),
        None,
    )

    if not evidencia:
        raise HTTPException(
            status_code=404,
            detail="Evidência não encontrada.",
        )

    storage_path = evidencia.get("caminho_storage")

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
            detail="Não foi possível gerar o link temporário da evidência.",
        ) from exc


# ============================================================
# EXCLUSÃO DE EVIDÊNCIA
# ============================================================

@app.delete("/avaliacoes/{evaluation_id}/evidencias/{evidence_id}")
def delete_evidence(
    evaluation_id: str,
    evidence_id: str,
    user: dict = Depends(require_user),
):
    uid = get_user_id(user)
    evaluation_ref, dados = get_owned_evaluation(evaluation_id, uid)

    evidence_list = dados.get("evidencias", [])

    evidencia = next(
        (
            item
            for item in evidence_list
            if item.get("id") == evidence_id
        ),
        None,
    )

    if not evidencia:
        raise HTTPException(
            status_code=404,
            detail="Evidência não encontrada.",
        )

    storage_path = evidencia.get("caminho_storage")

    if not storage_path:
        raise HTTPException(
            status_code=500,
            detail="O caminho da evidência não está cadastrado.",
        )

    try:
        bucket.blob(storage_path).delete()

        evaluation_ref.update({
            "evidencias": [
                item
                for item in evidence_list
                if item.get("id") != evidence_id
            ]
        })

        logger.info(
            "Evidência %s removida da avaliação %s.",
            evidence_id,
            evaluation_id,
        )

        return {"ok": True}

    except Exception as exc:
        logger.exception("Erro ao excluir evidência %s.", evidence_id)

        raise HTTPException(
            status_code=500,
            detail="Não foi possível excluir a evidência.",
        ) from exc