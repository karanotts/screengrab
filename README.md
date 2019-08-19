# screengrab
https://screengrab-app.herokuapp.com/

Simple web application to request screenshots of pages from thum.io and provide API access to all stored items.

## API Documentation
Available at https://screengrab-app.herokuapp.com/api/v1/


## Installation

If you want to test the app locally, clone this repo to your local machine, provide environmental variables:
```.env
SECRET_KEY=12345ABCDE
FLASK_APP=screengrab
```
```.env-mysql
MYSQL_RANDOM_ROOT_PASSWORD=yes
MYSQL_DATABASE=sqldb
MYSQL_USER=sqluser
MYSQL_PASSWORD=sqlpassword
```
Once that is done, run  
`docker-compose build`  
`docker-compose up`  

The app will become accessible at http://localhost:80

To change the default localshot port, modify `docker-compose.yml` (host-port:container-port):
```
ports:
      - "80:5000"
```

## Testing

Testing is done using unittest, test files are located in /screengrab/tests.  
Simply run `python -m unittest` and see the results.  

`FlaskBasicTestCase` tests app setup and teardown and database model.  
`FlaskViewsTest` tests views and item creation.
  
### EXAMPLE TEST:
```
    response = self.client.post(
        '/api/v1/screenshots',
        content_type='application/json',
        data=json.dumps({'source_url': 'https://malformed-url'}))
        self.assertEqual(response.status_code, 500)
```
```
$ python -m unittest
(...)
"Failed to establish connection to {}".format(source_url)
Exception: Failed to establish connection to https://malformed-url
..
----------------------------------------------------------------------
Ran 5 tests in 2.966s

OK
```

Database query tests can be done using /screengrab/commands.py  
`flask test_query`
You can add and test your queries by following the pattern:  
```
@click.command(name='custom_query')
@with_appcontext
def custom_query():
    db_query = db.session.query(Screenshot).all()

    print("Query results:" , db_query)
```

# TODO
- work on mobile view, it's not responsive at the moment
- modify tests to dev to pass Travis tests
- set up Travis > Elasticbeanstalk pipeline