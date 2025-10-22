from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery
from .states import UserStates
from utils.utils import *
from config.settings import get_button_text, get_translation, ADMIN_ID, CLICK_TOKEN, PAYME_TOKEN
from keyboards.keyboards import *
import traceback
from aiogram.exceptions import TelegramForbiddenError
from aiogram.types import FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
import re
import os

PRICE=25000
router = Router()

@router.message(Command('start'))
async def start_handler_input(message: Message, state: FSMContext, bot: Bot):
    try:
        user_id = message.from_user.id
        language = get_user_language(user_id=user_id)
        if user_exists(user_id=user_id) and language is not None:
            await message.reply(get_translation('main_message', language=language), reply_markup=main_keyboard(language=language), parse_mode="HTML")
            await state.set_state(UserStates.main)
            set_user_state(user_id=user_id, state=UserStates.main.state)
        else:
            await message.reply(get_translation("start_message", 'en'), reply_markup=language_keyboard(), parse_mode="HTML")
            await state.set_state(UserStates.set_language)
    except Exception as e:
        await bot.send_message(chat_id=ADMIN_ID, text=f"Error occured on start_handler input: {e}")


@router.message(lambda message: message.text in [EN, RU, UZ], StateFilter(UserStates.set_language))
async def set_language_handler_input(message: Message, state: FSMContext, bot: Bot):
    try:
        user_id = message.from_user.id
        language_map = {
            "🇺🇸 English": "en",
            "🇺🇿 O'zbek Tili": "uz",
            "🇷🇺 Русский язык": "ru" 
        }
        language = language_map.get(message.text, "ru")
        set_user_state(user_id=user_id, state=UserStates.set_language.state)
        set_user_language(user_id=user_id, language=language)
        user_language = get_user_language(user_id=user_id)
        await message.reply(get_translation('main_message', user_language), reply_markup=main_keyboard(user_language), parse_mode="HTML")
        set_user_state(user_id=user_id, state=UserStates.main.state)
        await state.set_state(UserStates.main)
    except Exception as e:
        await bot.send_message(chat_id=ADMIN_ID, text=f"Error occured on set_language_handler_input input: {e}")


@router.message(lambda message: message.text == get_button_text('buy_premium_button', get_user_language(message.from_user.id)), StateFilter(UserStates.main))
async def handle_buy_premium(message: Message, state: FSMContext, bot: Bot):
    try:
        user_id = message.from_user.id
        language = get_user_language(user_id=user_id)
        set_user_state(user_id=user_id, state=UserStates.payment_info.state)
        await message.reply(
            get_translation('payment_info', language=language),
            reply_markup=confirmation_keyboard(language=language),
            parse_mode='HTML'
        )
        await state.set_state(UserStates.payment_info)
    except Exception as e:
        await bot.send_message(chat_id=ADMIN_ID, text=f"Error occured on handle_buy_premium input: {e}")

@router.message(lambda message: message.text == get_button_text('gift_premium_button', get_user_language(message.from_user.id)), StateFilter(UserStates.main))
async def handle_gift_premium(message: Message, state: FSMContext, bot: Bot):
    try:
        user_id = message.from_user.id
        language = get_user_language(user_id=user_id)
        set_user_state(user_id=user_id, state=UserStates.payment_info.state)
        await message.reply(
            get_translation('payment_info', language=language),
            reply_markup=confirmation_keyboard(language=language),
            parse_mode='HTML'
        )
        await state.set_state(UserStates.payment_info)
    except Exception as e:
        await bot.send_message(chat_id=ADMIN_ID, text=f"Error occured on handle_gift_premium input: {e}")

@router.message(lambda message: message.text == get_button_text('about_meteor_button', get_user_language(message.from_user.id)), StateFilter(UserStates.main))
async def handle_about_premium(message: Message, state: FSMContext, bot: Bot):
    try:
        user_id = message.from_user.id
        language = get_user_language(user_id=user_id)
        set_user_state(user_id=user_id, state=UserStates.main.state)
        await message.reply(
            get_translation('about_meteor', language=language),
            reply_markup=main_keyboard(language=language),
            parse_mode='HTML'
        )
        await state.set_state(UserStates.main)
    except Exception as e:
        await bot.send_message(chat_id=ADMIN_ID, text=f"Error occured on handle_about_premium input: {e}")

@router.message(lambda message: message.text == get_button_text('about_developer_button', get_user_language(message.from_user.id)), StateFilter(UserStates.main))
async def handle_about_premium(message: Message, state: FSMContext, bot: Bot):
    try:
        user_id = message.from_user.id
        language = get_user_language(user_id=user_id)
        set_user_state(user_id=user_id, state=UserStates.main.state)
        await message.reply(
            get_translation('about_developer', language=language),
            reply_markup=main_keyboard(language=language),
            parse_mode='HTML'
        )
        await state.set_state(UserStates.main)
    except Exception as e:
        await bot.send_message(chat_id=ADMIN_ID, text=f"Error occured on about_developer_button input: {e}")

