# EPIC EVENT
 

## Table of Contents
1. [General Info](#general-info)
2. [Technologies](#technologies)
3. [Installation](#installation)
5. [API endpoints](#API-endpoints-and-documentation)

## General Info
***
Epic Event is a consulting and management company in the event industry. It helps start-ups in the creation of epic parties.

Epic Event API is the CRM of the company.
The CRM system is the command center for the management of business processes for all actors involved, so that everyone has the information they need.

## Technologies
***

* [Python](https://www.python.org/): Version 3.9.2 
* [django](https://www.djangoproject.com/): Version 3.2.9
* [djangoRest framework](https://www.django-rest-framework.org/): Version 3.12.4
* [djangoRest framework-simplejwt](https://django-rest-framework-simplejwt.readthedocs.io/): Version 5.0.0
* [PostgreSQL](https://www.postgresql.org/): Version 14

## Installation
***
### PostgreSQL
First let's see how install PostgreSQL database locally:

1. Download and install [PostgreSQL](https://www.postgresql.org/) in your system
2. Create a new database (you can use [pgadmin4](https://www.pgadmin.org/)):
   * name : epic_event
   * host : localhost
   * port : 5432
   * user : User of your choice configured in postgresql
   * password: password of the user


We will see later how to configure PostgreSQL in django.

### Project

1. Clone Git repository <https://github.com/dardevetdidier/EpicEvent.git>
2. Create and activate a virtual environment in your project directory:

`$ cd your/project/directory`\
`$ python -m venv venv`\
`$ source venv/Script/activate`
3. Install required packages : `$ pip install -r requirements.txt`


4. Create a file '.env' at the root of the project.\
This file will contain the sensitive data of django settings.


5. Open '.env' file and replace example values with right ones without quotes:

   * SECRET_KEY=ThedjangosecretKey
   * DB_USER=Your user configured in PostgreSQL
   * DB_PASSWORD=Your password configured in PostgreSQL
   

6. Apply migrations:\
The project contains a custom migration that creates groups used for permissions.
To apply this migration enter the following:\
`$ python manage.py migrate 0007 && python manage.py migrate`


7. Create admin user:\
`$ python manage.py createsuperuser`


8. Run the server with `$ python manage.py runserver`

Admin user can now access admin interface in a browser with <http://127.0.0.1:8000/admin/>


## API endpoints and documentation

Sales and support Team members can access CRUD operations with endpoints available on Postman documentation. It describes the 
complete use of the API:
<https://documenter.getpostman.com/view/16247859/UVJeEG8A>


