from pydantic import BaseModel, Field, model_validator


class UserSchema(BaseModel):
    id: int = Field(...)
    nickname: str = Field(...)


class UserCreate(BaseModel):
    nickname: str = Field(...)
    password: str = Field(...)
    repeat_password: str = Field(...)

    # creating a function if passwords matching
    @model_validator(mode='after')
    def match_passwords(self):
        if self.password == self.repeat_password:
            return self
        else:
            raise ValueError("Passwords don't match.")


class UserUpdate(UserCreate):
    pass


class UserDelete(BaseModel):
    id: int = Field(...)