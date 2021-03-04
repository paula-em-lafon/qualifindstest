# Versioning control app #

## A small briefing ##

this repository contains two versions of the same app. They both have the exact same features but version 2 implements more hashing in order to increase performance. For instance instead of looking through all the different attributes to find out if a key exists it only need look for the key. At the moment of retrieval the key is found instantaneously instead of having to go through all the different entries. Some tradeoffs had to be made in order to have a cohesive data structure, but in general version 2 should be faster than version one.

## Running the app ##

To run version 1 one needs to type the following two commands:

    $ export FLASK_APP=app.py
    $ flask run

In order to run version 2 one only need type the same commands but with `app2.py`

    $ export FLASK_APP=app2.py
    $ flask run

Postman is recommended to run tests on the running apps. The data will not be persisted between server restarts which can be achived with databases, Redis or sessions. implementing these would be a feature I would implement on a future iteration of this app.

To make a `PUT` request make the request to `http://127.0.0.1/api/v1` with a body resembling the following:

    {
        "key": "whateverKey",
        "value": 300
    }

To make a `GET` request make the request to the same endpoint as before with a body resembling one of the following:

    {
        "key": "superImportantKey",
        "version": 7
    }

or:

    {
        "key": "superImportantKey"
    }

## Testing ##

in order to run the tests on version one run the following command:

    $ python -m unittest discover -p tests.py

and in order to run the tests on version two run the following

    $ python -m unittest discover -p tests2.py