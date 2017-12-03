import requests
import random
import string
import httplib2
import json
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from flask import make_response
from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from flask import abort
from flask import session as login_session
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Items


app = Flask(__name__)
# PRIVATE KEY NOT FOR PRODUCTION USE
app.secret_key = 'L\x08\xbb\x82.".S\xf6\x0b\xff\xbb\xc4\x93\xcb\xf6W\x15\x03\xa8l\xfd\xb4\xa0\x02\x8a-\xca\x08\x0f\xda`'
CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())[
    'web']['client_id']
engine = create_engine('sqlite:///items.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route("/")
def root():

    ItemOBJ = session.query(Items).limit(10).all()
    ItemsCatalog = session.query(Items.category).group_by(Items.category).all()

    return render_template('root.html', ItemOBJ=ItemOBJ, ItemsCatalog=ItemsCatalog)


@app.route("/<categoryPath>")
def category(categoryPath):
    ItemOBJ = session.query(Items).filter(
        func.lower(Items.category) == func.lower(categoryPath))
    if 0 == ItemOBJ.count():
        abort(404)
    ItemsCatalog = session.query(Items.category).group_by(Items.category).all()
    return render_template('category.html', ItemOBJ=ItemOBJ, ItemsCatalog=ItemsCatalog)


@app.route("/<categoryPath>/<itemPath>")
def item(categoryPath, itemPath):
    ItemOBJ = session.query(Items).filter(func.lower(Items.category) == func.lower(
        categoryPath), func.lower(Items.name) == func.lower(itemPath))
    if 0 == ItemOBJ.count():
        abort(404)
    return render_template('item.html', ItemOBJ=ItemOBJ)


@app.route("/login")
def login():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data
    try:
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response - \
            make_response(json.dumps(
                'Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' %
           access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps(result.get(
            "Token's user ID doesn't match give user ID.")), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    if result['issued_to'] != CLIENT_ID:
        response = make_response(json.dumps(result.get(
            "Token's client ID does not match app's.")), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(result.get(
            'current user is already connected')), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = json.loads(answer.text)
    login_session['username'] = data["name"]
    login_session['picture'] = data["picture"]
    login_session['email'] = data["email"]

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=8080)
    print "server terminated"