@router.message(lambda message: message.text == get_button_text('confirm_button', get_user_language(message.from_user.id)), StateFilter(UserStates.payment_info))
async def handle_confirm_button(message: Message, state: FSMContext, bot: Bot):
    try:
        user_id = message.from_user.id
        language = get_user_language(user_id=user_id)
        set_user_state(user_id=user_id, state=UserStates.user_email.state)
        await message.reply(
            get_translation('email_ask', language=language),
            reply_markup=back_button(language=language),
            parse_mode='HTML'
        )
        await state.set_state(UserStates.user_email)
    except Exception as e:
        await bot.send_message(chat_id=ADMIN_ID, text=f"Error occured on handle_confirm_button input: {e}")

@router.message(lambda message: message.text == get_button_text('back_button_2', get_user_language(message.from_user.id)), StateFilter(UserStates.user_email))
async def handle_email_back_button(message: Message, state: FSMContext, bot: Bot):
    try:
        user_id = message.from_user.id
        language = get_user_language(user_id=user_id)
        set_user_state(user_id=user_id, state=UserStates.payment_info.state)
        await message.reply(
            get_translation('payment_info', language=language),
            reply_markup=confirmation_keyboard(language=language),
            parse_mode='HTML'
        )
        await state.set_state(UserStates.payment_info)
    except Exception as e:
        await bot.send_message(chat_id=ADMIN_ID, text=f"Error occured on handle_email_back_button input: {e}") 

@router.message(StateFilter(UserStates.user_email))
async def handle_email_button(message: Message, state: FSMContext, bot: Bot):
    try:
        user_id = message.from_user.id
        language = get_user_language(user_id=user_id)
        email = message.text.strip()
        await state.update_data(email=email)
        set_user_state(user_id=user_id, state=UserStates.payment_type.state)
        await message.reply(
            get_translation('payment_type', language=language),
            reply_markup=payment_options_keyboard(language=language),
            parse_mode='HTML'
        )
        await state.set_state(UserStates.payment_type)
    except Exception as e:
        await bot.send_message(chat_id=ADMIN_ID, text=f"Error occured on handle_email_button input: {e}")

@router.message(lambda message: message.text == get_button_text('click_button', get_user_language(message.from_user.id)), StateFilter(UserStates.payment_type))
async def handle_click_payment(message: Message, bot: Bot, state: FSMContext):
    try:
        prices = [LabeledPrice(label="Meteordub Premium Subscription", amount=5000000)]
        user_id = message.from_user.id
        language = get_user_language(user_id=user_id)
        await message.reply_invoice(
            title=f"Meteordub Premium",
            description="Premium orqali websiteda maksimal imkoniyatlardan foydalaning.",
            payload=f"CLICK",
            provider_token=CLICK_TOKEN,
            currency="UZS",
            prices=prices,
            start_parameter="premium_upgrade",
            reply_markup=purchase_button()
        )
    except Exception as e:
        await bot.send_message(chat_id=ADMIN_ID, text=f"Error occured on handle_click_payment input: {e}")

@router.message(lambda message: message.text == get_button_text('payme_button', get_user_language(message.from_user.id)), StateFilter(UserStates.payment_type))
async def handle_payme_payment(message: Message, bot: Bot, state: FSMContext):
    try:
        prices = [LabeledPrice(label="Meteordub Premium Subscription", amount=5000000)]
        user_id = message.from_user.id
        language = get_user_language(user_id=user_id)
        await message.reply_invoice(
            title=f"Meteordub Premium",
            description="Premium orqali websiteda maksimal imkoniyatlardan foydalaning.",
            payload=f"PAYME",
            provider_token=PAYME_TOKEN,
            currency="UZS",
            prices=prices,
            start_parameter="premium_upgrade",
            reply_markup=purchase_button()
        )
    except Exception as e:
        await bot.send_message(chat_id=ADMIN_ID, text=f"Error occured on handle_payme_payment input: {e}")


@router.pre_checkout_query(lambda _: True)
async def pre_checkout_handler(pre_checkout_query: PreCheckoutQuery, bot: Bot):
    try:
        await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
    except Exception as e:
        await bot.send_message(chat_id=ADMIN_ID, text=f"Error occured on pre_checkout_handler input: {e}")

