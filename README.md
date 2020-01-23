# Django-Discussion-Forum
This is a web application developed on Django Framework that enables the user to deploy a simple discussion forum

## Getting started
The instructions below will help you get a copy of the project up and running on your local machine for development and testing purpose.

## Prerequisites
- Python installed
- Django installed
- Pycharm or other IDE

## Installing
### 1. Database setup
Firstly, Pull and open the project with your IDE.
In your terminal windows, create an admin/ superuser account with the following command:

```
python manage.py createsuperuser
```

Secondly, migrate the database with the following commands:
```
python manage.py migrate

python manage.py makemigrations myForum

python manage.py migrate
```

Lastly, start your server with the following command:

```
python manage.py runserver
```
Your local web app will be up and running on port 8000.

### 2. Setup the forum
Firstly, access the admin page with the following syntax:
> {{website url}}/admin

Setup the forum:
- Major section
- Minor/ sub section

```
Your simple discussion forum has been completed and up for running.
You can now create a user account to post a new topic or comment in topic that you like.
```

Have a look at the demo here: http://jamessly.pythonanywhere.com/
