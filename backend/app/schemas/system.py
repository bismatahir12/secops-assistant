import uuid
from datetime import datetime

from pydantic import BaseModel


class SystemCreate(BaseModel):
    name: str
    system_type: str = "generic"


class SystemRead(BaseModel):
    id: uuid.UUID
    name: str
    system_type: str
    created_at: datetime

    model_config = {"from_attributes": True}
