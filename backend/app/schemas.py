from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class RegisterIn(BaseModel):
    email: EmailStr
    display_name: str = Field(min_length=2, max_length=80)
    password: str = Field(min_length=12, max_length=128)

    @field_validator("display_name")
    @classmethod
    def normalize_display_name(cls, value: str) -> str:
        value = value.strip()
        if len(value) < 2:
            raise ValueError("Display name must contain at least two non-space characters")
        return value


class LoginIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class UserOut(BaseModel):
    id: str
    email: EmailStr
    display_name: str
    role: str
    model_config = ConfigDict(from_attributes=True)


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LessonOut(BaseModel):
    id: int
    title: str
    duration_minutes: int
    position: int
    model_config = ConfigDict(from_attributes=True)


class CourseOut(BaseModel):
    id: int
    title: str
    slug: str
    summary: str
    difficulty: str
    duration_minutes: int
    category: str
    lessons: list[LessonOut]
