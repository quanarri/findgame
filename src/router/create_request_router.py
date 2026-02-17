from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton,  InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData
from database.dao import add_request, get_games, get_regions
from uuid import UUID as PythonUUID
from create_bot import bot

create_request_router = Router()


class RequestCallback(CallbackData, prefix="request"):
    action: str
    id: PythonUUID
    
class AddRequestStates(StatesGroup):
    region = State() 
    game = State() 
    game_id = State()
    top = State()
    position = State()

@create_request_router.callback_query(F.data.startswith('create_request'))
async def start_note(callback_query: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback_query.answer() 
    


    kb_list = [
        [KeyboardButton(text="❌ Отмена заявки")]]
    cancel_keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=False)

    user_id = callback_query.from_user.id
    await bot.send_message(user_id, "Вы попали в меню заявки", reply_markup=cancel_keyboard)

    regions = await get_regions()
    region_kb = []
    for region in regions:
        region_kb.append([InlineKeyboardButton(text=region["name"], 
                                               callback_data=RequestCallback(id=region["id"], action="region").pack()
                                               )])

    await bot.send_message(user_id, 'Регион',
                         reply_markup=InlineKeyboardMarkup(inline_keyboard=region_kb))
    await state.set_state(AddRequestStates.region)

@create_request_router.callback_query(RequestCallback.filter(F.action == "region"))
async def region_callback(callback_query: CallbackQuery, callback_data: RequestCallback, state: FSMContext):
    await callback_query.answer()

    region_id = callback_data.id
    await state.update_data({
        "region": region_id,
    })

    user_id = callback_query.from_user.id
    games = await get_games()
    region_kb = []
    for game in games:
        region_kb.append([InlineKeyboardButton(text=game["name"], 
                                               callback_data=RequestCallback(id=game["id"], action="game").pack()
                                               )])

    await bot.send_message(user_id, 'Регион',
                         reply_markup=InlineKeyboardMarkup(inline_keyboard=region_kb))
    await state.set_state(AddRequestStates.game)

@create_request_router.callback_query(RequestCallback.filter(F.action == "game"))
async def game_callback(callback_query: CallbackQuery, callback_data: RequestCallback, state: FSMContext):
    await callback_query.answer()

    game_id = callback_data.id
    await state.update_data({
        "game": game_id,

    })

    user_id = callback_query.from_user.id
    await bot.send_message(user_id, 'Введите id в игре')
    await state.set_state(AddRequestStates.game_id)


@create_request_router.message(AddRequestStates.game_id)
async def cancel_add_note(message: Message, state: FSMContext):
    game_id = message.text
    await state.update_data({
        "gameid": game_id,
    })
    await message.answer('Введите топ в игре!')
    await state.set_state(AddRequestStates.top)


@create_request_router.message(AddRequestStates.top)
async def cancel_add_note(message: Message, state: FSMContext):
    top = message.text
    await state.update_data({
        "top": top,
    })
    await message.answer('Введите позицию в игре!')
    await state.set_state(AddRequestStates.position)


@create_request_router.message(AddRequestStates.position)
async def cancel_add_note(message: Message, state: FSMContext):
    position = message.text
    await state.update_data({
        "position": position,
    })

    data = await state.get_data()
  
    await add_request(user_id=message.from_user.id, region=data.get('region'),
                   game=data.get('game'),  gameid=data.get('gameid'),  top=data.get('top'),  position=data.get('position'))
    start_kb = [
        [KeyboardButton(text="Моя анкета")],
        [KeyboardButton(text="Поиск команды")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=start_kb, resize_keyboard=True, one_time_keyboard=False)
    await message.answer('Заявка успешно добавлена!', reply_markup=keyboard)
    await state.clear()
