from pydantic import BaseModel


class Speaker(BaseModel):
    audioPath: str
    name: str