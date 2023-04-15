import sqlite3
import pydantic
from typing import Optional, List, Dict
import datetime

import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, Boolean


TABLE_NAME: str = 'users'
DB_NAME: str = 'guess_number_bot.db'


Base = declarative_base()


class UserTable(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    in_game = Column(Boolean)
    secret_number = Column(Integer)
    attempts = Column(Integer)
    total_games = Column(Integer)
    wins = Column(Integer)


engine = create_async_engine(f'sqlite+aiosqlite:///{DB_NAME}')


# create the users table if it doesn't exist
async def create_users_table():
    async with engine.begin() as conn: # 'users'
        if not await conn.run_sync(Base.metadata.tables[UserTable.__tablename__].exists):
            await conn.run_sync(Base.metadata.create_all)

# create the users table when the module is imported
asyncio.run(create_users_table())



def check_table_existence(table_name: str, cursor: sqlite3.Cursor) -> bool:
    query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'"
    cursor.execute(query)
    result = cursor.fetchone()
    if result is not None:
        return True
    else:
        return False


class UserModel(pydantic.BaseModel):
    id: int
    in_game: bool
    secret_number: Optional[int]
    attempts: Optional[int]
    total_games: int
    wins: int


# Connect to the database
connection = sqlite3.connect(DB_NAME)
cursor = connection.cursor()

if check_table_existence(TABLE_NAME, cursor=cursor):
    print(f"{TABLE_NAME} table exists in {DB_NAME}")
else:
    # Create the users table
    cursor.execute(f'''CREATE TABLE {TABLE_NAME}
                 (id INTEGER PRIMARY KEY, 
                  in_game INTEGER, 
                  secret_number INTEGER,
                  attempts INTEGER,
                  total_games INTEGER,
                  wins INTEGER)''')

    # Commit the changes and close the connection
    connection.commit()
    # do NOT close connection here:
    # connection.close()

    print(f"Created table {TABLE_NAME} in {DB_NAME} at {datetime.datetime.now().strftime(f'%H:%M:%S')}")

