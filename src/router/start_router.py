from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.formatting import Bold, Text, as_section, as_line
from database.dao import set_user
start_router = Router()


class StartSG(StatesGroup):
    main = State()
    createAvatar = State()

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

    ##message.from_user.full_name
    await message.answer(**content.as_kwargs())
    

@start_router.message(F.text == 'Поиск команды')
async def find_command(message: Message):
    find_command_kb = [
        [InlineKeyboardButton(text="📝Создать заявку", callback_data='create_request')],
       [InlineKeyboardButton(text="Мои заявки" , callback_data='my_requests')],
       [InlineKeyboardButton(text="Заявки", callback_data='all_request')]
    ]
    print(find_command_kb)
    rm = InlineKeyboardMarkup(inline_keyboard=find_command_kb)
    await message.answer('Поиск команды',  reply_markup=rm)