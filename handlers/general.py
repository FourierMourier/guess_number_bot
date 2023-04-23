import datetime

import aiogram
import asyncio
import sqlite3

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram import F, filters
from aiogram.filters import Command
from aiogram.types import Message, ContentType, CallbackQuery, InlineQuery

from lexicon.general import Lexicon, Commands # LEXICON_EN

import sqlalchemy
from database.core import async_sessionmaker, AsyncSession
from database import UserModel, get_user_by_id, insert_user, update_user_data, DB_NAME, add_new_user
from database.core import UserTable

# additional ones:
from keyboards.basic.language import LANG_MSG_START, InlineLanguageKeyboard # get_keyboard # LanguageKeyboard

from typing import Optional


router: Router = Router()


# @router.message(Command(commands=['start']))
# async def process_start_command(message: Message) -> None:
#     user_id: int = message.from_user.id
#     connection = sqlite3.connect(DB_NAME)
#     cursor = connection.cursor()
#
#     user: Optional[UserModel] = get_user_by_id(user_id, cursor=cursor)
#     if user is None:
#         user = UserModel(id=user_id,
#                          in_game=False,
#                          secret_number=None,
#                          attempts=None,
#                          total_games=0,
#                          wins=0,
#                          )
#
#         insert_user(user, connection=connection)
#         print(f"user with id = {user_id} was inserted: {user}")
#
#     await message.answer(Lexicon.get_response(Commands.START))
#
#     cursor.close()
#     connection.close()
#

@router.message(Command(commands=['start']))
async def process_start_command(message: Message) -> None:
    user_id: int = message.from_user.id

    async with async_sessionmaker() as session:
        user: Optional[UserModel] = await get_user_by_id(user_id, session=session)

        lang: Optional[str] = None
        curr_dt = datetime.datetime.now()
        if user is None:
            await add_new_user(user_id, curr_dt, session)
            print(f"user with id = {user_id} was inserted: {user}")

        else:
            lang = user.lang

        await message.answer(Lexicon.get_response(Commands.START, lang))


@router.message(Command(commands=['help']))
async def process_help_command(message: Message) -> None:

    lang: Optional[str] = None
    user_id: int = message.from_user.id
    async with async_sessionmaker() as session:
        user: Optional[UserModel] = await get_user_by_id(user_id, session=session)

        lang = user.lang

    await message.answer(Lexicon.get_response(Commands.HELP, lang))


# @router.message(Command(commands=['stats']))
# async def process_stat_command(message: Message) -> None:
#     user_id: int = message.from_user.id
#     # create connection
#     connection = sqlite3.connect(DB_NAME)
#     cursor = connection.cursor()
#
#     user: Optional[UserModel] = get_user_by_id(user_id, cursor=cursor)
#     if user is None:
#         await message.answer(Lexicon.get_response(Commands.NO_GAME_YET))
#     else:
#         await message.answer(Lexicon.get_response(Commands.STATS).format(user.total_games, user.wins, user.attempts))
#
#     cursor.close()
#     connection.close()
#

@router.message(Command(commands=['lang']))
async def process_lang_command(message: Message) -> None:
    user_id: int = message.from_user.id
    # TODO: consider
    #       keyboard = await get_inline_keyboard()

    # async with async_sessionmaker() as session:
    #     user: Optional[UserModel] = await get_user_by_id(user_id, session=session)
    #     pass
    # now show keyboard
    await message.answer(f"Set the language (debug): ", reply_markup=InlineLanguageKeyboard)


@router.callback_query(lambda c: c.data.startswith(LANG_MSG_START))
async def process_callback_language(callback_query: CallbackQuery):#, state: FSMContext):
    # CallbackQuery.data.
    # language = callback_query.data.split("_")[1]
    language = callback_query.data.split(LANG_MSG_START)[-1]
    if language in Lexicon.supported_languages:
        # Update the user's language preference in the database
        user_id = callback_query.from_user.id
        async with async_sessionmaker() as session:
            user = await get_user_by_id(user_id, session=session)
            user.lang = language
            await update_user_data(user, session)
            # commit is inside update func
            # await session.commit()
        # Send a confirmation message to the user
        await callback_query.answer(f"Language was set to {language}")
    else:
        await callback_query.answer("Unsupported language selected")


@router.message(Command(commands=['stats']))
async def process_stats_command(message: Message) -> None:
    user_id: int = message.from_user.id

    async with async_sessionmaker() as session:
        user: Optional[UserModel] = await get_user_by_id(user_id, session=session)
        if user is None:
            await message.answer(Lexicon.get_response(Commands.NO_GAME_YET))
        else:
            await message.answer(Lexicon.get_response(Commands.STATS, user.lang).format(user.total_games, user.wins, user.attempts))


# @router.message()
# async def process_other_text_answers(message: Message):
#     user_id: int = message.from_user.id
#     # create connection
#     connection = sqlite3.connect(DB_NAME)
#     cursor = connection.cursor()
#
#     user: Optional[UserModel] = get_user_by_id(user_id, cursor=cursor)
#     if user is None:
#         await message.answer(Lexicon.get_response(Commands.NO_GAME_YET))
#     else:
#         if user.in_game:
#             await message.answer(Lexicon.get_response(Commands.GAME_IN_PROGRESS))
#         else:
#             await message.answer(Lexicon.get_response(Commands.START))
#
#     cursor.close()
#     connection.close()


@router.message()
async def process_other_text_answers(message: Message):
    user_id: int = message.from_user.id

    async with async_sessionmaker() as session:
        user: Optional[UserModel] = await get_user_by_id(user_id, session=session)

        if user is None:
            await message.answer(Lexicon.get_response(Commands.NO_GAME_YET))
        else:
            if user.in_game:
                await message.answer(Lexicon.get_response(Commands.GAME_IN_PROGRESS, user.lang))
            else:
                await message.answer(Lexicon.get_response(Commands.START, user.lang))

    return
