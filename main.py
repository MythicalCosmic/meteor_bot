import logging
import uvicorn
import asyncio
from fastapi import FastAPI
from aiogram.types import Update
from config.config import bot, dp
from config.settings import WEBHOOK, WEBHOOK_URL

app = FastAPI()

@app.post("/webhook")
async def webhook(update: dict):
    tg_update = Update(**update)
    await dp.feed_update(bot, tg_update)
    return {"status": "ok"}


async def on_startup():
    if WEBHOOK:
        logging.info("Setting webhook...")
        await bot.set_webhook(WEBHOOK_URL)
    else:
        logging.info("Deleting webhook and starting polling...")
        await bot.delete_webhook(drop_pending_updates=True)
        asyncio.create_task(dp.start_polling(bot))  # non-blocking


def start():
    logging.info(f"Starting in {'WEBHOOK' if WEBHOOK else 'POLLING'} mode.")
    if WEBHOOK:
        uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
    else:
        asyncio.run(on_startup())


if __name__ == "__main__":
    start()
