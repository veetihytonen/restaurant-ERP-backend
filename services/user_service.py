from flask import abort, request, session
from daos.user_dao import UserDao
from secrets import token_hex

class UserService:
    def __init__(self, dao: UserDao) -> None:
        self.__dao = dao

    def login(self, username: str, password: str):
        user = self.__dao.login(username, password)
        
        if not user:
            return False
        
        session['id'] = user['id']
        session['username'] = user['username']
        session['role'] = user['role']
        session['csrf_token'] = token_hex(16)

        return True

    def register(self, username: str, password1: str, password2: str, role: int):
        # validation failure returns dict: {'username': "error here", 'passwords': "error here"}
        
        # validate username:
        if len(username) < 4 or len(username) > 15:
            raise ValueError('Käyttäjänimen tulee olla 4 - 15 merkkiä')
        
        if password1 != password2:
            raise ValueError('Salasanojen tulee olla samat')

        # validate passwords:
        if len(password1) < 4:
            raise ValueError('Salasanan tulee olla vähintään 4 merkkiä')

        user_id, username, role  = self.__dao.create_user(username, password1, role)

        return True
