from pydantic import BaseModel, EmailStr


class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str = "user"


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class TicketCreate(BaseModel):
    title: str
    description: str


class TicketUpdate(BaseModel):
    title: str
    description: str


class CommentCreate(BaseModel):
    comment: str


class AssignTicket(BaseModel):
    assigned_to: int


class StatusUpdate(BaseModel):
    status: str