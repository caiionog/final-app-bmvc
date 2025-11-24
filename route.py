from app.controllers.application import Application
from bottle import Bottle, route, run, request, static_file
from bottle import redirect, template, response

app = Bottle()
ctl = Application()

# decorator
def login_required(func):
    def wrapper(*args, **kwargs):
        if not ctl.is_logged():
            return redirect('/portal')
        return func(*args, **kwargs)
    return wrapper

#-----------------------------------------------------------------------------
# Rotas:

@app.route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root='./app/static')

@app.route('/helper')
def helper(info= None):
    return ctl.render('helper')

@app.route('/pagina', methods=['GET'])
@app.route('/pagina/<username>', methods=['GET'])
def action_pagina(username=None):
    if not username:
        return ctl.render('pagina')
    else:
        return ctl.render('pagina',username)

@app.route('/portal', method='GET')
def login():
    return ctl.render('portal')

@app.route('/portal', method='POST')
def action_portal():
    username = request.forms.get('username')
    password = request.forms.get('password')
    session_id, username= ctl.authenticate_user(username, password)
    if session_id:
        response.set_cookie('session_id', session_id, httponly=True, \
        secure=True, max_age=3600)
        redirect(f'/pagina/{username}')
    else:
        return redirect('/portal')
    
@app.route('/logout', method='GET')
def logout():
    ctl.logout_user()
    response.delete_cookie('session_id')
    redirect('/helper')
    
#-----------------------------------------------------------------------------
# Suas rotas aqui:

@app.route('/message-portal', method='GET')
@login_required
def message_portal():
    return ctl.render('message_portal')

@app.route('/message-portal', method='POST')
@login_required
def action_message_portal():
    text = request.forms.get('text')
    ctl.save_message(text)
    return redirect('/message-portal')

@app.route('/', method='GET')
def home():
    return ctl.render('messages')

@app.post('/messages/delete/<msg_id>')
@login_required
def delete_message_route(msg_id):
    ok = ctl.delete_message(msg_id)
    # opcional: informar se não foi possível
    return redirect('/')

@app.get('/messages/edit/<msg_id>')
@login_required
def edit_message(msg_id):
    message = ctl.get_message(msg_id)
    return template('app/views/html/edit_message', msg=message)

@app.post('/messages/edit/<msg_id>')
@login_required
def update_message(msg_id):
    new_text = request.forms.get('text')
    ctl.update_message(msg_id, new_text)
    redirect('/')

#-----------------------------------------------------------------------------

if __name__ == '__main__':
    run(app, host='0.0.0.0', port=8080, debug=True)
