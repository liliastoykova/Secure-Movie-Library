import unittest
from unittest.mock import MagicMock
from fastapi import HTTPException
from data.models import User, UserCreate, UserBase
from services.user_service import UserService

def _make_user():
    return UserCreate(username="lilia",
                      role="USER",
                      password="Lilia123!",
                       )
def _make_service():
    user_repo = MagicMock()
    return UserService(user_repo), user_repo

class TestRegisterUser(unittest.TestCase):
    def test_user_is_created(self):
        service, repo = _make_service()

        created_user = User(
            id=5,
            username="lilia",
            password="hashed_password",
            role="USER"
        )

        repo.get_user_by_username.side_effect = [None, created_user]

        data = UserCreate(
            username="lilia",
            password="Lilia123!",
            role="USER"
        )

        result = service.register_user(data)

        self.assertEqual(result, created_user)

    def test_register_user_duplicate(self):
        service, repo = _make_service()

        data = _make_user()
        repo.get_user_by_username.return_value = data

        with self.assertRaises(HTTPException):
            service.register_user(data)


