from pydantic import BaseModel, Field


class QuestionCreate(BaseModel):
    text: str = Field(..., description="Text of the question", max_length=140)
    user_id: int | None = Field(default=None)


class QuestionDelete(BaseModel):
    question_id: int = Field(...)


class QuestionUpdate(QuestionCreate):
    pass


class QuestionSchema(BaseModel):
    id: int
    text: str
    user_id: int | None = Field(default=None)
    user_nickname: str | None = Field(default=None)


