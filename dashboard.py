import os
import sys
import logging
import logging.config
import yaml
import sqlite3
import json
from werkzeug.security import generate_password_hash, check_password_hash
from flask_extended import Flask
from flask import jsonify, request, session, g, redirect, url_for, render_template, flash
from archives.core import searchAll
from archives.core import search as mysearch
from archives.core import archivesList
from archives.core import get_translations
from lxml import etree
from archives import belgium


app = Flask(__name__)
app.config.from_object(__name__)
logConfig = yaml.load(open(os.path.join(app.instance_path, 'logging.conf')))
logging.config.dictConfig(logConfig)
# app.logger.setLevel(logging.DEBUG)
# handler = handlers.RotatingFileHandler(
#     os.path.join(app.instance_path, 'irp2.log'),
#     maxBytes=1024 * 1024 * 100,
#     backupCount=20)
# app.logger.addHandler(handler)

app.config.update(dict(
    DATABASE=os.path.join(app.instance_path, 'irp2.db'),
    # DATABASE=os.path.join('postgresql://postgres:karishma@localhost', 'postgres'),
    DEBUG=True,
    USERNAME='admin',
    PASSWORD='default',
    SECRET_KEY='INSECURE_DEVELOPMENT_KEY'
))
config_yaml = os.path.join(app.instance_path, 'config.yaml')
if os.path.isfile(config_yaml):
    app.config.from_yaml(config_yaml)


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'dbconn'):
        g.dbconn = connect_db()
    return g.dbconn


@app.cli.command()
def init_db():
    db = connect_db()
    with app.open_resource('irp2_schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    logging.warn('Initialized the database.')


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'dbconn'):
        g.dbconn.close()


@app.route('/')
def render_index_page():
    return render_template('layout.html')


@app.route('/showLogin')
def showLogin():
    return render_template('login.html')


@app.route('/toregister', methods=['POST', 'GET'])
def login():
    db = get_db()
    # read the posted values from the UI
    _name = request.form['usernamesignup']
    _email = request.form['emailsignup']
    _password = request.form['passwordsignup']
    # validate the received values
    if _name and _email and _password:
        cur = db.execute("""SELECT username FROM user_profile
                        WHERE email_id = ?;""", [_email])
        if len(cur.fetchall()) > 0:
            flash('This Email is already a user')
            return redirect(url_for('showLogin'))
        else:
            _pwhash = generate_password_hash(_password)
            db.execute("""INSERT INTO user_profile(username, password, email_id, registered_on)
                           values(?, ?, ?, date('now'));""",
                       [_name, _pwhash, _email])
            db.commit()
            flash('User created successfully !')
            return redirect(url_for('showLogin'))
    else:
        return json.dumps({'html': '<span>Enter the required fields</span>'})


@app.route('/tologin', methods=['POST'])
def tologin():
    db = get_db()
    _uname = request.form['username'].strip()
    _password = request.form['password']
    cur = db.execute("""
        SELECT username, password, email_id, registered_on FROM user_profile
        WHERE ( username = ? OR email_id = ? )
        LIMIT 1;""", [_uname, _uname])
    row = cur.fetchone()
    if row is None:
        logging.debug("No matching row for login")
        return json.dumps({'html': '<span>Incorrect credentials. PLease try again.. </span>'})
    logging.debug("Got a matching row for login:\n"+str(row))
    if check_password_hash(row['password'], _password):
        session['_uname'] = _uname
        flash("Login Succeeded. Welcome {0}.".format(row['username']))
        return redirect(url_for('profile'))
    else:
        return json.dumps({'html': '<span>Incorrect credentials. PLease try again.. </span>'})


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if '_uname' not in session:
        return redirect(url_for('showLogin'))
    return render_template('profile.html')


@app.route('/logout')
def signout():
    if '_uname' not in session:
        return redirect(url_for('showLogin'))
    session.pop('_uname', None)
    return render_template('afterlogout.html')


@app.route('/searchOne', methods=['GET'])
def searchOne():
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
    myargs['collectionid'] = inputs.get('collectionid', '')
    myargs['location'] = inputs.get('location', '')
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


@app.route('/search', methods=['GET', 'POST'])
def search():
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
    return render_template("search.html", results=results, archivesList=archivesList, inputs=inputs)


@app.route('/saveSearch', methods=['GET', 'POST'])
def saveSearch():
    inputs = session["inputs"]
    _uname = session["_uname"]
    db = get_db()
    db.execute("""INSERT INTO saved_search(username, searched_on, search_key)
                   values(?, date('now'), ?);""",
               [_uname, json.dumps(inputs)])
    db.commit()
    flash('Your search has been saved.')
    return redirect(url_for('render_index_page'))


@app.route('/adsearch', methods=['GET', 'POST'])
def adsearch():
    if request.method == 'POST':
        keywords = request.form.getlist('keywords')
    if request.method == 'GET':
        keywords = request.args.getlist('keywords')
    result = belgium.findresult(keywords)
    return render_template('adsearch.html', results=result)


@app.route('/advsearch', methods=['GET', 'POST'])
def advsearch():
    tree = etree.parse("archives/belgium.xml")
    inventory = tree.getroot()
    session.clear()
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
    return render_template('adsearch.html', results=ls)


@app.route('/detail', methods=['GET', 'POST'])
def detail():
    result = request.args.get("detail")
    return render_template('detail.html', results=result)


if __name__ == '__main__':
    if len(sys.argv) > 1 and 'initdb' == sys.argv[1]:
        initdb_command()
    else:
        app.run("0.0.0.0")
