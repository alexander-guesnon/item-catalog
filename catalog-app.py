from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Items

engine = create_engine('sqlite:///items.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session =DBSession()


class WebServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output=""#templet
                output+="""<html>
                <head>
                <style>
                .navbar-collapse.collapse {
                display: block!important;
                }

                .navbar-nav>li, .navbar-nav {
                float: left !important;
                }

                .navbar-nav.navbar-right:last-child {
                margin-right: -15px !important;
                }

                .navbar-right {
                float: right!important;
                }
                </style>
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <script
                src="https://code.jquery.com/jquery-3.2.1.js"
                integrity="sha256-DZAnKJ/6XZ9si04Hgrsxu/8s717jcIzLy3oi35EouyE="
                crossorigin="anonymous"></script>
                <script
                src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"
                integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa"
                crossorigin="anonymous"></script>
                <link
                href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"
                rel="stylesheet"
                integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u"
                crossorigin="anonymous">
                </head>
                <body>
                <nav class="navbar navbar-default" role="navigation">
                <div class="container-fluid">
                <ul class="nav navbar-nav navbar-left">
                <li>
	        <h1><a href="/">Catalog App</a></h1>
                </li>
                </ul>

	        <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
      
	        <ul class="nav navbar-nav navbar-right">
                <li><a href="/login"><button class="btn">Login</button></a></li>
	        </ul>
	        </div>
                </div>
                </nav>
    
                <div class="container">
                <div class="row">
	        <div class="col-sm-4">
	        <h2>Categories</h2>
	        <a href="/soccer">Soccer</a>
	        </div>
	        <div class="col-sm-8">
	        <h2>Latest Items</h2>
	        <a href="/soccer/stuff">stuff</a> (Soccer)
	        </div>
                </div>
                </div>
    
                <footer><center><a href="#">Alex Guesnon</a></center></footer>
                </body>
                </html>
                """

                self.wfile.write(output)
                print(output)
                return
            if self.path.endswith("/soccer"):#dynamicly change this to each catagory
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output=""#templet
                output+="""<html>
                <head>
                <style>
                .navbar-collapse.collapse {
                display: block!important;
                }

                .navbar-nav>li, .navbar-nav {
                float: left !important;
                }

                .navbar-nav.navbar-right:last-child {
                margin-right: -15px !important;
                }

                .navbar-right {
                float: right!important;
                }
                </style>
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <script
                src="https://code.jquery.com/jquery-3.2.1.js"
                integrity="sha256-DZAnKJ/6XZ9si04Hgrsxu/8s717jcIzLy3oi35EouyE="
                crossorigin="anonymous"></script>
                <script
                src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"
                integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa"
                crossorigin="anonymous"></script>
                <link
                href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"
                rel="stylesheet"
                integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u"
                crossorigin="anonymous">
                </head>
                <body>
                <nav class="navbar navbar-default" role="navigation">
                <div class="container-fluid">
                <ul class="nav navbar-nav navbar-left">
                <li>
	        <h1><a href="/">Catalog App</a></h1>
                </li>
                </ul>

	        <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
      
	        <ul class="nav navbar-nav navbar-right">
                <li><a href="/login"><button class="btn">Login</button></a></li>
	        </ul>
	        </div>
                </div>
                </nav>
    
                <div class="container">
                <div class="row">
	        <div class="col-sm-4">
	        <h2>Categories</h2>
	        <a href="/soccer">Soccer</a>
	        </div>
	        <div class="col-sm-8">
	        <h2>Latest Items</h2>
	        <a href="/soccer/stuff">stuff</a>
	        </div>
                </div>
                </div>
    
                <footer><center><a href="#">Alex Guesnon</a></center></footer>
                </body>
                </html>
                """
                self.wfile.write(output)
                print(output)
                return
            
            if self.path.endswith("/soccer/stuff"):#dynamicly change this to each catagory
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output=""#templet
                output+="""
                <html>
                <head>
                <style>
                .navbar-collapse.collapse {
                display: block!important;
                }

                .navbar-nav>li, .navbar-nav {
                float: left !important;
                }

                .navbar-nav.navbar-right:last-child {
                margin-right: -15px !important;
                }

                .navbar-right {
                float: right!important;
                }
                </style>
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <script
                src="https://code.jquery.com/jquery-3.2.1.js"
                integrity="sha256-DZAnKJ/6XZ9si04Hgrsxu/8s717jcIzLy3oi35EouyE="
                crossorigin="anonymous"></script>
                <script
                src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"
                integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa"
                crossorigin="anonymous"></script>
                <link
                href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"
                rel="stylesheet"
                integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u"
                crossorigin="anonymous">
                </head>
                <body>
                <nav class="navbar navbar-default" role="navigation">
                <div class="container-fluid">
                <ul class="nav navbar-nav navbar-left">
                <li>
	        <h1><a href="/">Catalog App</a></h1>
                </li>
                </ul>

	        <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
      
	        <ul class="nav navbar-nav navbar-right">
                <li><a href="/login"><button class="btn">Login</button></a></li>
	        </ul>
	        </div>
                </div>
                </nav>

                <h2>Stuff</h2>
                <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam ipsum nibh, dictum nec placerat a, tincidunt nec odio. Phasellus velit nunc, luctus vel orci sed, venenatis bibendum sem. Integer et tempor nulla, nec aliquam nunc. In quam erat, varius at suscipit at, pretium ut lacus. Phasellus sagittis, ligula sed pharetra tincidunt, leo ipsum sodales elit, quis sagittis velit diam quis enim. Curabitur viverra lacus et lorem aliquet, sed venenatis felis mattis. Fusce semper erat massa, eu rhoncus eros congue at. Phasellus scelerisque sem vel gravida volutpat. Sed hendrerit elit eu egestas semper. Curabitur feugiat lacinia mi, ac molestie leo tempor posuere. Proin velit nulla, lacinia eget erat sed, ultrices dignissim dolor. Donec convallis nulla in convallis vehicula. Sed laoreet velit leo, id ultrices urna vehicula nec. Integer ultrices nisi vel ex dictum, vel pharetra massa hendrerit. Aliquam felis augue, ornare mattis convallis a, tristique placerat eros. Vivamus lorem quam, lobortis vitae leo vel, ornare tristique odio.</p>
                <footer><center><a href="#">Alex Guesnon</a></center></footer>
                </body>
                </html>
                """
                self.wfile.write(output)
                print(output)
                return

            if self.path.endswith("/login"):#dynamicly change this to each catagory
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output=""#templet
                output+="""
                <html>
                <head>
                <style>
                .navbar-collapse.collapse {
                display: block!important;
                }
                
                .navbar-nav>li, .navbar-nav {
                float: left !important;
                }
                
                .navbar-nav.navbar-right:last-child {
                margin-right: -15px !important;
                }
                
                .navbar-right {
                float: right!important;
                }
                </style>
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <script
                src="https://code.jquery.com/jquery-3.2.1.js"
                integrity="sha256-DZAnKJ/6XZ9si04Hgrsxu/8s717jcIzLy3oi35EouyE="
                crossorigin="anonymous"></script>
                <script
                src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"
                integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa"
                crossorigin="anonymous"></script>
                <link
                href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"
                rel="stylesheet"
                integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u"
                crossorigin="anonymous">
                </head>
                <body>
                <nav class="navbar navbar-default" role="navigation">
                <div class="container-fluid">
                <ul class="nav navbar-nav navbar-left">
                <li>
	        <h1><a href="/">Catalog App</a></h1>
                </li>
                </ul>
                
	        <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
      
	        <ul class="nav navbar-nav navbar-right">
                <li><a href="/login"><button class="btn">Login</button></a></li>
	        </ul>
	        </div>
                </div>
                </nav>

                <h2>LOGIN</h2>
                putin oath google and facebook

                </body>
                </html>
                """
                
                self.wfile.write(output)
                print(output)
                return           
            
        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/somethingelse"):
                print("post a test")
            
        except Exception:
            pass


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
