# Hotel Data search

In this project hotel data is fetched daily from an API and shown to the user.
The user can search for a certain city and get a list of hotels in that city.

This is a Django project, and the API data is stored in Django models.
When the hotel and city data comes in from the API it is not linked to each other, this is done when the data is imported into Django models.

The project includes also a cronjob that schedules a daily fetching of the API data.

The project works for now with an SQLLite db to store the data.


## Running and viewing the project


### Project requirements

This project runs on Python 3.
It assumes that the `python` command in your terminal corresponds to Python 3.


### Setting up a Virtual Environment and installing requirements

To start the project, it is good practice (but not required) to create a virtual environment,
so that all required packages for the project can be installed within that virtual environment.

Within the root of the project, create a virtual environment and activate it:
```commandline
python -m venv venv
source venv/bin/activate
```

Now install all the required packages, as listed in requirements.txt
```commandline
pip install -r requirements.txt
```

### Importing API data

Next, you will want to import the Hotel data from the external API.

There is the `fetch_api_data.py` script that accomplishes this.
It fetches the API data from the external API and imports it to Django models,
thereby creating the relation between Hotel and City (a Hotel is situated in a certain City).

#### Get the API url, username and password the env

Since the API url, username and password for the API are sensitive, they are not added in the normal code base.
Instead you should add them in an `.env` file at the root of your project.

The `.env` file should look like this:
```
API_USERNAME='my_username'
API_PASSWORD='my_password'
API_CITY_URL='api_city_url'
API_HOTEL_URL='api_hotel_url'
```

#### Run migrations for DB tables

Now, run migrations to get the DB tables:
```commandline
python manage.py migrate
```

Then run the `fetch_api_data.py` script, run:
```commandline
python manage.py fetch_api_data
```

You might see a lot of warnings printed about multiple hotels with the same name and city, this is a known issue.

### Running the server

Now it is time to run the webserver and see the hotel data in the browser.

To run the server:
```commandline
python manage.py runserver
```

Navigate to `http://127.0.0.1:8000/hotel_search/`

Search for a city to get hotels in that city


## Development

If you want to continue development on this project, there are a few things to note.

### Running unit tests

To run all of the unit tests, run:
```commandline
python3 manage.py test api_data.tests
```
Or for a specific file:
```commandline
python3 manage.py test api_data.tests.testModels
```

### Adding new packages

Make sure that any new packages you install are listed in the `requirements.txt` file,
so that it is clear for everyone what needs to be installed.

In order to 'freeze' (list) all the packages you have installed into the requirements.txt file, run:
```commandline
pip freeze > requirements.txt
```

### Making changes to the Django models

It can be the case that you want to make changes to the Django models.
In case you do, you'll need to run migrations to update the database.

In order to make a migration file, run:
```commandline
python manage.py makemigrations
```
Check the migration file and its name, and change the name (but not the number it starts with) if it would make the change clearer.

Now run the migrations
```commandline
python manage.py migrate
```
