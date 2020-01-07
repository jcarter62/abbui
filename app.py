import os
import logging
import arrow
from flask import Flask, render_template, send_from_directory, request
from flask_bootstrap import Bootstrap

from logdir import LogFile
from data import Sites, Mrr, Site

app = Flask(__name__)
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
    s = Sites()
    data = s.sites
    total = s.total_flow

    context = {
        "data": data,
        "total": total,
    }
    return render_template('home.html', context=context)


@app.route('/site/<sitename>')
def route_site_site(sitename):
    log(request)
    s = Site(sitename=sitename)
    context = s.data
    return render_template('site.html', context=context)


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


