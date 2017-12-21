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
from database_setup import Base, Items, Catagory


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


# This is the rooot endswitch this dictates the begainging of the website.


@app.route("/")
def root():
    top10Items = session.query(Items).order_by(Items.id.desc()).limit(10).all()
    ItemsCatalog = session.query(Catagory).all()
    return render_template('root.html', ItemOBJ=top10Items,
                           ItemsCatalog=ItemsCatalog,
                           Login_Session=login_session.get('access_token'))

# This is the catagory section of the website it showss all items in the
# specified catagory


@app.route("/<path:categoryPath>")
def category(categoryPath):
    categoryCheck = session.query(Catagory).filter(
        func.lower(Catagory.name) == func.lower(categoryPath))
    if 0 == categoryCheck.count():  # checking if it extists
        abort(404)
    itemsInCategory = session.query(Items, Catagory).filter(
        Catagory.id == Items.catagory_id).filter(
        func.lower(Catagory.name) == func.lower(categoryPath))
    ItemsCatalog = session.query(Catagory).all()
    return render_template('category.html', categoryPath=categoryPath,
                           itemsInCategory=itemsInCategory,
                           ItemsCatalog=ItemsCatalog,
                           Login_Session=login_session.get('access_token'))

# This will show indificual items that you wish to view


@app.route("/<path:categoryPath>/<path:itemPath>")
def item(categoryPath, itemPath):
    queriedItem = session.query(Items, Catagory).filter(
        Catagory.id == Items.catagory_id).filter(
        func.lower(Catagory.name) == func.lower(categoryPath),
        func.lower(Items.name) == func.lower(itemPath))

    if 0 == queriedItem.count():  # checking if it extists
        abort(404)
    print(queriedItem[0][0].name)
    return render_template('item.html',
                           queriedItem=queriedItem,
                           categoryPath=categoryPath,
                           itemPath=itemPath,
                           Login_Session=login_session.get('access_token'))

# sends html file to find out what edits you would like to make


@app.route("/<path:categoryPath>/<path:itemPath>/edit")
def edit(categoryPath, itemPath):
    if login_session.get('access_token') is None:  # is the user logged in
        abort(404)

    queriedItem = session.query(Items, Catagory).filter(
        Catagory.id == Items.catagory_id).filter(
        func.lower(Catagory.name) == func.lower(categoryPath),
        func.lower(Items.name) == func.lower(itemPath))
    if 0 == queriedItem.count():  # checking if it extists
        abort(404)

    ItemsCatalog = session.query(Catagory).all()
    return render_template('edit.html',
                           ItemsCatalog=ItemsCatalog,
                           categoryPath=categoryPath,
                           itemPath=itemPath,
                           message="")

# commits edits you have specified


@app.route("/<path:categoryPath>/<path:itemPath>/edit", methods=['POST'])
def editDB(categoryPath, itemPath):
    if login_session.get('access_token') is None:  # is the user logged in
        abort(404)

    queriedItem = session.query(Items, Catagory).filter(
        Catagory.id == Items.catagory_id).filter(
        func.lower(Catagory.name) == func.lower(categoryPath),
        func.lower(Items.name) == func.lower(itemPath))
    if 0 == queriedItem.count():  # checking if it extists
        abort(404)

    if len(list(request.form)) != 3:  # is their 3 items passed
        ItemsCatalog = session.query(Catagory).all()
        return render_template('edit.html',
                               ItemsCatalog=ItemsCatalog,
                               message="ERROR: All info was not filled out")
    # is the information correct and is not from a rogue post request
    # or somebody messing with the html in browser
    if not list(request.form)[0] == 'category' or \
            not list(request.form)[1] == 'name' or \
            not list(request.form)[2] == 'description':
        ItemsCatalog = session.query(Catagory).all()
        return render_template('edit.html',
                               ItemsCatalog=ItemsCatalog,
                               categoryPath=categoryPath,
                               itemPath=itemPath,
                               message="ERROR: Forum is not correct")

    # is the info the right length
    # this is mostly to sanitize input
    # prevent rouge post request
    if not (len(request.form['category']) > 0 and
            len(request.form['category']) <= 80) or \
            not (len(request.form['name']) > 0 and
                 len(request.form['name']) <= 80) or \
            not (len(request.form['description']) > 0 and
                 len(request.form['description']) <= 250):
        ItemsCatalog = session.query(Catagory).all()
        return render_template('edit.html',
                               ItemsCatalog=ItemsCatalog,
                               categoryPath=categoryPath,
                               itemPath=itemPath,
                               message="ERROR: not the right length")
    itemsInCategory = session.query(Items, Catagory).filter(
        Catagory.id == Items.catagory_id).filter(
        func.lower(Catagory.name) == func.lower(request.form['category']))
    # looking to see if the item is beeing reapeted
    for i in itemsInCategory:
        if request.form['name'].lower() == i[0].name.lower() and \
                request.form['category'].lower() == i[0].category.lower():
            ItemsCatalog = session.query(Catagory).all()
            return render_template('edit.html',
                                   ItemsCatalog=ItemsCatalog,
                                   categoryPath=categoryPath,
                                   itemPath=itemPath,
                                   message="ERROR: repeat item")

    itemQuery = session.query(Items).filter_by(id=queriedItem[0][0].id).one()
    if itemQuery != [] and itemQuery.user_id == login_session['username']:
        catagorytemp = session.query(Catagory).filter(
            Catagory.name == request.form['category']).one()
        itemQuery.name = request.form['name']
        itemQuery.catagory = catagorytemp
        itemQuery.description = request.form['description']
        session.add(itemQuery)
        session.commit()
        return render_template('redirect_response.html', title="Item edit",
                               response='The item has been edited to \
                            the database.')
    else:
        return render_template('redirect_response.html', title="ERROR",
                               response='trying to edit Item that is not \
                               yours.')

