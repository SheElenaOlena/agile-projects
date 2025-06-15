from pydantic import BaseModel, Field


class ResponseSchema(BaseModel):
    question_text: str = Field(...)
    is_agree: bool = Field(...)
    question_id: int = Field(...)
    id: int = Field(...)
    text: str | None = Field(default=None)
    user_id: int | None = Field(default=None)
    user_nickname: str | None = Field(default=None)


class ResponseCreate(BaseModel):
    question_id: int = Field(..., description="ID of the question the response belongs to")
    is_agree: bool = Field(...)
    text: str | None = Field(default=None)
    user_id: int | None = Field(default=None)


class ResponseUpdate(ResponseCreate):
    pass


class ResponseDelete(BaseModel):
    response_id: int = Field(...)

