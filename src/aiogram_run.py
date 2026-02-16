import asyncio
from create_bot import bot, dp, admins
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats, BotCommandScopeAllGroupChats, BotCommandScopeUnion
from aiogram.fsm.scene import SceneRegistry
from database.base import create_tables
from database.dao import init_data
from router.start_router import start_router
from router.create_request_router import create_request_router

async def set_commands():
    private_commands = [BotCommand(command='start', description='Старт')]
    commands = [BotCommand(command='start', description='Старт')]
    await bot.set_my_commands(private_commands, BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(commands, BotCommandScopeAllGroupChats())


async def start_bot():
    await set_commands()
    await create_tables()
    await init_data()
    for admin_id in admins:
        try:
            await bot.send_message(admin_id, f'Я запущен🥳.')
        except:
            pass


# Функция, которая выполнится когда бот завершит свою работу
async def stop_bot():
    try:
        for admin_id in admins:
            await bot.send_message(admin_id, 'Бот остановлен. За что?😔')
    except:
        pass



async def main():
    # регистрация роутеров
    dp.include_router(start_router)
    dp.include_router(create_request_router)
    # регистрация функций
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)


    # запуск бота в режиме long polling при запуске бот очищает все обновления, которые были за его моменты бездействия
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())


