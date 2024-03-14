import asyncio
import logging
import os


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "news_channel.news_channel.settings")
os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = "true"

import django

django.setup()

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage
from aioredis import Redis
# from tgbot.handlers import main_menu, news, not_published_news, edit_title_and_text_news, edit_photo_news, \
#     edit_group_news, edit_tags_news

from tgbot.config import load_config

logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config = load_config(".env")

    storage = RedisStorage(Redis(host=config.redis_host)) if config.tg_bot.use_redis else MemoryStorage()
    dp = Dispatcher(storage=storage)
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')


    # Запускаем бота и пропускаем все накопленные входящие
    # Да, этот метод можно вызвать даже если у вас поллинг
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())