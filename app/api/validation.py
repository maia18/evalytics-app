"""Validação e sanitização de arquivos e manifestos de evidências."""

import re
from pathlib import Path

from fastapi import HTTPException, UploadFile

from .config import (
    MAX_FILE_SIZE,
    MAX_FILES_PER_EVALUATION,
    MAX_FILES_PER_INDICATOR,
)
from .schemas import EvidenceManifestItem

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
        raise HTTPException(status_code=400, detail=f"O arquivo {nome} está vazio.")
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
        if quantidade_por_indicador[indicador_id] > MAX_FILES_PER_INDICATOR:
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
