
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import aiohttp

from decouple import Config, RepositoryEnv
ENV_FILE = 'e.env'
params = ''
config = Config(RepositoryEnv(ENV_FILE))

# Router-отдельный объект, не нужна сеть
router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
"Запуск сообщения по команде /start. \n Commands: /create <IMYA> <FAMILIA> \n /read <ID> \n /update <ID> <IMYA> <FAMILIA>"
)

@router.message(Command('create'))
async def cmd_create(message: Message):
    words, params = message.text.split(" "), ""
    if (len(words)>1): params={"name": words[1], "surname": None}
    if (len(words)>2): params={"name": words[1], "surname": words[2]}

    async with aiohttp.ClientSession() as session:
        async with session.post(config('API_ADDR'),params) as response:
            await message.answer(await response.json())

@router.message(F.text == 'read')#F - более гибкая
async def cmd_read(message: Message):
    words, params = message.text.split(" "), ""

    async with aiohttp.ClientSession() as session:
        async with session.get(config('API_ADDR')+'/'+words[1]) as response:
            await message.answer(await response.json())

@router.message(F.text == 'update')#F - более гибкая
async def cmd_update(message: Message):
    words, params = message.text.split(" "), ""
    if (len(words)>1): params={"name": words[1], "surname": None}
    if (len(words)>2): params={"name": words[1], "surname": words[2]}

    async with aiohttp.ClientSession() as session:
        async with session.put(config('API_ADDR'), params) as response:
            await message.answer(await response.json())

