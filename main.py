import asyncio
import datetime
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.requests import Request
import uvicorn
from aiogram.types import Update

import handlers  # noqa
from loader import dp, bot
from config import WEBHOOK


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa
    # Стартуем! Я начну стрелять!
    with open('bot.log', 'a') as log_file:
        log_file.write(f'\n========== New bot session {datetime.datetime.now()} ==========\n\n')
    url_webhook = WEBHOOK
    await bot.set_webhook(url=url_webhook,
                          allowed_updates=dp.resolve_used_update_types(),
                          drop_pending_updates=True)
    yield
    await bot.delete_webhook()


app = FastAPI(lifespan=lifespan)


@app.post("/webhook/kurs_bot")
async def webhook(request: Request) -> None:
    update = Update.model_validate(await request.json(), context={"bot": bot})
    await dp.feed_update(bot, update)


# async def start_up():
#     with open('bot.log', 'a') as log_file:
#         log_file.write(f'\n========== New bot session {datetime.datetime.now()} ==========\n\n')
#     await bot.delete_webhook()
#     print('Стартуем')
#
#     await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        # asyncio.run(start_up())
        uvicorn.run(app, host="0.0.0.0", port=5000)
    except KeyboardInterrupt:
        print('Хорош, бро')