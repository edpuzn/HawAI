from __future__ import annotations
from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class ChatIn(BaseModel):
    message: str
    user_meta: Optional[Dict[str, object]] = Field(default_factory=dict)
    image_url: Optional[str] = None
    image_base64: Optional[str] = None


class Source(BaseModel):
    title: str
    url: str


class Safety(BaseModel):
    is_emergency: bool


class ChatOut(BaseModel):
    reply: str
    sdg_tags: List[str]
    sources: List[Source]
    safety: Safety
