from flask import Flask, render_template, send_from_directory, request, session, redirect
from flask_bootstrap import Bootstrap
import os
import logging
import arrow
from auth import RemoveToken

from logdir import LogFile
from data import Sites, Mrr, Site

app = Flask(__name__)
app.config['SECRET_KEY'] = 'this is a secret key used by the flask web application.'

# app.config.update(
#     # Set the secret key to a sufficiently random value
#     SECRET_KEY='jdklsa;fjkafjiopgijegrqnljbngjliosolgrvf;vjdospji;djgfb',  ## os.urandom(24),
#     # Set the session cookie to be secure
#     SESSION_COOKIE_SECURE=True,
#     # Set the session cookie for our app to a unique name
#     SESSION_COOKIE_NAME='abbui',
#     # Set CSRF tokens to be valid for the duration of the session. This assumes you’re using WTF-CSRF protection
#     WTF_CSRF_TIME_LIMIT=None
#     #
#     # ref: https://developer.ibm.com/qradar/2018/10/03/secret-key-session-python-apps/
# )
bootstrap = Bootstrap(app)

logfile = LogFile(app_name='abbui')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
log_file_handler = logging.FileHandler(filename=logfile.full_path)
logger.addHandler(log_file_handler)
app.logger = logger


@app.route('/')
def route_home():
    log(request)

    if logged_in():
        s = Sites()
        data = s.sites
        total = s.total_flow

        context = {
            "data": data,
            "total": total,
        }
        return render_template('home.html', context=context)
    else:
        return redirect('/login')


def test_session_storage():
    print('session start')
    x = 'this is a variable'
    session['mykey'] = x
    print('session mykey saved with ' + x )
    xx = session.get('mykey')
    print()

def logged_in():
    from auth import TokenOK
    result = False
    if session.get('logged_in', '') == 'yes':
        tok = session.get('token', '')
        if tok > '':
            token_ok = TokenOK(token=tok)
            if token_ok.status == 'OK':
                result = True
    return result


@app.route('/login', methods=['GET', 'POST'])
def route_login():
    log(request)
    if request.method == 'GET':
        if session.get('token') is not None:
            if session.get('logged_in') == 'yes':
                RemoveToken(token=session.get('token'))

        context = {
            'username': session.get('username', ''),
            'password': ''
        }
        return render_template('login.html', context=context)
    else:
        # POST
        username = request.form['username']
        password = request.form['password']
        token = user_login(username=username, password=password)
        if token == '':
            session['username'] = username
            session['token'] = ''
            session['logged_in'] = 'no'
            return redirect('/login')
        else:
            session['username'] = username
            session['token'] = token
            session['logged_in'] = 'yes'
            return redirect('/')


@app.route('/logout')
def route_logout():
    log(request)
    token = session.get('token')
    if token is not None:
        rmtok = RemoveToken(token=token)

    session.pop('token')
    session.pop('username')
    session.pop('logged_in')
    return redirect('/')



def user_login(username='', password='') -> str:
    from auth import Login
    result = ''
    login = Login(username=username, password=password)
    if login.token > '':
        result = login.token
    return result


@app.route('/site/<sitename>')
def route_site_site(sitename):
    log(request)
    if logged_in():
        s = Site(sitename=sitename)
        context = s.data
        return render_template('site.html', context=context)
    else:
        return redirect('/login')


def findmrr(name, mrr):
    for m in mrr:
        if name.lower() == m['site'].lower():
            return m
    return None


def calc_age(record) -> str:
    if record is None:
        result = ''
    else:
        current_time = arrow.utcnow().timestamp
        age = current_time - record['t0']
        if age < 120:
            result = '0'
        elif age < 240:
            result = '1'
        elif age < 360:
            result = '2'
        elif age < 480:
            result = '3'
        else:
            result = '4'
        result = 'age' + result

    return result





@app.route('/favicon.ico')
def favicon():
    log(request)
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')

def log(req):
    import arrow
    now_string = arrow.now().format("YYYY/MM/DD-HH:mm:ss")
    obj = {
        'stamp': now_string,
        'url': req.path,
        'ip': req.remote_addr,
        'agent': req.user_agent,
    }

    new_file = LogFile(app_name='abbui').full_path
    current_file = app.logger.handlers[0].baseFilename
    if current_file != new_file:
        handler = app.logger.handlers[0]
        app.logger.removeHandler(hdlr=handler)
        handler = logging.FileHandler(filename=new_file)
        app.logger.addHandler(handler)

    logger.info('%(ip)s %(stamp)s %(url)s %(agent)s' % obj)

    return


if __name__ == '__main__':
    app.run()


