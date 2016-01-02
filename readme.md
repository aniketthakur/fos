### fos webapp.

#### install webapp locally.
```
$ sudo apt-get install mongodb python-dev zlib1g-dev libxml2-dev libxslt1-dev
$ pip install -r requirements.txt
```

#### db helpers.
```
#initialize
$ python manage.py initdb

# dropdb
$ python manage.py dropdb
```

#### run locally.
```
$ python manage.py runserver
```