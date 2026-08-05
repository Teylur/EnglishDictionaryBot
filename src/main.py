from fastapi import FastAPI, status
from src.schemas.dict_schema import Word

app = FastAPI()

dict: list[Word] = []

@app.post("/dict", status_code=status.HTTP_201_CREATED)
def new_word(payload: Word) -> Word:
    dict.append(payload)
    return payload

@app.get("/dict")
def new_word() -> list[Word]:
    return dict
