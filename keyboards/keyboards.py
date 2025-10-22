from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from config.settings import get_button_text, get_translation

UZ = "🇺🇿 O'zbek Tili"
EN = "🇺🇸 English"
RU = "🇷🇺 Русский"



def language_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=UZ)],
            [KeyboardButton(text=EN)],
            [KeyboardButton(text=RU)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

def main_keyboard(language: str = 'uz') -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_button_text('buy_premium_button', language)),
             KeyboardButton(text=get_button_text('gift_premium_button', language))],
            [KeyboardButton(text=get_button_text('about_meteor_button', language)),
             KeyboardButton(text=get_button_text('about_developer_button', language))],
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

def confirmation_keyboard(language: str = 'uz') -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_button_text('confirm_button', language))],
            [KeyboardButton(text=get_button_text('decline_button', language))],
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

def payment_options_keyboard(language: str = 'uz') -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_button_text('click_button', language)), KeyboardButton(text=get_button_text('payme_button', language))],
            [KeyboardButton(text=get_button_text('back_button', language))]
        ],
        resize_keyboard=True
    )

def purchase_button(language: str = 'uz') -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=get_button_text('purchase_button', language), pay=True)]
        ]
    )

def back_button(language: str = 'uz') -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_button_text('back_button_2', language))]
        ],
        resize_keyboard=True
    )