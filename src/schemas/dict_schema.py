from typing import List, Tuple
from pydantic import BaseModel, ConfigDict

class WordSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    body: str
    user_id: str | None
    translate: str | None
    examples: list[dict[str, str]] | None

class WordCreate(BaseModel):
    # id: str
    body: str
    user_id: str | None
    translate: str | None
    examples: list[dict[str, str]] | None

class WordDelete(BaseModel):
    body: str
    user_id: str

class WordGet(BaseModel):
    body: str
    user_id: str