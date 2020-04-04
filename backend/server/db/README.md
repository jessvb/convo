# Database
This directory contains the database files for Convo

## Local
To create a database for local development, open up an interactive Python shell in `server` directory and run
```python
from db_manage import db
db.create_all()
```

This will create a SQLite3 database `convo.db` in `db` which you can access if you have `sqlite3` installed.
If you want to install SQLite3 check the [guide](https://www.tutorialspoint.com/sqlite/sqlite_installation.htm).
