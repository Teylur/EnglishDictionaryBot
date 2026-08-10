
class DictionaryExceptionsBase(Exception):
    pass

class WordIsAlreadyExist(DictionaryExceptionsBase):
    def __init__(self, word:str):
        super().__init__(f"Слово {word} уже в словаре!")