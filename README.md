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

### Running unit tests

To run all of the unit tests, run:
```commandline
python3 manage.py test api_data.tests
```
Or for a specific file:
```commandline
python3 manage.py test api_data.tests.testModels
```