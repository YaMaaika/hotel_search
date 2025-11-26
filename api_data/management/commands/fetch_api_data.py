import requests

from django.core.management.base import BaseCommand

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


    def fetch_cities(self, *args, **kwargs):
        """
        Make an API request for the city data, and store the cities in Django models.
        If a city with that ID already exist, the object is only updated if relevant.

        Returns:
            count (int): The number of cities that were created or updated
        """
        api_url = ''        # Im not adding the url as Im not sure I can publish it
        # TODO: store the username and password in an env var and make an authenticated HTTP request
        # for now it also works without authentication
        username = ''
        password = ''

        try:
            #response = requests.get(api_url, auth=HTTPBasicAuth(username, password))
            response = requests.get(api_url)

            if response.status_code == 200:
                lines = response.text.strip().split('\n')

                cities_read_count = 0
                cities_added_count = 0
                for line in lines:
                    parts = line.split(';')

                    if len(parts) == 2:  # Make sure there is text before and after the ';'
                        city_id = parts[0].strip()
                        city_name = parts[1].strip()
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

            return cities_read_count, cities_added_count

        except requests.RequestException as e:
            self.stdout.write(
                self.style.ERROR(f'Error fetching data: {str(e)}')
            )


    def fetch_hotels(self, *args, **kwargs):
        """
        Make an API request for the hotel data, and store the hotels in Django models.
        The city that the hotel is located in is queried from the Django models, to create the correct Foreign Key.
        If a hotel with that ID already exists, the object is only updated if relevant.

        Returns:
            count (int): The number of hotels that were created or updated
        """
        api_url = ''        # Im not adding the url as Im not sure I can publish it
        # TODO: store the username and password in an env var and make an authenticated HTTP request
        # for now it also works without authentication
        username = ''
        password = ''

        try:
            # response = requests.get(api_url, auth=HTTPBasicAuth(username, password))
            response = requests.get(api_url)

            if response.status_code == 200:
                lines = response.text.strip().split('\n')

                hotels_read_count = 0
                hotels_added_count = 0
                for line in lines:
                    parts = line.split(';')

                    if len(parts) == 3:  # Make sure there is text before and after the ';'
                        hotel_city_id = parts[0].strip()
                        hotel_id = parts[1].strip()
                        hotel_name = parts[2].strip()

                        city = City.objects.get(id=hotel_city_id)

                        hotels_read_count +=1

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

            return hotels_read_count, hotels_added_count


        except requests.RequestException as e:
            self.stdout.write(
                self.style.ERROR(f'Error fetching data: {str(e)}')
            )
