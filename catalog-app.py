import requests
import random
import string
import httplib2
import json
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from flask import make_response
from flask import Flask, render_template, request
from flask import abort, redirect, jsonify, url_for, flash
from flask import session as login_session
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Items


app = Flask(__name__)
# PRIVATE KEY NOT FOR PRODUCTION USE
app.secret_key = 'L\x08\xbb\x82.".S\xf6\x0b\xff\xbb\xc4\x93\xcb\xf6W\x15\
\x03\xa8l\xfd\xb4\xa0\x02\x8a-\xca\x08\x0f\xda`'
CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())[
    'web']['client_id']
engine = create_engine('sqlite:///items.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route("/")
def root():

    ItemOBJ = session.query(Items).order_by(Items.id.desc()).limit(10).all()
    ItemsCatalog = session.query(Items.category).group_by(Items.category).all()

    return render_template('root.html', ItemOBJ=ItemOBJ,
                           ItemsCatalog=ItemsCatalog,
                           Login_Session=login_session.get('access_token'))


@app.route("/<categoryPath>")
def category(categoryPath):
    ItemOBJ = session.query(Items).filter(
        func.lower(Items.category) == func.lower(categoryPath))
    if 0 == ItemOBJ.count():
        abort(404)
    ItemsCatalog = session.query(Items.category).group_by(Items.category).all()
    return render_template('category.html',
                           ItemOBJ=ItemOBJ, ItemsCatalog=ItemsCatalog,
                           Login_Session=login_session.get('access_token'))


@app.route("/<categoryPath>/<itemPath>")
def item(categoryPath, itemPath):
    ItemOBJ = session.query(Items).filter(
        func.lower(Items.category) == func.lower(
            categoryPath), func.lower(Items.name) == func.lower(itemPath))
    if 0 == ItemOBJ.count():
        abort(404)
    return render_template('item.html',
                           ItemOBJ=ItemOBJ,
                           categoryPath=categoryPath,
                           itemPath=itemPath,
                           Login_Session=login_session.get('access_token'))


@app.route("/<categoryPath>/<itemPath>/edit")
def edit(categoryPath, itemPath):
    if login_session.get('access_token') is None:
        abort(404)

    ItemOBJ = session.query(Items).filter(
        func.lower(Items.category) == func.lower(
            categoryPath), func.lower(Items.name) == func.lower(itemPath))
    if 0 == ItemOBJ.count():
        abort(404)

    ItemsCatalog = session.query(
        Items.category).group_by(Items.category).all()
    return render_template('edit.html',
                           ItemsCatalog=ItemsCatalog,
                           categoryPath=categoryPath,
                           itemPath=itemPath,
                           message="")


@app.route("/<categoryPath>/<itemPath>/edit", methods=['POST'])
def editDB(categoryPath, itemPath):
    if login_session.get('access_token') is None:
        abort(404)

    ItemOBJ = session.query(Items).filter(
        func.lower(Items.category) == func.lower(
            categoryPath), func.lower(Items.name) == func.lower(itemPath))
    if 0 == ItemOBJ.count():
        abort(404)

    if len(list(request.form)) != 3:
        ItemsCatalog = session.query(
            Items.category).group_by(Items.category).all()
        return render_template('edit.html',
                               ItemsCatalog=ItemsCatalog,
                               message="ERROR: All info was not filled out")

    if not list(request.form)[0] == 'category' or \
            not list(request.form)[1] == 'name' or \
            not list(request.form)[2] == 'description':
        ItemsCatalog = session.query(
            Items.category).group_by(Items.category).all()
        return render_template('edit.html',
                               ItemsCatalog=ItemsCatalog,
                               categoryPath=categoryPath,
                               itemPath=itemPath,
                               message="ERROR: Forum is not correct")

    # is the info the right length
    # this is mostly to sanitize input
    # prevent rouge post request
    if not (len(request.form['category']) > 0 and
            len(request.form['category']) <= 250) or \
            not (len(request.form['name']) > 0 and
                 len(request.form['name']) <= 80) or \
            not (len(request.form['description']) > 0 and
                 len(request.form['description']) <= 250):
        ItemsCatalog = session.query(
            Items.category).group_by(Items.category).all()
        return render_template('edit.html',
                               ItemsCatalog=ItemsCatalog,
                               categoryPath=categoryPath,
                               itemPath=itemPath,
                               message="ERROR: not the right length")

    ItemOBJ = session.query(Items).filter(
        func.lower(Items.category) == func.lower(request.form['category']))
    for i in ItemOBJ:
        if request.form['name'] == i.name or \
                request.form['category'] != i.category:
            ItemsCatalog = session.query(
                Items.category).group_by(Items.category).all()
            return render_template('edit.html',
                                   ItemsCatalog=ItemsCatalog,
                                   categoryPath=categoryPath,
                                   itemPath=itemPath,
                                   message="ERROR: repeat item")

    itemQuery = session.query(Items).filter_by(id=ItemOBJ[0].id).one()
    # Create new Restaurant class
    if itemQuery != []:
        itemQuery.name = request.form['name']
        itemQuery.category = request.form['category']
        itemQuery.description = request.form['description']
        session.add(itemQuery)
        session.commit()
    return render_template('redirect_response.html', title="Item edit",
                           response='The item has been edited to \
                            the database.')


@app.route("/<categoryPath>/<itemPath>/delete")
def delete(categoryPath, itemPath):
    if login_session.get('access_token') is None:
        abort(404)
    ItemOBJ = session.query(Items).filter(
        func.lower(Items.category) == func.lower(
            categoryPath), func.lower(Items.name) == func.lower(itemPath))
    if 0 == ItemOBJ.count():
        abort(404)
    tempCatagory = session.query(Items).filter(
        func.lower(Items.category) == func.lower(categoryPath))
    if len(list(tempCatagory)) > 2:
        return render_template('redirect_response.html',
                               title="ERROR:Item can not be deleted",
                               response='you are trying to delete a catagory \
                                database.')
    return render_template('delete.html',
                           categoryPath=categoryPath,
                           itemPath=itemPath)


@app.route("/<categoryPath>/<itemPath>/delete", methods=['POST'])
def deleteItemDB(categoryPath, itemPath):
    if login_session.get('access_token') is None:
        abort(404)
    ItemOBJ = session.query(Items).filter(
        func.lower(Items.category) == func.lower(
            categoryPath), func.lower(Items.name) == func.lower(itemPath))
    if 0 == ItemOBJ.count():
        abort(404)
    tempCatagory = session.query(Items).filter(
        func.lower(Items.category) == func.lower(categoryPath))
    if len(list(tempCatagory)) > 2:
        return render_template('redirect_response.html',
                               title="ERROR:Item can not be deleted",
                               response='you are trying to delete a catagory \
                                database.')
    if itemtQuery != []:
        session.delete(itemtQuery)
        session.commit()
    return render_template('redirect_response.html', title="Item deleted",
                           response='The item has been deleted to the \
                            database.')


@app.route("/add")
def add():
    if login_session.get('access_token') is None:
        abort(404)
    ItemsCatalog = session.query(Items.category).group_by(Items.category).all()
    return render_template('add.html', ItemsCatalog=ItemsCatalog, message="")


@app.route("/add", methods=['POST'])
def addToDB():
    if login_session.get('access_token') is None:
        abort(404)

    if len(list(request.form)) != 3:
        ItemsCatalog = session.query(
            Items.category).group_by(Items.category).all()
        return render_template('add.html',
                               ItemsCatalog=ItemsCatalog,
                               message="ERROR: All info was not filled out")

    if not list(request.form)[0] == 'category' or \
            not list(request.form)[1] == 'name' or \
            not list(request.form)[2] == 'description':
        ItemsCatalog = session.query(
            Items.category).group_by(Items.category).all()
        return render_template('add.html',
                               ItemsCatalog=ItemsCatalog,
                               message="ERROR: Forum is not correct")

    # is the info the right length
    # this is mostly to sanitize input
    # prevent rouge post request
    if not (len(request.form['category']) > 0 and
            len(request.form['category']) <= 250) or \
            not (len(request.form['name']) > 0 and
                 len(request.form['name']) <= 80) or \
            not (len(request.form['description']) > 0 and
                 len(request.form['description']) <= 250):
        ItemsCatalog = session.query(
            Items.category).group_by(Items.category).all()
        return render_template('add.html',
                               ItemsCatalog=ItemsCatalog,
                               message="ERROR: not the right length")

    ItemOBJ = session.query(Items).filter(
        func.lower(Items.category) == func.lower(request.form['category']))
    for i in ItemOBJ:
        if request.form['name'] == i.name or \
                request.form['category'] != i.category:
            ItemsCatalog = session.query(
                Items.category).group_by(Items.category).all()
            return render_template('add.html',
                                   ItemsCatalog=ItemsCatalog,
                                   message="ERROR: repeat item")

    newItem = Items(name=request.form['name'],
                    category=request.form['category'],
                    description=request.form['description'])
    session.add(newItem)
    session.commit()
    return render_template('redirect_response.html', title="Item added",
                           response='The item has been added to the database.')


@app.route("/login")
def login():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state,
                           Login_Session=login_session.get('access_token'))


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

    return "Login Successful"


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        return render_template('redirect_response.html', title="Logout",
                               response='Current user not connected.')

    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % \
        login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        return render_template('redirect_response.html', title="Logout",
                               response='Successfully disconnected.')
    else:
        login_session['access_token'] = None
        return render_template('redirect_response.html', title="Logout",
                               response='Failed to revoke token for given \
                                user.')