@router.message(lambda message: message.successful_payment is not None, StateFilter(UserStates.payment_type))
async def successful_payment_handler(message: Message, bot: Bot, state: FSMContext):
    user_id = message.from_user.id
    language = get_user_language(user_id=user_id)
    try:
        total_price = message.successful_payment.total_amount / 100
        payment_type = message.successful_payment.invoice_payload
        data = await state.get_data()
        email = data.get("email")
        payment_movement_id = add_to_payment_movements(
            message.from_user.id,
            email,
            total_price,
            payment_type
        )
        set_user_state(user_id, UserStates.start.state)
        await bot.send_message(ADMIN_ID, format_payment_success(message, total_price, payment_type, email, payment_movement_id))
        await message.reply(get_translation('success_message', language=language).replace(':email',email), parse_mode='HTML', reply_markup=main_keyboard(language=language))
        await state.set_state(UserStates.start) 
    except Exception as e:
        await bot.send_message(chat_id=ADMIN_ID, text=f"Error occured on successful_payment_handler input: {e}")


@router.message(lambda message: message.text == get_button_text('decline_button', get_user_language(message.from_user.id)), StateFilter(UserStates.payment_info))
async def handle_decline_button(message: Message, state: FSMContext, bot: Bot):
    try:
        user_id = message.from_user.id
        language = get_user_language(user_id=user_id)
        set_user_state(user_id=user_id, state=UserStates.main.state)
        await message.reply(
            get_translation('main_message', language=language),
            reply_markup=main_keyboard(language=language),
            parse_mode='HTML'
        )
        await state.set_state(UserStates.main)
    except Exception as e:
        await bot.send_message(chat_id=ADMIN_ID, text=f"Error occured on handle_decline_button input: {e}")


@router.message(lambda message: message.text == get_button_text('back_button', get_user_language(message.from_user.id)), StateFilter(UserStates.payment_type))
async def handle_decline_button(message: Message, state: FSMContext, bot: Bot):
    try:
        user_id = message.from_user.id
        language = get_user_language(user_id=user_id)
        set_user_state(user_id=user_id, state=UserStates.user_email.state)
        await message.reply(
            get_translation('email_ask', language=language),
            reply_markup=back_button(language=language),
            parse_mode='HTML'
        )
        await state.set_state(UserStates.user_email)
    except Exception as e:
        await bot.send_message(chat_id=ADMIN_ID, text=f"Error occured on handle_decline_button input: {e}")

@router.message(StateFilter(UserStates.main))
async def main_handler(message: Message, state: FSMContext, bot: Bot):
    try:
        user_id = message.from_user.id
        language = get_user_language(user_id=user_id)
        await message.reply(get_translation('main_message', language=language), reply_markup=main_keyboard(language=language), parse_mode="HTML")
        set_user_state(user_id=user_id, state=UserStates.main.state)
    except Exception as e:
        await message.reply(f"Error occured: {e}")
        
@router.message(StateFilter(UserStates.set_language, UserStates.main, UserStates.payment_info, UserStates.payment_type))
async def handle_unrecognized_input(message: Message, state: FSMContext, bot: Bot):
    try:
        current_state = await state.get_state()
        user_id = message.from_user.id
        language = get_user_language(user_id=user_id)
        state_responses = {
            UserStates.set_language: {
                "text": get_translation('start_message', language=language),
                "keyboard": language_keyboard()
            },
            UserStates.payment_info: {
                "text": get_translation('payment_info', language=language),
                "keyboard": confirmation_keyboard(language=language)
            },
            UserStates.payment_type: {
                "text": get_translation('payment_type', language=language),
                "keyboard": payment_options_keyboard(language=language)
            }
        }
        response = state_responses.get(current_state, {
            "text": get_translation('main_message', language=language),
            "keyboard": main_keyboard(language=language)
        })

        await message.reply(
            response['text'],
            reply_markup=response['keyboard'],
            parse_mode='HTML'
        )

    except Exception as e:
        await message.reply(f'Error occured on handle_unrecognized_input handler: {e}')

@router.message()
async def fallback_handler(message: Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        language = get_user_language(user_id=user_id)
        if user_exists(user_id=user_id) and language is not None:
            await message.reply(get_translation('main_message', language=language), reply_markup=main_keyboard(language=language), parse_mode="HTML")  
            await state.set_state(UserStates.main)
            set_user_state(user_id=user_id, state=UserStates.main.state)

        else:
            await message.reply(get_translation('start_message', 'uz'), reply_markup=language_keyboard(), parse_mode='HTML')
            await state.set_state(UserStates.start)
            await set_user_state(user_id=user_id, state=UserStates.main.state)          
    except Exception as e:
        await message.reply(f"Error occured on fallback_handler: {e}")


