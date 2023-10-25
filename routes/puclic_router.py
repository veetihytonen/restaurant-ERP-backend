from flask import request
from flask.blueprints import Blueprint
from services.user_service import UserService
from http import HTTPMethod, HTTPStatus
from utils import check_auth


def make_public_router(service: UserService) -> Blueprint:
    router = Blueprint("main_router", __name__)
    
    @router.route('/login', methods=[HTTPMethod.POST])
    def login():
        data = request.get_json()

        username, password = data['username'], data['password']

        user = service.login(username, password)

        if not user:
            return 'Väärä käyttäjätunnus tai salasana', HTTPStatus.UNAUTHORIZED
        
        return user, HTTPStatus.OK
    
    @router.route('/logout', methods=[HTTPMethod.GET])
    def logout():
        auth = check_auth(access_level=0)
        if not auth[0]:
            return auth[1], HTTPStatus.UNAUTHORIZED
        
        service.logout()
        
        return 'Olet kirjautunut ulos', HTTPStatus.OK

    @router.route('/register', methods=[HTTPMethod.POST])
    def register():
        data = request.get_json()
        username, passw1, passw2, role = data['username'], data['password1'], data['password2'], data['role'], 
        
        try:
            user = service.register(username=username, password1=passw1, password2=passw2, role=role)
        except ValueError as error:
            return error.args[0], HTTPStatus.CONFLICT
        
        return user, HTTPStatus.CREATED

    return router