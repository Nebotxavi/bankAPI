import time
from typing import List

from app.utils.utils import Crypt

from ..models.users import User

mock_users_list = [
    {
        "mail": "andrew.phew@apibank.com",
        "password": Crypt.hash('testpassword1'),
    },
    {
        "mail": "martin.gray@apibank.com",
        "password": Crypt.hash('testpassword2'),
    }
]


def parse_users(user_list):
    parsed_users: List[User] = []
    for user in user_list:
        parsed_users.append(User.parse_obj(user))
        time.sleep(0.01)

    return parsed_users


mock_parsed_users = parse_users(mock_users_list)
