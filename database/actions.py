import sqlite3
from .core import UserModel, UserTable

import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession  # AsyncConnection
from utils.common.general import exceptionColorstr

from typing import Optional


# def get_user_by_id(user_id: int, cursor: sqlite3.Cursor) -> Optional[UserModel]:
#     query = "SELECT * FROM users WHERE id = ?"
#     cursor.execute(query, (user_id,))
#     row = cursor.fetchone()
#     if row is not None:
#         user = UserModel(id=row[0],
#                          in_game=bool(row[1]),
#                          secret_number=row[2],
#                          attempts=row[3],
#                          total_games=row[4],
#                          wins=row[5],)
#         return user
#     return None


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
        )
        return user
    return None


# def insert_user(user: UserModel, connection: sqlite3.Connection) -> bool:
#     cursor = connection.cursor()
#     query = "INSERT INTO users (id, in_game, secret_number, attempts, total_games, wins) VALUES (?, ?, ?, ?, ?, ?)"
#     values = (user.id, user.in_game, user.secret_number, user.attempts, user.total_games, user.wins)
#     try:
#         cursor.execute(query, values)
#         connection.commit()
#         return True
#     except Exception as e:
#         print(f"Failed to insert user {user.id}: {e}")
#         return False
#
#
# def update_user_data(user: UserModel, connection: sqlite3.Connection) -> None:
#     query = """
#         UPDATE users
#         SET in_game = ?,
#             secret_number = ?,
#             attempts = ?,
#             total_games = ?,
#             wins = ?
#         WHERE id = ?
#     """
#     cursor = connection.cursor()
#     data = (user.in_game, user.secret_number, user.attempts, user.total_games, user.wins, user.id)
#     cursor.execute(query, data)
#     connection.commit()


async def insert_user(user: UserModel, session: AsyncSession) -> bool:
    try:
        session.add(user)
        await session.commit()
        return True
    except Exception as e:
        print(f"Failed to insert user {user.id}: {e}")
        return False


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
            wins=user.wins
        )
        await session.execute(stmt)
        await session.commit()
    except Exception as e:
        print(exceptionColorstr(f"Failed to update user {user.id} data: {e}"))
        pass
