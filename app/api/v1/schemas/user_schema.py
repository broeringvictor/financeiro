from pydantic import BaseModel, EmailStr


class CreateUserRequest(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    password_confirmation: str


class CreateUserResponse(BaseModel):
    user_id: str
    name: str
    email: str
