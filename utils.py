from flask import request, session, abort, redirect, flash, Response

def check_csrf() -> None:
    if session['csrf_token'] != request.form['csrf_token']:
        abort(403)

def check_auth(access_level: int) -> tuple[bool, Response | None]:
    if 'username' not in session:
        flash('Et ole kirjautunut sisään', 'error')
        
        return False, redirect('/login')

    if session['role'] < access_level:
        flash('Käyttäjälläsi ei ole oikeutta tähän toimintoon', 'error')

        return False, redirect('/')
    
    return True, None