# sends delete html file to make sure the user wishes to delete the specified
# item


@app.route("/<path:categoryPath>/<path:itemPath>/delete")
def delete(categoryPath, itemPath):
    if login_session.get('access_token') is None:  # is the user logged in
        abort(404)

    queriedItem = session.query(Items, Catagory).filter(
        Catagory.id == Items.catagory_id).filter(
        func.lower(Catagory.name) == func.lower(categoryPath),
        func.lower(Items.name) == func.lower(itemPath))

    if 0 == queriedItem.count():  # checking if it extists
        abort(404)
    return render_template('delete.html',
                           categoryPath=categoryPath,
                           itemPath=itemPath)

# this will delete the specified itme


@app.route("/<path:categoryPath>/<path:itemPath>/delete", methods=['POST'])
def deleteItemDB(categoryPath, itemPath):
    if login_session.get('access_token') is None:  # is the user logged in
        abort(404)
    queriedItem = session.query(Items, Catagory).filter(
        Catagory.id == Items.catagory_id).filter(
        func.lower(Catagory.name) == func.lower(categoryPath),
        func.lower(Items.name) == func.lower(itemPath))
    if 0 == queriedItem.count():  # checking if it extists
        abort(404)

    itemQuery = session.query(Items).filter_by(id=queriedItem[0][0].id).one()
    if itemQuery != [] and itemQuery.user_id == login_session['username']:
        session.delete(itemQuery)
        session.commit()
        return render_template('redirect_response.html', title="Item deleted",
                               response='The item has been deleted to the \
                            database.')
    else:
        return render_template('redirect_response.html', title="ERROR",
                               response='trying to delete Item that is not \
                               yours.')

# sends html file to ask what you would like to add


@app.route("/add")
def add():
    if login_session.get('access_token') is None:  # is the user logged in
        abort(404)
    ItemsCatalog = session.query(Catagory).all()
    return render_template('add.html', ItemsCatalog=ItemsCatalog, message="")
# commits what you want to add


