from auth.hashing import get_password_hash
from data.database import insert_query, read_query
from data.models import UserCreate, User


def create_user(user_data: UserCreate):
    sql = """INSERT INTO users (username, password, role)
                VALUES (?, ?, ?)"""
    hashed = get_password_hash(user_data.password)

    return insert_query(sql, (user_data.username, hashed, user_data.role))

def get_user_by_username(username: str):
    sql = """SELECT id, username, password, role
                FROM users
                WHERE username = ?"""

    rows = read_query(sql, (username, ))

    if not rows:
        return None

    row = rows[0]

    user = User(id=row[0],
                username=row[1],
                password=row[2],
                role=row[3])

    return user

