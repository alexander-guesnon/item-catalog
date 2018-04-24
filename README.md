# Log-Analysis
This is a Python program I created to parse website logs. It's using the Flask and SQLalchemy libraries and this program was running on an Ubuntu VM.
## Outline
 * Create a python program to display the following information.
  * Show the top 3 articles in the database
  * Show the top authors in the database
  * Show the days where the errors resulting from page requests were more than 1%
 * Use PostgreSQL in order to perform the queries
## Execution

### Requirements
* Python 2.7 - newer
* PostgreSQL 9.5 - newer

### Running
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


## License
Log-Analysis is distributed under the GPLv3 license.
