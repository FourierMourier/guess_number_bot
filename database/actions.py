import sqlite3
from .core import UserModel

from typing import Optional


def get_user_by_id(user_id: int, cursor: sqlite3.Cursor) -> Optional[UserModel]:
    query = "SELECT * FROM users WHERE id = ?"
    cursor.execute(query, (user_id,))
    row = cursor.fetchone()
    if row is not None:
        user = UserModel(id=row[0],
                         in_game=bool(row[1]),
                         secret_number=row[2],
                         attempts=row[3],
                         total_games=row[4],
                         wins=row[5],)
        return user
    return None


def insert_user(user: UserModel, connection: sqlite3.Connection) -> bool:
    cursor = connection.cursor()
    query = "INSERT INTO users (id, in_game, secret_number, attempts, total_games, wins) VALUES (?, ?, ?, ?, ?, ?)"
    values = (user.id, user.in_game, user.secret_number, user.attempts, user.total_games, user.wins)
    try:
        cursor.execute(query, values)
        connection.commit()
        return True
    except Exception as e:
        print(f"Failed to insert user {user.id}: {e}")
        return False


def update_user_data(user: UserModel, connection: sqlite3.Connection) -> None:
    query = """
        UPDATE users
        SET in_game = ?,
            secret_number = ?,
            attempts = ?,
            total_games = ?,
            wins = ?
        WHERE id = ?
    """
    cursor = connection.cursor()
    data = (user.in_game, user.secret_number, user.attempts, user.total_games, user.wins, user.id)
    cursor.execute(query, data)
    connection.commit()
