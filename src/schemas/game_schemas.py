from pydantic import BaseModel, ConfigDict

class WordForGame(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str | None
    body: str | None
    translate: str | None
