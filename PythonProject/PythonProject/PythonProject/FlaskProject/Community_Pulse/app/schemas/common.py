from pydantic import BaseModel, Field
from typing import Any


class MessageResponse(BaseModel):
    message: Any = Field(...)


class StatisticSchema(BaseModel):
    question_text: str = Field(...)
    agree_count: int = Field(...)
    disagree_count: int = Field(...)