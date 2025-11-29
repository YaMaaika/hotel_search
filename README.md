# Hotel Data search

In this project hotel data is shown in a Django app

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
```commandline
API_USERNAME='my_username'
API_PASSWORD='my_password'
API_CITY_URL='api_city_url'
API_HOTEL_URL='api_hotel_url'
```

To run the script, run:
```commandline
python manage.py fetch_api_data
```

### Cronjob for automating daily data import

Since the API data is daily updated, you might want to automate the API data fetching as well.

The project includes a script that adds a cronjob that accomplishes this daily update at 2AM at night.

1. Open your terminal.
2. Navigate to the project directory (where `daily_update.sh` is located).
3. Make the script executable:
    ```bash
    chmod +x daily_update.sh
    ```
4. Run the script:
    ```bash
    ./daily_update.sh
    ```
5. To confirm that the cron job was added successfully, you can check your current cron jobs with:
    ```bash
    crontab -l
    ```
The cronjob logs its results to the logile.log that should appear at the root of the project once the cronjob has run once.


### Running the server

Now it is time to run the webserver and see the hotel data in the browser.

To run the server:
```commandline
python manage.py runserver
```

Navigate to `http://127.0.0.1:8000/hotel_search/`

Search for a city to get hotels in that city

### Running unit tests

To run all of the unit tests, run:
```commandline
python3 manage.py test api_data.tests
```
Or for a specific file:
```commandline
python3 manage.py test api_data.tests.testModels
```