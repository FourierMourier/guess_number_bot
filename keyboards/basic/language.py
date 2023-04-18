import random

from aiogram.types import (
    Message,
    # ordinary
    KeyboardButton, MenuButton, ReplyKeyboardMarkup, ReplyKeyboardRemove,
    # inline
    InlineKeyboardButton, InlineKeyboardMarkup,
)

from lexicon.general import Lexicon

from typing import List, Optional, Any

LANG_MSG_START: str = f'_{str(random.randint(0, 10000 - 1)).zfill(5)}_lang_'


# def get_keyboard() -> InlineKeyboardMarkup:

buttons: List[InlineKeyboardButton] = \
    [InlineKeyboardButton(text=lang, callback_data=f"{LANG_MSG_START}{lang}") for lang in Lexicon.supported_languages]
keyboard = [buttons]
# Создаем объект разметки инлайн-кнопок и добавляем кнопки в список кнопок
InlineLanguageKeyboard = InlineKeyboardMarkup(inline_keyboard=keyboard, row_width=2,
                                              resize_keyboard=True)
# return InlineLanguageKeyboard
# inline_keyboard.add()

# buttons: List[KeyboardButton] = [KeyboardButton(text=f"{lang}") for lang in Lexicon.supported_languages]
#
#
# keyboard: List[List[KeyboardButton]] = [buttons]
#
# LanguageKeyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
