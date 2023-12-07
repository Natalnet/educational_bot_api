from pydantic import BaseModel


class UserDtoInput(BaseModel):
    discord_id: str


class UserDtoOutput(BaseModel):
    id: str
    discord_id: str


class RegisterDtoInput(BaseModel):
    discord_id: str
    matricula: str
