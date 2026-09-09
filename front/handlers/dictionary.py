from aiogram import Router
from aiogram.types import Message, CallbackQuery
import httpx
from httpx import AsyncClient
from front.states.states import GameMode, Dictionary, WordDelete
from aiogram.fsm.context import FSMContext
from aiogram import F
from front.keyboards.dict_keyboards import (get_accept_reject_inline_keyboard, get_dict_main_Readline_keyboard, 
                                            get_dict_delete_word_keyboard, get_dict_back_button)

router = Router()

#word list
@router.message(Dictionary.word, F.text=="Список слов")
async def word_list(message: Message):
    user_id = str(message.from_user.id)
    async with AsyncClient() as client:
        r: httpx.Response = await client.get(url=f'http://127.0.0.1:8000/dict/{user_id}')
    response = "Dictionary:\n"
    for word in r.json():
        response += word["body"] + " - " + word["translate"] +"\n"
    await message.answer(text=response, reply_markup=get_dict_delete_word_keyboard())

#main state
@router.message(Dictionary.word, F.text)
async def dictionary(message: Message, state: FSMContext):
    
    current_state = await state.get_state()
    if current_state == GameMode.waiting_for_answer:
        return
    
    word = message.text
    user_id = str(message.from_user.id)
    async with AsyncClient() as client:
        r: httpx.Response = await client.get(url=f'http://127.0.0.1:8000/dict/{user_id}/{word}', timeout=30)
    if r.is_error:
        text = r.text + "\nПожалуйста повторите запрос позже:)"
        await message.answer(text=text)
    temp = r.json()
    translate = temp["translate"]
    examples = temp["examples"]
    response = f"Слово: {word}\nПеревод: {translate}\nПримеры:\n"
    for ex in examples:
        response += ex["en"] + " " + ex["ru"] + "\n"

    await state.update_data(word=message.text, translate=translate, examples=examples)
    await message.answer(response, reply_markup=get_accept_reject_inline_keyboard())

#word delete
@router.message(WordDelete.word_to_delete, F.text)
async def word_delete(message: Message, state: FSMContext):
    word_to_delete: str = message.text.lower()
    print(word_to_delete)
    # word_to_delete = word_to_delete["word_to_delete"]
    user_id = str(message.from_user.id)
    print(user_id)
    async with AsyncClient() as client:
        r: httpx.Response = await client.delete(f'http://127.0.0.1:8000/dict/{user_id}/{word_to_delete}')
    if r.is_error:
        await message.answer(text=f"Слово {word_to_delete} не найдено! \nПроверьте корректность написания.", reply_markup=get_dict_back_button())
    else:
        await message.answer(text=f"Слово {word_to_delete} успешно удалено!", reply_markup=get_dict_back_button())

# word_accept callback create
@router.message(Dictionary.word)
@router.callback_query(lambda c: c.data == "word_accept")
async def word_accepted(callback: CallbackQuery, state: FSMContext):
    word = await state.get_data()
    print(word, callback.from_user.id)
    word_body: str = word["word"].lower()
    async with AsyncClient() as client:
        r: httpx.Response = await client.post('http://127.0.0.1:8000/dict', json={'body': word_body, 'user_id': str(callback.from_user.id), 
                                                                                  'translate': word["translate"], 'examples': word["examples"]})
    #errors
    if r.is_success:
        await callback.message.edit_text(word_body + " было добавлено в словарь! ✔",)
    elif r.is_client_error:
        await callback.message.edit_text(word_body + " уже есть в словаре",)
    else:
        await callback.message.edit_text(word_body + " не удалось добавить в словарь",)


#back callback
@router.message(WordDelete.word_to_delete)
@router.callback_query(lambda c: c.data == "back")
async def back(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer("Введите слово для перевода")
    await state.set_state(Dictionary.word)

# word_reject callback
@router.message(Dictionary.word)
@router.callback_query(lambda c: c.data == "word_reject")
async def word_reject(callback: CallbackQuery, state: FSMContext):
    word = await state.get_data()
    word = word["word"]
    await state.clear()
    await callback.message.edit_text(f"Слово {word} не добавлено в словарь! ❌", reply_markup=None)
    await state.set_state(Dictionary.word)

# word_delete callback
@router.message(Dictionary.word)
@router.callback_query(lambda c: c.data == "word_delete")
async def word_delete(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Введите слово которое хотите удалить (на англиском)", reply_markup=get_dict_back_button())
    await state.clear()
    await state.set_state(WordDelete.word_to_delete)