@app.route("/add", methods=['POST'])
def addToDB():
    if login_session.get('access_token') is None:  # is the user logged in
        abort(404)
    if len(list(request.form)) != 3:  # is their 3 items passed
        ItemsCatalog = session.query(Catagory).all()
        return render_template('add.html',
                               ItemsCatalog=ItemsCatalog,
                               message="ERROR: All info was not filled out")
    # is the information correct and is not from a rogue post request
    # or somebody messing with the html in browser
    if not list(request.form)[0] == 'category' or \
            not list(request.form)[1] == 'name' or \
            not list(request.form)[2] == 'description':
        ItemsCatalog = session.query(Catagory).all()
        return render_template('add.html',
                               ItemsCatalog=ItemsCatalog,
                               message="ERROR: Forum is not correct")
    # is the info the right length
    # this is mostly to sanitize input
    # prevent rouge post request
    if not (len(request.form['category']) > 0 and
            len(request.form['category']) <= 80) or \
            not (len(request.form['name']) > 0 and
                 len(request.form['name']) <= 80) or \
            not (len(request.form['description']) > 0 and
                 len(request.form['description']) <= 250):
        ItemsCatalog = session.query(Catagory).all()
        return render_template('add.html',
                               ItemsCatalog=ItemsCatalog,
                               message="ERROR: not the right length")

    itemsInCategory = session.query(Items, Catagory).filter(
        Catagory.id == Items.catagory_id).filter(
        func.lower(Catagory.name) == func.lower(request.form['category']))
    for i in itemsInCategory:
        if request.form['name'].lower() == i[0].name.lower() and \
                request.form['category'].lower() == i[0].catagory.name.lower():
            ItemsCatalog = session.query(Catagory).all()
            return render_template('add.html',
                                   ItemsCatalog=ItemsCatalog,
                                   message="ERROR: repeat item")
    catagorytemp = session.query(Catagory).filter(
        Catagory.name == request.form['category']).one()
    newItem = Items(name=request.form['name'],
                    catagory=catagorytemp,
                    description=request.form['description'],
                    user_id=login_session['username'])
    session.add(newItem)
    session.commit()
    return render_template('redirect_response.html', title="Item added",
                           response='The item has been added to the database.')


@app.route("/login")
def login():
    # current state of the server prevent attacks
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state,
                           Login_Session=login_session.get('access_token'))

# logs you in through google


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
        response = \
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
# logs you out through google


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

# prints all data in database to json file


@app.route('/api/v1/catalog.json')
def apiCatalog():
    entireDB = session.query(Items).all()
    itemList = []
    for i in entireDB:
        # python wont refesh data with out it being zeroed out
        itemDicionaryTemp = {
            "name": "",
            "id": 0,
            "category": "",
            "description": "",
            "user_id": ""
        }
        itemDicionaryTemp["name"] = i.name
        itemDicionaryTemp["id"] = i.id
        itemDicionaryTemp["category"] = i.catagory.name
        itemDicionaryTemp["description"] = i.description
        itemDicionaryTemp["user_id"] = i.user_id
        itemList.append(itemDicionaryTemp)
    return jsonify(itemList)
# prints all data in specified catagory to a json file


@app.route('/api/v1/query/<path:categoryPath>.json')
def apiCategory(categoryPath):
    itemsInCategory = session.query(Items, Catagory).filter(
        Catagory.id == Items.catagory_id).filter(
        func.lower(Catagory.name) == func.lower(categoryPath))
    if 0 == itemsInCategory.count():
        abort(404)
    itemList = []
    for i in itemsInCategory:
        # python wont refesh data with out it being zeroed out
        itemDicionaryTemp = {
            "name": "",
            "id": 0,
            "category": "",
            "description": "",
            "user_id": ""
        }
        itemDicionaryTemp["name"] = i[0].name
        itemDicionaryTemp["id"] = i[0].id
        itemDicionaryTemp["category"] = i[0].catagory.name
        itemDicionaryTemp["description"] = i[0].description
        itemDicionaryTemp["user_id"] = i[0].user_id
        itemList.append(itemDicionaryTemp)
    return jsonify(itemList)

# prints individual item from DB


@app.route('/api/v1/query/<path:categoryPath>/<path:itemPath>.json')  # all
def apiItem(categoryPath, itemPath):
    queriedItem = session.query(Items, Catagory).filter(
        Catagory.id == Items.catagory_id).filter(
        func.lower(Catagory.name) == func.lower(categoryPath),
        func.lower(Items.name) == func.lower(itemPath))
    if 0 == queriedItem.count():
        abort(404)
    itemDicionaryTemp = {
        "name": "",
        "id": 0,
        "category": "",
        "description": "",
        "user_id": ""
        }
    itemDicionaryTemp["name"] = queriedItem[0][0].name
    itemDicionaryTemp["id"] = queriedItem[0][0].id
    itemDicionaryTemp["category"] = queriedItem[0][0].catagory.name
    itemDicionaryTemp["description"] = queriedItem[0][0].description
    itemDicionaryTemp["user_id"] = queriedItem[0][0].user_id

    return jsonify(itemDicionaryTemp)


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=8080)
    print "server terminated"
