import os
from pathlib import Path
import sqlite3
import pydantic
from typing import Optional, List, Dict
import datetime

import asyncio
import sqlalchemy
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncConnection
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql import select, update, delete
from sqlalchemy import Column, Integer, Boolean, String, DateTime

from utils.common.general import infoColorstr


ROOT: Path = Path(__file__).parents[0]
PROJECT_ROOT: Path = ROOT.parents[0]

TABLE_NAME: str = 'users'
DB_NAME: str = 'guess_number_bot.db'

Base = declarative_base()
Metadata = Base.metadata


class UserTable(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    in_game = Column(Boolean)
    secret_number = Column(Integer)
    attempts = Column(Integer)
    total_games = Column(Integer)
    wins = Column(Integer)
    lang = Column(String)
    last_activity_dt = Column(DateTime, default=datetime.datetime.utcnow)
    # last_activity_dt = Column(DateTime, default=None)


# echo for logging all sql-statements to the console adn future for 2.0 features support
DATABASE_PATH: str = str(PROJECT_ROOT / DB_NAME)
DATABASE_URI: str = f'sqlite+aiosqlite:///{DATABASE_PATH}'
engine = create_async_engine(DATABASE_URI, echo=True, future=True)
# Create a sessionmaker
# async_session = sessionmaker(engine, class_=AsyncSession)
async_sessionmaker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=True) # False)


class SyncSqliteConnection:
    """
    Please use this class as the context manager like
        with SyncSqliteConnection(DB_NAME) as cursor:
            user: Optional[UserModel] = get_user_by_id(user_id, cursor=cursor)
    but for async code use
    """

    __slots__ = ('db_name', 'connection', 'cursor')

    def __init__(self, db_name: str):
        self.db_name = db_name
        self.connection: Optional[sqlite3.Connection] = None
        self.cursor: Optional[sqlite3.Cursor] = None

    def __enter__(self) -> sqlite3.Cursor:
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.connection.close()
        self.cursor = None
        self.connection = None


async def check_table_existence(table_name: str,
                                conn: AsyncConnection,
                                ) -> bool:
    # not able to do the following:
    # inspector = sqlalchemy.inspect(conn)
    # return await conn.run_sync(
    #     inspector.has_table, table_name, schema=None
    # )
    # see
    #   https://docs.sqlalchemy.org/en/20/errors.html#error-xd3s
    # inspector = sqlalchemy.inspect(conn)
    tables = await conn.run_sync(
        lambda sync_conn: sqlalchemy.inspect(sync_conn).get_table_names()
    )
    return table_name in tables


# create the users table if it doesn't exist
async def create_users_table():
    async with engine.begin() as conn:
        # async with async_sessionmaker() as session:
        if not await check_table_existence(UserTable.__tablename__, conn):  # session):
            await conn.run_sync(Base.metadata.create_all)
        else:
            print(infoColorstr(f"There's already database with users table at {DATABASE_URI}"))

# create the users table when the module is imported
asyncio.run(create_users_table())


# def check_table_existence(table_name: str, cursor: sqlite3.Cursor) -> bool:
#     query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'"
#     cursor.execute(query)
#     result = cursor.fetchone()
#     if result is not None:
#         return True
#     else:
#         return False

class UserModel(pydantic.BaseModel):
    id: int
    in_game: bool
    secret_number: Optional[int]
    attempts: Optional[int]
    total_games: int
    wins: int
    lang: Optional[str]
    last_activity_dt: Optional[datetime.datetime]

# # Connect to the database
# connection = sqlite3.connect(DB_NAME)
# cursor = connection.cursor()
#
# if check_table_existence(TABLE_NAME, cursor=cursor):
#     print(f"{TABLE_NAME} table exists in {DB_NAME}")
# else:
#     # Create the users table
#     cursor.execute(f'''CREATE TABLE {TABLE_NAME}
#                  (id INTEGER PRIMARY KEY,
#                   in_game INTEGER,
#                   secret_number INTEGER,
#                   attempts INTEGER,
#                   total_games INTEGER,
#                   wins INTEGER)''')
#
#     # Commit the changes and close the connection
#     connection.commit()
#     # do NOT close connection here:
#     # connection.close()
#
#     print(f"Created table {TABLE_NAME} in {DB_NAME} at {datetime.datetime.now().strftime(f'%H:%M:%S')}")
#
