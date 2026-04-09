from datetime import datetime
from typing import Optional

from pydantic import Field

from .base import BaseModel, WordStatus


class WordReviewPublic(BaseModel):
    """Schema de leitura de uma revisão, visível para o dono da palavra e para ADMINs."""

    id: int
    reviewer_id: int
    status: WordStatus
    comment: Optional[str]
    created_at: datetime

    model_config = {'from_attributes': True}


class WordReviewCreate(BaseModel):
    """
    Payload recebido pelo endpoint POST /words/{word_id}/reviews.

    Somente ADMINs têm acesso a esta operação.
    O `comment` é obrigatório quando o status exigir justificativa
    (REJECTED ou CHANGES_REQUESTED), e facultativo para APPROVED.
    """

    status: WordStatus = Field(
        description=(
            "Novo status que o ADMIN está atribuindo à palavra. "
            "Use APPROVED para aprovar, REJECTED para rejeitar definitivamente, "
            "ou CHANGES_REQUESTED para solicitar ajustes ao autor."
        )
    )
    comment: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Feedback textual do revisor sobre a palavra.",
    )
