import requests

from django.db import IntegrityError
from django.core.management.base import BaseCommand
from django.conf import settings

from api_data.models import Hotel, City


class Command(BaseCommand):
    help = 'Fetches data from external API and saves to database'

    def handle(self, *args, **kwargs):
        """
        Fetch the cities and hotel data from the external API and store it in Django models
        """

        cities_read_count, cities_added_count = self.fetch_cities()
        print(f"Total cities received from API data {cities_read_count}, total new added {cities_added_count}")

        hotels_read_count, hotels_added_count = self.fetch_hotels()
        print(f"Total hotels received from API data {hotels_read_count}, total new added {hotels_added_count}")


    def fetch_cities(self):
        """
        Make an API request for the city data, and store the cities in Django models.
        If a city with that ID already exist, the object is only updated if relevant.

        Returns:
            cities_read_count (int): The number of cities that were read from the API data
            cities_added_count (int): The number of cities that were actually created or updated (assuming that most cities
            already exist in the Django models)
        """

        # Get the API urls, username and password from the env vars (through settings)
        api_url = settings.API_CITY_URL
        username = settings.API_USERNAME
        password = settings.API_PASSWORD

        try:
            response = requests.get(api_url, auth=requests.auth.HTTPBasicAuth(username, password))

            if response.status_code == 200:
                lines = response.text.strip().split('\n')

                cities_read_count = 0
                cities_added_count = 0
                for line in lines:
                    parts = line.split(';')

                    if len(parts) == 2:  # Make sure there is text before and after the ';'
                        # TODO: I am assuming the first item in the data (for example 'AMS' for 'Amsterdam') is a unique
                        #  identifier of the city. Verify with the API documentation that this is indeed the case
                        city_id = parts[0].strip()
                        city_name = parts[1].strip()

                        # Remove the quotation marks from the strings (they come in as '"Amsterdam"')
                        city_id = city_id.replace('"', '')
                        city_name = city_name.replace('"', '')

                        cities_read_count += 1
                        city, created = City.objects.update_or_create(
                            id=city_id,
                            defaults={
                                'name': city_name,
                            }
                        )
                        city.save()
                        if created:
                            cities_added_count += 1

                    # TODO: raise an error if the API data structure is not as expected

                return cities_read_count, cities_added_count

        except requests.RequestException as e:
            self.stdout.write(
                self.style.ERROR(f'Error fetching data: {str(e)}')
            )


    def fetch_hotels(self):
        """
        Make an API request for the hotel data, and store the hotels in Django models.
        The city that the hotel is located in is queried from the Django models, to create the correct Foreign Key.
        If a hotel with that ID already exists, the object is only updated if relevant.

        Returns:
            hotels_read_count (int): The number of hotels that were read from the API data
            hotels_added_count (int): The number of hotels that were actually created or updated (assuming that most hotels
            already exist in the Django models)
        """

        # Get the API urls, username and password from the env vars (through settings)
        api_url = settings.API_HOTEL_URL
        username = settings.API_USERNAME
        password = settings.API_PASSWORD

        try:
            response = requests.get(api_url, auth=requests.auth.HTTPBasicAuth(username, password))

            if response.status_code == 200:
                lines = response.text.strip().split('\n')

                hotels_read_count = 0
                hotels_added_count = 0
                for line in lines:
                    parts = line.split(';')

                    if len(parts) == 3:  # Make sure there is text before and after the ';'
                        # TODO: I am assuming the first item in the data (for example 'AMS001' for an hotel in Amsterdam)
                        #  is a unique identifier of the city. Verify with the API documentation that this is indeed the case
                        hotel_city_id = parts[0].strip()
                        hotel_id = parts[1].strip()
                        hotel_name = parts[2].strip()

                        # Remove the quotation marks from the strings (they come in as '"Amsterdam"')
                        hotel_city_id = hotel_city_id.replace('"', '').replace("'", '')
                        hotel_id = hotel_id.replace('"', '').replace("'", '')
                        hotel_name = hotel_name.replace('"', '').replace("'", '')

                        city = City.objects.get(id=hotel_city_id)

                        # TODO: raise an error for if no city is found

                        hotels_read_count +=1

                        try:
                            hotel, created = Hotel.objects.update_or_create(
                                id=hotel_id,
                                defaults={
                                    'name': hotel_name,
                                    'city': city
                                }
                            )
                            city.save()
                            if created:
                                hotels_added_count += 1

                        except IntegrityError as e:
                            self.stdout.write(
                                self.style.WARNING(f'Error for hotel with ID {hotel_id} and name {hotel_name} in {city.name}: {str(e)}')
                            )

                    # TODO: raise an error if the API data structure is not as expected

                return hotels_read_count, hotels_added_count

        except requests.RequestException as e:
            self.stdout.write(
                self.style.ERROR(f'Error fetching data: {str(e)}')
            )
