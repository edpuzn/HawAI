from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class MessageCreate(BaseModel):
    thread_id: str
    content: str
    images: List[str] = []  # dataURL veya URL


class MessageDB(BaseModel):
    id: Optional[str]
    thread_id: str
    user_id: str
    role: str  # user | assistant
    content: str
    images: List[str] = []
    edited: bool = False
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()


