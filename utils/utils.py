from sqlalchemy.orm import Session
from database.models import User, PaymentMovement
from database.database import engine, SessionLocal
from config.settings import TIMEZONE
import traceback
import pytz
from datetime import datetime
timezone = pytz.timezone(TIMEZONE)

def user_exists(user_id: int) -> bool:
    db = SessionLocal()
    try:
        exists = db.query(User).filter(User.id == user_id).first() is not None
        return exists
    finally:
        db.close()

def add_user(user_id: int, first_name: str, last_name: str | None, username: str | None):
    db = SessionLocal()
    existing_user = db.query(User).filter(User.id == user_id).first()
    
    if not existing_user:
        user = User(id=user_id, first_name=first_name, last_name=last_name, username=username)
        db.add(user)
        db.commit()
    
    db.close()

def set_user_state(user_id: int, state: str):
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    
    if user:
        user.state = state
        db.commit()
    
    db.close()

def get_user_state(user_id: int) -> str | None:
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    db.close()
    
    return user.state if user else None

def get_user_language(user_id: int) -> str | None:
    with SessionLocal() as db:
        user = db.query(User).filter(User.id == user_id).first()
        return user.language if user else None


def set_user_language(user_id: int, language: str):
    with SessionLocal() as db:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            user.language = language
            db.commit()

def add_to_payment_movements(user_id: int, email: str, total_price: float, payment_type: str):
    db = SessionLocal()
    payment_movement = PaymentMovement(telegram_id=user_id, email=email, total_price=total_price, payment_type=payment_type)
    db.add(payment_movement)
    db.commit()
    db.refresh(payment_movement)
    return payment_movement.id

def format_payment_success(message, total_price, payment_type, email, payment_movement_id):
    current_time = datetime.now(timezone).strftime('%Y-%m-%d %H:%M:%S')
    formatted_price = f"{total_price:,.2f}"
    return (
        f"✅ Muvaffaqiyatli to'lov qabul qilindi!\n\n"
        f"To'lov ID: #{payment_movement_id}\n"
        f"User ID: {message.from_user.id}\n"
        f"Username: @{message.from_user.username or ''}\n"
        f"FIO: {message.from_user.first_name} {message.from_user.last_name or ''}\n"
        f"Summa: {formatted_price} {message.successful_payment.currency}\n"
        f"To'lov usuli: #{payment_type}\n"
        f"Email: {email}\n"
        f"Sana: {current_time}\n"
    )