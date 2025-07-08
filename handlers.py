
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
"Запуск сообщения по команде /start. \n Commands: create <IMYA> <FAMILIA> \n read <ID> \n update <ID> <IMYA> <FAMILIA>"
)

@router.message(Command('create'))
async def cmd_create(message: Message):
    words = message.text.split(" ")
    if (len(words)>1): params='{"name": '+words[1]+', "surname": }'
    if (len(words)>2): params='{"name": '+words[1]+', "surname": '+words[2]+'}'
    session = aiohttp.ClientSession()
    response = session.post(config('API_ADDR'),params)
    data = await response.json()
    await message.answer(f"{data}")

@router.message(F.text == 'read')#F - более гибкая
async def cmd_read(message: Message):
    session = aiohttp.ClientSession()
    response = session.get(config('API_ADDR')+message.text.split(" ")[1])
    data = await response.json()
    await message.answer(f"{data}")

@router.message(F.text == 'update')#F - более гибкая
async def cmd_update(message: Message):
    words = message.text.split(" ")
    if (len(words)>1): params='{"name": '+words[1]+', "surname": }'
    if (len(words)>2): params='{"name": '+words[1]+', "surname": '+words[2]+'}'
    session = aiohttp.ClientSession()
    response = session.put(config('API_ADDR'), params)
    data = await response.json()
    await message.answer(f"{data}")
