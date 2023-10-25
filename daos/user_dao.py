from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import text

from sqlalchemy.exc import IntegrityError

class UserDao:
    def __init__(self, db_connection: SQLAlchemy) -> None:
        self.__db = db_connection

    def get_all_users(self) -> list[tuple]:
        sql = """
        SELECT (
            id, 
            username, 
            role
        )
        FROM 
            users
        """

        results = self.__db.session.execute(text(sql))
        
        return results.fetchall()

    def get_user_by_id(self, user_id: int) -> tuple:
        sql = """
        SELECT (
            id, 
            username, 
            role
        )
        FROM 
            users
        WHERE
            id = :id
        """
        
        results = self.__db.session.execute(text(sql), {'id': user_id})
        
        return results.fetchone()
            
    def login(self, username: str, password: str) -> bool | tuple:
        sql = """
        SELECT 
            id,
            username,
            password,
            role
        FROM 
            users 
        WHERE 
            username = :username
        """
        
        params = {'username': username}
        
        result = self.__db.session.execute(text(sql), params)
        user = result.fetchone()

        if not user:
            return False

        if not check_password_hash(user.password, password):
            return False 

        return {'id': user.id, 'username': user.username, 'role': user.role}

    def create_user(self, username: str, password: str, role: int):
        password_hash = generate_password_hash(password)

        sql = """
        INSERT INTO users (
            username,
            password,
            role
        )
        VALUES (
            :username,
            :password_hash,
            :role
        )
        RETURNING 
            id, 
            username,
            role
        """

        params = {
            'username': username, 
            'password_hash': password_hash,
            'role': role
        }

        try:
            results = self.__db.session.execute(text(sql), params)
            self.__db.session.commit()
        except IntegrityError:
            raise ValueError('Käyttäjä on jo olemassa')

        return results.fetchone()
s