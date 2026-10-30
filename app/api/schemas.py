"""Modelos de entrada e validação dos payloads da API."""

from typing import Any

from pydantic import BaseModel, Field


class EvidenceManifestItem(BaseModel):
    upload_id: str = Field(min_length=1, max_length=80)
    indicador_id: str = Field(min_length=1, max_length=200)
    filename: str = Field(min_length=1, max_length=255)


class EvaluationPayload(BaseModel):
    curso_id: str = Field(min_length=1, max_length=200)
    curso_nome: str = Field(min_length=1, max_length=300)
    respostas: dict[str, Any]
    justificativas: dict[str, str] = Field(default_factory=dict)
