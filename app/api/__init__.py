"""API HTTP do Evalytics.

O objeto ``app`` continua exposto em ``app.api`` para manter compatibilidade
com comandos ASGI como ``uvicorn app.api:app``.
"""

from fastapi import FastAPI

from .routes.evaluations import router as evaluations_router
from .routes.evidence import router as evidence_router
from .config import (
    MAX_FILE_SIZE,
    MAX_FILES_PER_EVALUATION,
    MAX_FILES_PER_INDICATOR,
    bucket,
    db,
    logger,
)

app = FastAPI(
    title="Evalytics Evidence API",
    version="1.2.0",
    description=(
        "API para avaliações institucionais e gerenciamento "
        "de evidências do Evalytics."
    ),
)

app.include_router(evaluations_router)
app.include_router(evidence_router)

# Mantém disponíveis em ``app.api`` nomes usados por integrações existentes.
from .auth import get_user_id, require_user  # noqa: E402
from .dependencies import cleanup_partial_evaluation, get_owned_evaluation  # noqa: E402
from .routes.evaluations import create_evaluation, health, list_evaluations  # noqa: E402
from .routes.evidence import delete_evidence, get_evidence_url, list_evidence  # noqa: E402
from .schemas import EvaluationPayload, EvidenceManifestItem  # noqa: E402
from .validation import safe_filename, safe_path_segment, validate_file, validate_manifest  # noqa: E402

__all__ = [
    "MAX_FILE_SIZE",
    "MAX_FILES_PER_EVALUATION",
    "MAX_FILES_PER_INDICATOR",
    "app",
    "bucket",
    "create_evaluation",
    "delete_evidence",
    "db",
    "EvaluationPayload",
    "EvidenceManifestItem",
    "get_evidence_url",
    "get_owned_evaluation",
    "get_user_id",
    "health",
    "list_evaluations",
    "list_evidence",
    "logger",
    "require_user",
    "safe_filename",
    "safe_path_segment",
    "validate_file",
    "validate_manifest",
]
