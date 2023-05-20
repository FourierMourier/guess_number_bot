import asyncio
import datetime

import aiogram

from credentials.general import BotConfig
from handlers import game, general

from utils.common.general import colorstr, infoColorstr, warningColorstr
from utils.common.wrappers import async_time_counter

from database.core import async_sessionmaker, AsyncSession, UserTable
from database.actions import delete_inactive_users


@async_time_counter()
async def delete_inactive_users_on_schedule():
    # for debug use 1.0
    every_period: float = 60 * 60  # 1.0  # 60 * 60
    # TODO: after you've deleted > max_deletions - return smth to quit the func
    max_deletions: int = 0 # 10
    performed_deletions: int = 0
    # use `-1` only for debugging since anything will be less than future
    days_diff: int = 6  # -1 # 0 # 6

    while True:
        # Delete inactive users from the database here
        async with async_sessionmaker() as session:
            # Calculate the cutoff time
            cutoff_time = datetime.datetime.utcnow() - datetime.timedelta(days=days_diff)

            deleted_users: int = await delete_inactive_users(session, cutoff_time)

        print(warningColorstr(f"Deleted {deleted_users} users at {datetime.datetime.now().strftime('%H:%M:%S.%f')}"))
        performed_deletions += 1

        # Log the number of deleted users
        print(warningColorstr(f"Total deletions so far: {performed_deletions}"))

        # Check if we have reached the max deletions limit
        if max_deletions != -1 and performed_deletions >= max_deletions:
            print(warningColorstr((f"Breaking the infinite loop for deleting inactive users "
                                   f"with performed deletions={performed_deletions}")))
            break

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
    delete_inactive_task: asyncio.Task = asyncio.create_task(delete_inactive_users_on_schedule())
    polling: asyncio.Task = asyncio.create_task(dispatcher.start_polling(bot))

    # now await them:
    await delete_inactive_task
    await polling  # dispatcher.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
