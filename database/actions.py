import sqlite3
from .core import UserModel, UserTable
import datetime

import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession  # AsyncConnection
from utils.common.general import exceptionColorstr

from typing import Optional


async def get_user_by_id(user_id: int, session: AsyncSession) -> Optional[UserModel]:
    stmt = sqlalchemy.select(UserTable).where(UserTable.id == user_id)
    result = await session.execute(stmt)
    rows = result.fetchone()
    if rows:
        table_row: UserTable = rows[0]
        user = UserModel(
            id=table_row.id,
            in_game=table_row.in_game,
            secret_number=table_row.secret_number,
            attempts=table_row.attempts,
            total_games=table_row.total_games,
            wins=table_row.wins,
            lang=table_row.lang,
            last_activity_dt=table_row.last_activity_dt,
        )
        return user
    return None


async def update_user_data(user: UserModel, session: AsyncSession) -> None:
    try:
        # session.query(UserModel).filter_by(id=user.id).update({
        #     "in_game": user.in_game,
        #     "secret_number": user.secret_number,
        #     "attempts": user.attempts,
        #     "total_games": user.total_games,
        #     "wins": user.wins
        # })
        # await session.commit()
        stmt = sqlalchemy.update(UserTable).where(UserTable.id == user.id).values(
            in_game=user.in_game,
            secret_number=user.secret_number,
            attempts=user.attempts,
            total_games=user.total_games,
            wins=user.wins,
            lang=user.lang,
            last_activity_dt=user.last_activity_dt,
        )
        await session.execute(stmt)
        await session.commit()
    except Exception as e:
        print(exceptionColorstr(f"Failed to update user {user.id} data: {e}"))
        pass


async def add_new_user(user_id: int, curr_dt: datetime.datetime, session: AsyncSession):
    # using
    # user = UserTable(id=user_id,
    #                  in_game=False,
    #                  secret_number=None,
    #                  attempts=None,
    #                  total_games=0,
    #                  wins=0,
    #                  lang=None,
    #                  last_activity_dt=curr_dt,
    #                  )
    #
    # session.add(user)

    # will result in
    #   sqlalchemy.exc.MissingGreenlet: greenlet_spawn has not been called; can't call await_only() here.  ...
    #   https://sqlalche.me/e/20/xd2s
    # so use pure statements like below:

    lang: Optional[str] = None
    stmt = sqlalchemy.insert(UserTable).values(
        id=user_id,
        in_game=False,
        secret_number=None,
        attempts=None,
        total_games=0,
        wins=0,
        lang=lang,
        last_activity_dt=curr_dt,  # or None
    )
    await session.execute(stmt)
    await session.commit()


async def delete_inactive_users(session: AsyncSession, cutoff_time: datetime.datetime) -> int:
    # Query all inactive users to delete
    stmt = sqlalchemy.select(UserTable).filter(sqlalchemy.or_(
        UserTable.last_activity_dt == None,
        UserTable.last_activity_dt < cutoff_time
    ))
    # TODO: consider to delete max users per 1 statement with
    #               stmt = stmt.limit(max_deletions_per_statement)
    results = await session.execute(stmt)
    users_to_delete = results.scalars().all()
    if len(users_to_delete) == 0:
        return len(users_to_delete)
    # Delete inactive users from the database here
    for user in users_to_delete:
        stmt = sqlalchemy.delete(UserTable).where(UserTable.id == user.id)
        await session.execute(stmt)
        # OR simply: # may not work with `AsyncSession` object because .query is not there
        # session.delete(user)

    await session.commit()
    return len(users_to_delete)