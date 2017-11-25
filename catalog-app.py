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
    # make pree stored querrys for larg rewquset volumes
    ItemOBJ = session.query(Items).all()
    for i in ItemOBJ:
        print(i.name)
        print(i.id)
        print(i.category)
        print(i.description)
    # commo goes here to pass to document
    return render_template('root.html', ItemOBJ=ItemOBJ)

# TODO dynamic url


@app.route("/<itemPath>")
def category(itemPath):
    print (itemPath)
    return render_template('category.html')


# TODO add custome template per item and  TODO dynamic url
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
