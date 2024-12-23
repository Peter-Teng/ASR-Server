from pydantic import BaseModel


class Audio(BaseModel):
    path: str