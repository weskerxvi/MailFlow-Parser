from datetime import datetime

from pydantic import BaseModel, ConfigDict

class OrderSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    number: int
    client: str
    value: float


class ProcessingRunSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    status: str
    total_read: int
    total_parsed: int
    created: int
    updated: int
    ignored: int
    failed: int
    error_message: str | None
    started_at: datetime
    finished_at: datetime | None
