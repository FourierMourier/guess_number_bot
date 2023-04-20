import asyncio
import datetime

import aiogram

from credentials.general import BotConfig
from handlers import game, general

from utils.common.general import colorstr, infoColorstr, warningColorstr
from utils.common.wrappers import async_time_counter

from typing import List


@async_time_counter()
async def delete_inactive_users():
    # for debug use 1.0
    every_period: float = 60 * 60  # 1.0  # 60 * 60
    # TODO: after you've deleted > max_deletions - return smth to quit the func
    max_deletions: int = 10
    while True:
        # Delete inactive users from the database here
        print(warningColorstr(f"deleting users at {datetime.datetime.now().strftime('%H:%M:%S.%f')}"))
        await asyncio.sleep(every_period)  # Sleep for 60 minutes


async def main() -> None:

    bot: aiogram.Bot = aiogram.Bot(token=BotConfig.token)
    dispatcher = aiogram.Dispatcher()

    # routers:
    dispatcher.include_router(game.router)
    dispatcher.include_router(general.router)

    # remove extra updates + start polling:
    await bot.delete_webhook(drop_pending_updates=True)
    # create tasks:
    delete_inactive_task: asyncio.Task = asyncio.create_task(delete_inactive_users())
    polling: asyncio.Task = asyncio.create_task(dispatcher.start_polling(bot))

    # now await them:
    await delete_inactive_task
    await polling  # dispatcher.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
