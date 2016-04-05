# d
d for django

## Run server

`python manange.py runserver`

check out urls.py for the urls.

admin username: admin

admin password: navaneethan


## Rest usage:

### GET all the accounts:

`curl 'http://localhost:8000/rest/api/v1/accounts/' -H "Content-Type: application/json" -X GET`

### Create New Account:


`curl 'http://localhost:8000/rest/api/v1/accounts/' -H "Content-Type: application/json" -X POST --data '{"user_name": "nava", "password": "nava123", "email": "rest@gmail.com", "first_name": "f", "last_name":"t", "mobile_no":"1234"}' -vv`

### Dependencies:
_django-recaptcha_
[https://github.com/praekelt/django-recaptcha#installation]


