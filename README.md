# d
d for django

## Run server

`python manange.py runserver`

check out urls.py for the urls.

admin username: admin

admin password: navaneethan

## TO DO Before run the app:
in your _/etc/hosts_ file add an entry

`
127.0.0.1    test1.com
`

## Rest usage:

### GET all the accounts:

`curl 'http://localhost:8000/rest/api/v1/accounts/' -H "Content-Type: application/json" -X GET`

### Create New Account:


`curl 'http://localhost:8000/rest/api/v1/accounts/' -H "Content-Type: application/json" -X POST --data '{"user_name": "nava", "password": "nava123", "email": "rest@gmail.com", "first_name": "f", "last_name":"t", "mobile_no":"1234"}' -vv`

### Dependencies:
1. django-recaptcha
[https://github.com/praekelt/django-recaptcha#installation]
2. pip install python-social-auth


