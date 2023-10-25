from flask import request, session, render_template, redirect, flash
from flask.blueprints import Blueprint
from services.user_service import UserService
from http import HTTPMethod

def make_main_router(service: UserService) -> Blueprint:
    router = Blueprint("main_router", __name__)

    @router.route('/', methods=[HTTPMethod.GET])
    def home():
        if 'username' in session:
            return render_template('index.html', role=session['role'])
        else:
            return redirect('/login')

    @router.route('/login', methods=[HTTPMethod.GET])
    def login_page():
        return render_template('login.html')
    
    @router.route('/login', methods=[HTTPMethod.POST])
    def login_action():
        username = request.form['username']
        password = request.form['password']

        user = service.login(username, password)

        if not user:
            flash('Väärä tunnus tai salasana', 'error')
            return redirect('/login')        
        
        return redirect("/")
    
    @router.route('/logout', methods=[HTTPMethod.GET])
    def logout():
        if 'username' not in session:
            flash('Et ole kirjautunut sisään', 'error')
            return redirect('/login')
        
        del session['id']
        del session['username']
        del session['role']
        del session['csrf_token']
        
        flash('Olet kirjautunut ulos', 'notification')
        return redirect('/login')

    @router.route('/register', methods=[HTTPMethod.POST])
    def register_action():
        form = request.form
        username, passw1, passw2, role = form['username'], form['password1'], form['password2'], form['role'], 
        
        try:
            user = service.register(username=username, password1=passw1, password2=passw2, role=role)
        except ValueError as error:
            flash(error.args[0], 'error')
            return redirect('/register')
        
        flash('Käyttäjän luominen onnistui', 'notification')
        return redirect('/login')

    return router