@app.route('/api/v1/catalog.json')  # all
def apiCatalog():
    ItemOBJ = session.query(Items).all()
    itemList = []
    for i in ItemOBJ:
        # python wont refesh data with out it being zeroed out
        itemDicionaryTemp = {
            "name": "",
            "id": 0,
            "category": "",
            "description": ""
        }
        itemDicionaryTemp["name"] = i.name
        itemDicionaryTemp["id"] = i.id
        itemDicionaryTemp["category"] = i.category
        itemDicionaryTemp["description"] = i.description
        itemList.append(itemDicionaryTemp)
    return jsonify(itemList)


@app.route('/api/v1/query/<categoryPath>.json')  # all
def apiCategory(categoryPath):
    ItemOBJ = session.query(Items).filter(
        func.lower(Items.category) == func.lower(categoryPath))
    if 0 == ItemOBJ.count():
        abort(404)
    itemList = []
    for i in ItemOBJ:
        # python wont refesh data with out it being zeroed out
        itemDicionaryTemp = {
            "name": "",
            "id": 0,
            "category": "",
            "description": ""
        }
        itemDicionaryTemp["name"] = i.name
        itemDicionaryTemp["id"] = i.id
        itemDicionaryTemp["category"] = i.category
        itemDicionaryTemp["description"] = i.description
        itemList.append(itemDicionaryTemp)
    return jsonify(itemList)


@app.route('/api/v1/query/<categoryPath>/<itemPath>.json')  # all
def apiItem(categoryPath, itemPath):
    ItemOBJ = session.query(Items).filter(
        func.lower(Items.category) == func.lower(
            categoryPath), func.lower(Items.name) == func.lower(itemPath))
    if 0 == ItemOBJ.count():
        abort(404)
    itemDicionary = {
        "name": "",
        "id": 0,
        "category": "",
        "description": ""
    }
    itemDicionary["name"] = ItemOBJ[0].name
    itemDicionary["id"] = ItemOBJ[0].id
    itemDicionary["category"] = ItemOBJ[0].category
    itemDicionary["description"] = ItemOBJ[0].description
    return jsonify(itemDicionary)


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=8080)
    print "server terminated"
