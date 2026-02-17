from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.formatting import Bold, Text, as_section, as_line
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters.callback_data import CallbackData
from create_bot import bot

from database.dao import get_all_requests, get_my_requests, set_user
start_router = Router()


class StartSG(StatesGroup):
    main = State()
    createAvatar = State()
@start_router.message(F.text == '❌ Отмена заявки')
@start_router.message(CommandStart())
async def cmd_private_start(message: Message, state: FSMContext):
    await state.clear()
    user = await set_user(tg_id=message.from_user.id)
    msg = "Привет"
    start_kb = [
        [KeyboardButton(text="Моя анкета")],
        [KeyboardButton(text="Поиск команды")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=start_kb, resize_keyboard=True, one_time_keyboard=False)
    await message.answer(msg,  reply_markup=keyboard)

@start_router.message(F.text == 'Моя анкета')
async def cmd_start(message: Message):
    content = Text(
        as_section(
            Bold("моя анкета"),
            as_line(Bold("ID"), message.from_user.id, sep=": "),
            as_line(Bold("Имя"), message.from_user.full_name, sep=": ")
        )
    )


    await message.answer(**content.as_kwargs())
    

class AdminAction(CallbackData, prefix="adm"):
    action: str

@start_router.message(F.text == 'Поиск команды')
async def find_command(message: Message):
    find_command_kb = [
        [InlineKeyboardButton(text="📝Создать заявку", callback_data="create_request")],
       [InlineKeyboardButton(text="Мои заявки", callback_data="my_requests")],
       [InlineKeyboardButton(text="Заявки", callback_data="all_requests")]
    ]
    rm = InlineKeyboardMarkup(inline_keyboard=find_command_kb)
    await message.answer('Поиск команды',  reply_markup=rm)


@start_router.callback_query(F.data.in_({"my_requests"}))
async def find_command(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    
    requests = await get_my_requests(tg_id=callback_query.from_user.id)
    user_id = callback_query.from_user.id
    caption = "Мои заявки\n"
    for request in requests:
        caption += "`" + str(request['user_id']) + "`, " + request["region_name"] +  ", " + request['game_name'] + ", " + request['gameid'] + ", " + request["top"] + ", " + request["position"] + " \n"
    await bot.send_message(user_id, caption, parse_mode=ParseMode.MARKDOWN_V2)


@start_router.callback_query(F.data.in_({"all_requests"}))
async def find_command(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    user_id = callback_query.from_user.id
    requests = await get_all_requests(user_id)

    caption = "Заявки\n"
    for request in requests:
        caption += "`" + str(request['user_id']) + "`, " + request["region_name"] +  ", " + request['game_name'] + ", " + request['gameid'] + ", " + request["top"] + ", " + request["position"] + " \n"
  
    await bot.send_message(user_id, caption)