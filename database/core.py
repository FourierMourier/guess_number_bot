import sqlite3
import pydantic
from typing import Optional, List, Dict
import datetime


TABLE_NAME: str = 'users'
DB_NAME: str = 'guess_number_bot.db'


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

