from aiogram.fsm.state import State, StatesGroup

class UserStates(StatesGroup):
    start = State()
    set_language = State()
    main = State()
    payment_info = State()
    user_email = State()
    payment_type = State()
    payment_success = State()
    payment_unsuccess = State()
    