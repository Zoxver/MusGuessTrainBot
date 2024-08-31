import logging
from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import IDFilter, CommandHelp


async def bot_help(message: types.Message):
    await message.answer('Список доступных команд:\n/start\n/help\n/ready')


async def bot_help_admin(message: types.Message):
    await message.answer('Список доступных админских команд:')
    await message.answer('Список доступных команд:\n/start\n/help\n/choose_task')


def register_help(dp: Dispatcher):
    dp.register_message_handler(bot_help_admin, CommandHelp(), IDFilter(user_id=466435942))
    dp.register_message_handler(bot_help, CommandHelp())
