from flask import Flask, render_template, abort
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Items

app = Flask(__name__)

engine = create_engine('sqlite:///items.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()



@app.route("/")
def root():  # put var here to pass to document
    # make pree stored querrys for larg rewquset volumes]
    ItemOBJ = session.query(Items).all()
    ItemsCatalog = session.query(Items.category).group_by(Items.category).all()
    # commo goes here to pass to document
    return render_template('root.html', ItemOBJ=ItemOBJ, ItemsCatalog=ItemsCatalog)

# TODO dynamic url


@app.route("/<categoryPath>")
def category(categoryPath):
    ItemOBJ = session.query(Items).filter(
        func.lower(Items.category) == func.lower(categoryPath))
    if 0 == ItemOBJ.count():
        abort(404)
    ItemsCatalog = session.query(Items.category).group_by(Items.category).all()
    return render_template('category.html', ItemOBJ=ItemOBJ, ItemsCatalog=ItemsCatalog)


# TODO add custome template per item and  TODO dynamic url
@app.route("/<categoryPath>/<itemPath>")
def item(categoryPath, itemPath):
    return "soccer item"


@app.route("/login")
def login():
    return render_template('login.html')


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=8080)
    print "server terminated"
