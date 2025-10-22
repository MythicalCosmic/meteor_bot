from aiogram import BaseMiddleware
from aiogram.types import Message
from handlers.states import UserStates
from keyboards.keyboards import language_keyboard
from config.settings import get_translation
from utils.utils import * 

class UserRegistrationMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message, data: dict):
        
        user_id = event.from_user.id
        first_name = event.from_user.first_name
        last_name = event.from_user.last_name
        username = event.from_user.username
        language = get_user_language(user_id=user_id)
        
        if not user_exists(user_id):
            add_user(user_id, first_name, last_name, username)
            set_user_state(user_id, UserStates.set_language.state)
            
            await event.answer(
                get_translation('start_message', language=language),
                reply_markup=language_keyboard(),
                parse_mode='HTML'
            )
            state = data['state']
            await state.set_state(UserStates.set_language)
            return 
        
        return await handler(event, data)


class PrivateChatMiddleware(BaseMiddleware):
    async def __call__(self, handler, event,  data: dict):
        if event.chat.type != "private":
            return
        
        
        return await handler(event, data)