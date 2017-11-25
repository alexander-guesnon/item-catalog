
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Items
from flask import Flask
app = Flask(__name__)

engine = create_engine('sqlite:///items.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route("/")
def hello1():
    return "root"


@app.route("/soccer")
def hello2():
    return "soccer"


@app.route("/soccer/stuff")
def hello3():
    return "soccer item"


@app.route("/login")
def hello4():
    return "login"


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=8080)
    print "server terminated"
