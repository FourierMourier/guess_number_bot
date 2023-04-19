import random

from aiogram.types import (
    Message,
    # ordinary
    KeyboardButton, MenuButton, ReplyKeyboardMarkup, ReplyKeyboardRemove,
    # inline
    InlineKeyboardButton, InlineKeyboardMarkup,
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from lexicon.general import Lexicon

from typing import List, Optional, Any

LANG_MSG_START: str = f'_{str(random.randint(0, 10000 - 1)).zfill(5)}_lang_'

# === visible keyboard:
keyboard_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
visible_buttons: List[KeyboardButton] = [KeyboardButton(text=f"{lang}") for lang in Lexicon.supported_languages]
keyboard_builder.row(*visible_buttons, width=4)

VisibleLanguageKeyboard = keyboard_builder.as_markup()

# === inline keyboard:
inline_buttons: List[InlineKeyboardButton] = \
    [InlineKeyboardButton(text=lang, callback_data=f"{LANG_MSG_START}{lang}") for lang in Lexicon.supported_languages]
inline_keyboard = [inline_buttons]
# Создаем объект разметки инлайн-кнопок и добавляем кнопки в список кнопок
InlineLanguageKeyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard, row_width=2,
                                              resize_keyboard=True)
