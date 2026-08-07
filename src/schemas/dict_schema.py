from typing import Tuple
from pydantic import BaseModel, ConfigDict

class WordSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    body: str
    examples: Tuple[str] | None

class WordCreate(BaseModel):
    # id: str
    body: str
    # translate: str
    # examples: List[str]