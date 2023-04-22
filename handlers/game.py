import datetime

import aiogram
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from constants.game import GameConstants

import sqlite3

from database.core import async_sessionmaker, AsyncSession
from database import UserModel, get_user_by_id, insert_user, update_user_data#, DB_NAME
from lexicon.general import Lexicon, Commands # LEXICON_EN

import random

from utils.common.general import colorstr, infoColorstr
from typing import Optional

router: Router = Router()


def get_random_number() -> int:
    return random.randint(1, 100)


# @router.message(Command(commands=['cancel']))
# async def process_cancel_command(message: Message) -> None:
#     user_id: int = message.from_user.id
#     # create connection
#     # connection = sqlite3.connect(DB_NAME)
#     # cursor = connection.cursor()
#
#     user: Optional[UserModel] = get_user_by_id(user_id, cursor=cursor)
#     if user is None:
#         await message.answer(Lexicon.get_response(Commands.NO_GAME_YET))
#     else:
#         if user.in_game is True:
#             await message.answer(Lexicon.get_response(Commands.GAME_CANCELLED))  # LEXICON_EN['game_cancelled'])
#             user.in_game = False
#         else:
#             await message.answer(Lexicon.get_response(Commands.ALREADY_IN_GAME))  # LEXICON_EN['already_in_game'])
#     cursor.close()
#     connection.close()


@router.message(Command(commands=['cancel']))
async def process_cancel_command(message: Message, session: AsyncSession) -> None:
    user_id: int = message.from_user.id

    user = await get_user_by_id(user_id, session)
    if not user:
        await message.answer(Lexicon.get_response(Commands.NO_GAME_YET))
    else:
        if user.in_game:
            await message.answer(Lexicon.get_response(Commands.GAME_CANCELLED))
            user.in_game = False
        else:
            await message.answer(Lexicon.get_response(Commands.ALREADY_IN_GAME))

    await session.commit()


# @router.message(aiogram.filters.Text(text=['yes', 'go', "begin",
#                                            "start", "Да", "Сыграть", "Игра"], ignore_case=True))
# async def process_positive_answer(message: Message) -> None:
#     user_id: int = message.from_user.id
#     # create connection
#     connection = sqlite3.connect(DB_NAME)
#     cursor = connection.cursor()
#
#     user: Optional[UserModel] = get_user_by_id(user_id, cursor=cursor)
#     if user is None:
#         await message.answer(Lexicon.get_response(Commands.NO_GAME_YET)) #  LEXICON_EN['no_game_yet'])
#     else:
#         if user.in_game is False:
#             await message.answer(f"I guessed the number from 1 to 100")
#             user.in_game = True
#             user.secret_number = get_random_number()
#             user.attempts = GameConstants.attempts
#             update_user_data(user, connection=connection)
#         else:
#             await message.answer(Lexicon.get_response(Commands.ALREADY_IN_GAME)) # LEXICON_EN['already_in_game'])
#     cursor.close()
#     connection.close()


@router.message(aiogram.filters.Text(text=['yes', 'go', "begin",
                                           "start", "Да", "Сыграть", "Игра"], ignore_case=True))
async def process_positive_answer(message: Message) -> None:
    user_id: int = message.from_user.id

    async with async_sessionmaker() as session:
        user: Optional[UserModel] = await get_user_by_id(user_id, session=session)
        if user is None:
            await message.answer(Lexicon.get_response(Commands.NO_GAME_YET)) #  LEXICON_EN['no_game_yet'])
        else:
            if user.in_game is False:
                await message.answer(f"I guessed the number from 1 to 100")
                user.in_game = True
                user.secret_number = get_random_number()
                user.attempts = GameConstants.attempts
                user.last_activity_dt = datetime.datetime.now()

                await update_user_data(user, session=session)
            else:
                await message.answer(Lexicon.get_response(Commands.ALREADY_IN_GAME))


@router.message(aiogram.filters.Text(text=['No', 'Нет', 'Не', 'Не хочу', 'Не буду'], ignore_case=True))
async def process_negative_answer(message: Message):
    user_id: int = message.from_user.id

    async with async_sessionmaker() as session:
        user: Optional[UserModel] = await get_user_by_id(user_id, session=session)

        if user is None:
            await message.answer(Lexicon.get_response(Commands.NO_GAME_YET))
        else:
            if not user.in_game:
                await message.answer(f"=(")
            else:
                await message.answer(f"type the number from 1 to 100")


@router.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def process_numbers_answer(message: Message):
    user_id: int = message.from_user.id

    async with async_sessionmaker() as session:
        user: Optional[UserModel] = await get_user_by_id(user_id, session=session)

        if user is None:
            await message.answer(Lexicon.get_response(Commands.NO_GAME_YET))
        else:
            if user.in_game:
                if int(message.text) == user.secret_number:
                    await message.answer(f"You guessed the number! Let's try again?")

                    user.in_game = False
                    user.attempts = None
                    user.secret_number = None
                    user.total_games += 1
                    user.wins += 1

                elif int(message.text) > user.secret_number:
                    await message.answer('should be less')
                    user.attempts -= 1
                elif int(message.text) < user.secret_number:
                    await message.answer(f"should be greater")
                    user.attempts -= 1

                if user.attempts == 0:
                    await message.answer((f"you haven't guessed the number unfortunately..."
                                          f"it was {user.secret_number}"))
                    user.in_game = False
                    user.total_games += 1

                await update_user_data(user, session)
                print(infoColorstr(f"user with id={user_id} was updated in database"))

            else:
                await message.answer(Lexicon.get_response(Commands.NO_GAME_YET))
