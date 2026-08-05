from typing import List
from pydantic import BaseModel

class Word(BaseModel):
    id: str
    body: str
    # translate: str
    # examples: List[str]