from flask import Flask, render_template, send_from_directory, request, session, redirect
from flask_bootstrap import Bootstrap
from flask_mongo_session.session_processor import MongoSessionProcessor
import os
import logging
import arrow
from auth import RemoveToken

from logdir import LogFile
from data import Sites, Mrr, Site

app = Flask(__name__)

#
# Setup Server based session storage.
#
try:
    def getenv(name) -> str:
        result = ''
        value = os.getenv(name)
        if value is None:
            raise Exception('Environment Variable %s Missing' % name)
        else:
            result = value
        return result

    s_cookie_name = getenv('SESSION_COOKIE_NAME')
    s_host = getenv('SESSION_HOST')
    s_port = getenv('SESSION_PORT')
    s_db = getenv('SESSION_DB')
    _mongoconn_ = 'mongodb://%s:%s/%s' % (s_host, s_port, s_db)
    app.session_cookie_name = s_cookie_name
    app.session_interface = MongoSessionProcessor(_mongoconn_)
except Exception as e:
    print('Error with Environment: %s ' % e.__str__())
    exit()



bootstrap = Bootstrap(app)

logfile = LogFile(app_name='abbui-app')
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
            "loginout": login_logout(request)
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
            'password': '',
            "loginout": login_logout(request)
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
        context["loginout"] = login_logout(request)

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

#
# check session, and see if user is logged in.
# if Logged In, then return "logout" with correct url.
# if not, then return "login" and respective url.
#
def login_logout(req: request):
    if session.get('logged_in') == 'yes':
        result = {'url': '/logout', 'label': 'Logout'}
    else:
        result = {'url': '/login', 'label': 'Login'}
    return result




if __name__ == '__main__':
    app.run()


