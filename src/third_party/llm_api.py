import json
from ollama import AsyncClient
from src.config.config import settings

client = AsyncClient(
  host=settings.LOCAL_LLM_URL,
  headers={'x-some-header': 'some-value'}
)
async def get_examples_from_local_llm(word: str) -> dict[str, str]:
    message = [{
        "role": "user",
        "content": f'Переведи английское слово "{word}" на русский и приведи 3 примера предложений с ним с переводом. \
        Ответь строго в формате JSON: {{"translation": "...", "examples": [{{"en": "...", "ru": "..."}}]}}. Слово: {word}',
        "stream": False,
        "options": {"temperature": 0.2}
    }, ]
    response = await client.chat(model='qwen2.5:3b', messages=message)
    # print("ВЕСЬ response: " + response)
    print("RESPONSE MESSAGE CONTENT: " + response['message']['content'])
    json_respons = json.loads(response['message']['content'])
    return json_respons
