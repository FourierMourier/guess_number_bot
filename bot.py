import asyncio

import aiogram

from credentials.general import BotConfig
from handlers import game, general


async def main() -> None:

    bot: aiogram.Bot = aiogram.Bot(token=BotConfig.token)
    dispatcher = aiogram.Dispatcher()

    # routers:
    dispatcher.include_router(game.router)
    dispatcher.include_router(general.router)

    # remove extra updates + start polling:
    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
