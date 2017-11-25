from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Items

app = Flask(__name__)

engine = create_engine('sqlite:///items.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route("/")
def root():  # put var here to pass to document
    return render_template('root.html')  # commo goes here to pass to document


@app.route("/soccer")  # dynamic url
def category():
    return render_template('category.html')


@app.route("/soccer/stuff")
def item():
    return "soccer item"


@app.route("/login")
def login():
    return render_template('login.html')


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=8080)
    print "server terminated"
