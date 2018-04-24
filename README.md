# Item-Catalog

This is a project I made to deal with an AWS web application product database. The server will send out Flask HTML templets,  which are styled with CSS and Bootstrap, which allow users to submit POST requests to the servers via an HTML form. The server will take the user's data and manipulate the PSQL database as needed, using SQLachemy and Python. The SQL database is also accessible through the API and will return the data in a JSON format.


## Outline
* The application needs be able to do the following to a database:
  * Read
  * Create
  * Update
  * Delete
  
* The application needs to be able to login to an account using OAuth.
* The application needs to have JSON API endpoint.

## Execution

### Requirements
* Python 2.7 - newer

### Running

Launch a terminal in the Udacity-Item-Catalog directory. Then run the following.
```
python catalog-app.py
```
Then Launch a web browser and type the following
```
http://localhost:8080/
```
## API
In a web browser type the following to get a JSON file that will contain the entire database.
```
http://localhost:8080/api/v1/catalog.json
```
In a web browser type the following to get a JSON file that will contain the specified category given.
```
http://localhost:8080/api/v1/query/(Catagory).json
```
In a web browser type the following to get a JSON file that will contain the specified item given.
```
http://localhost:8080/api/v1/query/(Catagory)/(Item).json
```

## License
Item-Catalog is distributed under the GPLv3 license.
