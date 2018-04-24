<<<<<<< HEAD
# Log-Analysis
This is a Python program I created to parse website logs. It's using the Flask and SQLalchemy libraries and this program was running on an Ubuntu VM.
=======
# Udacity-Item-Catalog

This is a project I did for the Udacity backend module

>>>>>>> parent of 150040d... Update README.md
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
<<<<<<< HEAD
First, download the newsdata.sql file and put it into the log-analysis directory.

[newsdata.sql](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)

Run the following command when first installed.
~~~
sql -d news -f newsdata.sql
~~~
After the database is loaded you can run the following.
~~~
python DB-analysis-tool.py
~~~
If you want to reset the database run the following commands.
~~~
echo 'drop table log; drop table articles; drop table authors;' | psql news
sql -d news -f newsdata.sql
~~~

=======
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
>>>>>>> parent of 150040d... Update README.md

## License
Udacity-Item-Catalog is distributed under the GPLv3 license.
