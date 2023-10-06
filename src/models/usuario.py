from pydantic import BaseModel

class Usuario(BaseModel):
    discord_id: str