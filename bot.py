import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.bot.api import TelegramAPIServer
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from tg_bot.config import load_config
from tg_bot.filters.private_chat import IsPrivate
from tg_bot.handlers.add_album import register_add_album
from tg_bot.handlers.get_album import register_get_album
from tg_bot.handlers.help import register_help
from tg_bot.handlers.menu import register_menu
from tg_bot.handlers.start import register_start
from tg_bot.handlers.albums import register_albums
from tg_bot.handlers.start_training import register_start_training

logger = logging.getLogger(__name__)


def register_all_middlewares(dp):
    # dp.setup_middleware(...)
    pass


def register_all_filters(dp):
    #dp.filters_factory.bind(IsPrivate)
    pass


def register_all_handlers(dp):
    register_start(dp)
    register_help(dp)
    register_menu(dp)
    register_start_training(dp)
    register_albums(dp)
    register_add_album(dp)
    register_get_album(dp)


async def main():
    logging.basicConfig(level=logging.INFO,
                        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s')

    logger.info("Starting bot")
    config = load_config('.env')
    local_server = TelegramAPIServer.from_base("http://localhost:8081")
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML', server=local_server)

    storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
    dp = Dispatcher(bot, storage=storage)
    bot['config'] = config

    register_all_middlewares(dp)
    register_all_filters(dp)
    register_all_handlers(dp)

    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        session = await bot.get_session()
        await session.close()

if __name__ == '__main__':
    try:
        asyncio.run(main=main())
    except (KeyboardInterrupt, SystemExit):
        logger.error('Bot deadinside')