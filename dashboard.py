import os
import logging
import logging.config
from logging import handlers
import yaml
import sqlite3
import json
from werkzeug.security import generate_password_hash, check_password_hash
from flask_extended import Flask
from flask import jsonify, request, session, g, redirect, url_for, render_template, flash, Response
from archives.core import searchAll
from archives.core import search as mysearch
from archives.core import get_translations
from lxml import etree
from archives import belgium
from contextlib import closing


app = Flask(__name__)
app.config.from_object(__name__)
# logConfig = yaml.load(open(os.path.join(app.instance_path, 'logging.conf')))
# logging.config.dictConfig(logConfig)
app.logger.setLevel(logging.DEBUG)
handler = handlers.RotatingFileHandler(
  os.path.join(app.instance_path, 'irp2.log'),
  maxBytes=1024 * 1024 * 100,
  backupCount=20)
app.logger.addHandler(handler)

app.config.update(dict(
    DATABASE=os.path.join(app.instance_path, 'irp2.db'),
    DEBUG=True,
    USERNAME='admin',
    PASSWORD='default',
    SECRET_KEY='INSECURE_DEVELOPMENT_KEY',
    PROPAGATE_EXCEPTIONS=True
))
config_yaml = os.path.join(app.instance_path, 'config.yaml')
if os.path.isfile(config_yaml):
    app.config.from_yaml(config_yaml)


def connect_db():
    """Connects to the specific database."""
    logging.info(str(app.config['DATABASE']))
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


