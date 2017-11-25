from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
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


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), WebServerHandler)
        print "Web server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print "Stopping web server..."
        server.socket.close()


if __name__ == "__main__":
    main()
    print "server terminated"
