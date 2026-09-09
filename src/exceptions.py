
class DictionaryExceptionsBase(Exception):
    pass

class GameExceptionBase(Exception):
    pass

class WordIsAlreadyExist(DictionaryExceptionsBase):
    def __init__(self, word:str):
        super().__init__(f"Слово {word} уже в словаре!")

class WordIsNotExists(DictionaryExceptionsBase):
    def __init__(self, word:str):
        super().__init__(f"Слово {word} не найдено!")

class LLMRequestsLimit(DictionaryExceptionsBase):
    def __init__(self,llm_request_limit:int,  llm_ttl: int):
        super().__init__(f"Превышен лимит запросов в нейросеть, не более {llm_request_limit} в {llm_ttl} секунд")

class AllWordsPassed(GameExceptionBase):
    def __init__(self):
        super().__init__(f"Все слова пройдены!")

class HashIsAlreadyExists(GameExceptionBase):
    def __init__(self):
        super().__init__(f"Hash уже существует")