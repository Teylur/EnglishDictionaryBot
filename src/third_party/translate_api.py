from googletrans import Translator

async def get_translated_text(text: str) -> str:
    translator = Translator()
    result = await translator.translate(text=text, dest="ru")
    return result.text