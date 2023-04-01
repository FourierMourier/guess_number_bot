import aiogram
import asyncio
import sqlite3

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, ContentType

from lexicon.general import LEXICON_EN

from database import UserModel, get_user_by_id, insert_user, DB_NAME

from typing import Optional


router: Router = Router()


@router.message(Command(commands=['start']))
async def process_start_command(message: Message) -> None:
    user_id: int = message.from_user.id
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    user: Optional[UserModel] = get_user_by_id(user_id, cursor=cursor)
    if user is None:
        user = UserModel(id=user_id,
                         in_game=False,
                         secret_number=None,
                         attempts=None,
                         total_games=0,
                         wins=0,
                         )

        insert_user(user, connection=connection)
        print(f"user with id = {user_id} was inserted: {user}")

    await message.answer(LEXICON_EN['/start'])

    cursor.close()
    connection.close()


@router.message(Command(commands=['help']))
async def process_help_command(message: Message) -> None:
    await message.answer(LEXICON_EN['/help'])


@router.message(Command(commands=['stat']))
async def process_stat_command(message: Message) -> None:
    user_id: int = message.from_user.id
    # create connection
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    user: Optional[UserModel] = get_user_by_id(user_id, cursor=cursor)
    if user is None:
        await message.answer(f"We haven't played yet so statistics is empty. Shall we?")
    else:
        await message.answer((f"Games so far: {user.total_games}\n"
                              f"wins: {user.wins}\n"
                              f"attemps: {user.attempts}"))
    cursor.close()
    connection.close()


@router.message()
async def process_other_text_answers(message: Message):
    user_id: int = message.from_user.id
    # create connection
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    user: Optional[UserModel] = get_user_by_id(user_id, cursor=cursor)
    if user is None:
        await message.answer(LEXICON_EN['no_game_yet'])
    else:
        if user.in_game:
            await message.answer(f"We've already in game. Please send numbers from 1 to 100")
        else:
            await message.answer(f"Start the game")

    cursor.close()
    connection.close()
