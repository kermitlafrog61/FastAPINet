from typing import Optional

from pydantic import BaseModel


class PostCreate(BaseModel):
    title: str
    content: str


class PostUpdate(BaseModel):
    title: str = None
    content: str = None


class PostDetail(BaseModel):
    id: int
    title: str
    content: str

    class Config:
        from_attributes = True
