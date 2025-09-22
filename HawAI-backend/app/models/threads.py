from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ThreadCreate(BaseModel):
    title: str


class ThreadDB(BaseModel):
    id: Optional[str]
    user_id: str
    title: str
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()


