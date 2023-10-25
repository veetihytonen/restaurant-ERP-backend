from flask import request, session, abort

def check_csrf() -> None:
    # if session['csrf_token'] != request.form['csrf_token']:
    #     abort(403)
    return

def check_auth(access_level: int) -> tuple[bool, str | None]:
    # if 'username' not in session:
    #     return False, 'Et ole kirjautunut sisään'
        
    # if session['role'] < access_level:
    #     return False, 'Käyttäjälläsi ei ole oikeutta tähän toimintoon'
    
    return True, None
