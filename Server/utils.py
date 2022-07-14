import random
import string

from dataclasses import dataclass
from hashlib import sha256
from os.path import exists

if not exists("database.db"):
    file = open("database.db", 'w')
    file.write("")
    file.close()

if not exists("valid_session_ids.dat"):
    file = open("valid_session_ids.dat", 'w')
    file.write("")
    file.close()


@dataclass(frozen=True)
class User:
    """
    very simple class to store User data (sql would be much better)
    """
    id: int
    username: str
    password_hash: str


def login_check_database(username: str, passwd: str) -> bool:
    """
    simple function to authenticate logging in user
    :param username: str
    :param passwd: str
    :return: bool
    """
    database = load_database()
    pasword_hash = sha256(passwd.encode("utf8")).hexdigest()
    for user_id, user in database.items():
        if username == user.username and pasword_hash == user.password_hash:
            return True
    return False


def write_database(username: str, passwd: str) -> None:
    pasword_hash = sha256(passwd.encode("utf8")).hexdigest()
    with open("database.db", 'r') as f:
        lines = f.readlines()
    next_id = len(lines) + 1
    with open("database.db", 'a') as f:
        f.write(f"{next_id};{username};{pasword_hash}\n")


def load_database() -> dict[int:User]:
    """
    function returns dictionary of users with user_id being the key
    :return: dict[int:User]
    """
    data = dict()
    with open("database.db", 'r') as f:
        for line in f.readlines():
            user_id, username, passwd = line.strip().split(';')
            data[int(user_id)] = User(int(user_id), username, passwd)
    return data


def write_session_id(username: str) -> str:
    session_id = ''.join(random.choice(string.ascii_letters) for _ in range(20))
    with open("valid_session_ids.dat", 'a') as f:
        f.write(f"{username};{session_id}")
    return session_id


if __name__ == '__main__':
    write_database("test", "test")
    # print(login_check_database("test", "test1"))
    # write_session_id()