@app.cli.command()
def init_db():
    db = get_db()
    with app.open_instance_resource('irp2_schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()
    logging.warn('Initialized the database.')


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    # db = getattr(g, '_database', None)
    # if db is None:
    #    db = g._database = connect_db()
    # return db
    return connect_db()


# @app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def getcollections():
    # global collections
    # if collections is None:
    with closing(open('static/collections_ld.json', 'r', encoding='utf-8')) as data_file:
        collections = json.load(data_file)
    return collections


@app.route('/')
def welcome():
    return render_template('welcome.html', collections=getcollections())


@app.route('/about')
def about():
    return render_template('about.html', collections=getcollections())


@app.route('/collections')
def collections():
    return render_template('collections.html', collections=getcollections())


@app.route('/glossary')
def glossary():
    return render_template('glossary.html', collections=getcollections())


@app.route('/join', methods=['POST', 'GET'])
def join():
    return render_template('join.html', collections=getcollections())


@app.route('/resources', methods=['GET'])
def resources():
    return render_template('resources.html', collections=getcollections())


@app.route('/tojoin', methods=['POST', 'GET'])
def tojoin():
    db = get_db()
    # read the posted values from the UI
    _name = request.form['usernamesignup']
    _email = request.form['emailsignup']
    _password = request.form['passwordsignup']
    # validate the received values
    if _name and _email and _password:
        cur = db.execute("""SELECT username FROM userprofile
                        WHERE email_id = ?;""", [_email])
        if len(cur.fetchall()) > 0:
            flash('This Email is already a user')
            return redirect(url_for('showLogin'))
        else:
            _pwhash = generate_password_hash(_password)
            db.execute("""INSERT INTO userprofile(username, password, email_id, registered_on)
                           values(?, ?, ?, date('now'));""",
                       [_name, _pwhash, _email])
            db.commit()
            flash('User created successfully !')
            return redirect(url_for('welcome'))
    else:
        return json.dumps({'html': '<span>Enter the required fields</span>'})


@app.route('/tologin', methods=['POST'])
def tologin():
    db = get_db()
    _uname = request.form['username'].strip()
    _password = request.form['password']
    cur = db.execute("""
        SELECT username, password, email_id, registered_on FROM userprofile
        WHERE ( username = ? OR email_id = ? )
        LIMIT 1;""", [_uname, _uname])
    row = cur.fetchone()
    if row is None:
        logging.debug("No matching row for login")
        return json.dumps({'html': '<span>Incorrect credentials. PLease try again.. </span>'})
    logging.debug("Got a matching row for login:\n"+str(row))
    if check_password_hash(row['password'], _password):
        session['_uname'] = row['username']
        session['_email'] = row['email_id']
        flash("Sign in succeeded. Welcome, {0}.".format(row['username']))
        return redirect(url_for('welcome'))
    else:
        return json.dumps({'html': '<span>Incorrect credentials. PLease try again.. </span>'})


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if '_uname' not in session:
        flash("You must login first to access your settings.")
        return redirect(url_for('welcome'))

    return render_template('settings.html', collections=getcollections())


@app.route('/saved', methods=['GET', 'POST'])
def saved():
    if '_uname' not in session:
        flash("You must login first to access your saved searches.")
        return redirect(url_for('welcome'))
    _uname = session["_uname"]
    savedata = []
    try:
        db = get_db()
        cur = db.execute("""SELECT username, searched_on, search_key FROM saved_search
                      WHERE username = ?
                      ORDER BY searched_on DESC;""", (_uname,))
        for row in cur:
            jsonstr = row[2]
            d = json.loads(jsonstr)
            savedata.append([row[0], row[1], d])
    except Exception as e:
        logging.error(str(e))
    return render_template('saved.html', searches=savedata, collections=getcollections())


@app.route('/logout')
def signout():
    if '_uname' not in session:
        return redirect(url_for('showLogin'))
    session.pop('_uname', None)
    flash("Log out succeeded.")
    return redirect(url_for('welcome'))


@app.route('/search', methods=['GET', 'POST'])
def search():
    myjsonld = getcollections()
    return render_template('ajaxsearch.html', collections=myjsonld, inputs=request.args)


@app.route('/searchAJAX', methods=['POST'])
def searchAJAX():
    inputs = request.form
    try:
        languages = inputs.getlist('languages')
    except Exception as e:
        logging.exception(e)
        pass
    logging.debug("/search with inputs:\n{0}".format(json.dumps(inputs)))
    session["inputs"] = inputs
    myargs = {}
    myargs['keywords'] = inputs.get('keywords', '')
    myargs['artist'] = inputs.get('artist', '')
    myargs['collectionid'] = inputs.get('collectionid', '')
    myargs['location'] = inputs.get('location', '')
    myargs['technique'] = inputs.get('technique', '')
    myargs['startYear'] = inputs.get('startYear', '')
    myargs['endYear'] = inputs.get('endYear', '')
    for key, value in myargs.items():
        if len(value) == 0 or str(value).strip() == '':
            myargs[key] = None
    if len(languages) > 0 and myargs['keywords'] is not None:
        translated_terms = get_translations(myargs['keywords'], languages)
        myargs['translated_terms'] = translated_terms
    result = mysearch(**myargs)
    return jsonify(result)


@app.route('/translate', methods=['POST'])
def translate():
    mylanguage = request.form.get('language')
    text = request.form.get('text')
    logging.info("/translate requesting '{0}' into {1}".format(text, mylanguage))
    mytranslation = get_translations(text, [mylanguage])
    logging.info("/translate got back '{0}'".format(mytranslation))
    return Response(mytranslation, mimetype='text/plain')


@app.route('/searchAll', methods=['GET', 'POST'])
def searchAllPage():
    languages = []
    if request.method == 'POST':
        inputs = request.form
        try:
            languages = request.form.getlist('languages')
        except Exception as e:
            logging.exception(e)
            pass
    if request.method == 'GET':
        inputs = request.args
        try:
            languages = request.args.getlist('languages')
        except Exception as e:
            logging.exception(e)
            pass
    logging.debug("/search with inputs:\n{0}".format(json.dumps(inputs)))
    session["inputs"] = inputs
    myargs = {}
    myargs['keywords'] = inputs.get('keywords', '')
    myargs['artist'] = inputs.get('artist', '')
    myargs['location'] = inputs.get('location', '')
    myargs['startYear'] = inputs.get('startYear', '')
    myargs['endYear'] = inputs.get('endYear', '')
    for key, value in myargs.items():
        if len(value) == 0 or str(value).strip() == '':
            myargs[key] = None

    if len(languages) > 0 and myargs['keywords'] is not None:
        translated_terms = get_translations(myargs['keywords'], languages)
        myargs['translated_terms'] = translated_terms

    results = searchAll(**myargs)
    return render_template("search.html", results=results,
                           collections=getcollections(), inputs=inputs)


@app.route('/saveSearch', methods=['POST'])
def saveSearch():
    inputs = None
    try:
        inputs = request.form['savedata']
        _uname = session["_uname"]
        db = get_db()
        db.execute("""INSERT INTO saved_search(username, searched_on, search_key)
                       values(?, date('now'), ?);""",
                   (_uname, inputs))
        db.commit()
        return jsonify({'result': 'yes'})
    except Exception as e:
        logging.error(e)
        return jsonify({'result': 'no', 'message': str(e)})


@app.route('/adsearch', methods=['GET', 'POST'])
def adsearch():
    if request.method == 'POST':
        keywords = request.form.getlist('keywords')
    if request.method == 'GET':
        keywords = request.args.getlist('keywords')
    result = belgium.findresult(keywords)
    return render_template('adsearch.html', results=result, collections=getcollections())


@app.route('/advsearch', methods=['GET', 'POST'])
def advsearch():
    tree = etree.parse("archives/belgium.xml")
    inventory = tree.getroot()
    session.clear()  # FIXME this is extreme
    # initial
    result = set(inventory.iter())
    title = request.form.get("title")
    if title != "":
        title_r = belgium.ftitle(inventory, title)
        result = result & title_r

    date = request.form["date"]
    if date != "":
        date_r = belgium.fdate(inventory, date)
        result = result & date_r

    type = request.form["type"]
    if type != "":
        type_r = belgium.ftype(inventory, type)
        result = result & type_r

    series = request.form["series"]
    if series != "":
        series_r = belgium.fseries(inventory, series)
        result = result & series_r

    text = request.form["text"]
    if text != "":
        text_r = belgium.ftext(inventory, text)
        result = result & text_r

    name = request.form["name"]
    if name != "":
        name_r = belgium.fname(inventory, name)
        result = result & name_r

    ls = belgium.getresult(result)
    return render_template('adsearch.html', results=ls, collections=getcollections())


@app.route('/detail', methods=['GET', 'POST'])
def detail():
    result = request.args.get("detail")
    return render_template('detail.html', results=result, collections=getcollections())


if __name__ == '__main__':
    app.run("0.0.0.0", processes=5)
