from data.database import insert_query, read_query
from data.models import UserCreate, User


def create_user(user_data: UserCreate):
    sql = """INSERT INTO users (username, password, role)
                VALUES (?, ?, ?)"""

    return insert_query(sql, (user_data.username, user_data.password, user_data.role))

def get_user_by_username(username: str):
    sql = """SELECT id, username, role
                FROM users
                WHERE username = ?"""

    rows = read_query(sql, (username, ))

    if not rows:
        return None

    row = rows[0]

    user = User(id=row['id'],
                username=row['username'],
                password=row['password'],
                role=row["role"])

    return user

