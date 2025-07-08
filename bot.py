from handlers import router

from aiogram import Bot, Dispatcher,types # библиотека Телеграм
from aiogram.fsm.storage.memory import MemoryStorage

from decouple import Config, RepositoryEnv
ENV_FILE = 'e.env'
config = Config(RepositoryEnv(ENV_FILE))

async def main():

 bot = Bot(token=config('TOKEN'))

 commands = [
        types.BotCommand(command='/start', description='Начать взаимодействие с ботом'),
        types.BotCommand(command='/create', description='Запись данных'),
        types.BotCommand(command='/read', description='Чтение данных'),
    ]
 await bot.set_my_commands(commands)

 dp = Dispatcher(storage=MemoryStorage()) # объект обработки сообщений

 #основной процесс
 dp.include_router(router)
 await bot.delete_webhook(drop_pending_updates=True)
 await dp.start_polling(bot)
