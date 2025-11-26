from django.test import TestCase
from django.db import IntegrityError

from api_data.models import Hotel, City


class CityModelTest(TestCase):
    """Test the City model"""

    def setUp(self):
        """Set up test data"""
        self.city = City.objects.create(
            id="DMN",
            name="Diemen"
        )

    def test_city_creation(self):
        """Check that creating a City object works"""
        city = City.objects.create(id="UTR", name="Utrecht")
        self.assertEqual(city.id, "UTR")
        self.assertEqual(city.name, "Utrecht")


    def test_city_id_is_unique(self):
        """Test that city ID must be unique (it has a primary key constraint)"""
        City.objects.create(id="ZND", name="Zaandam")

        with self.assertRaises(IntegrityError):
            City.objects.create(id="ZND", name="Zaandam 1")


    def test_city_name_can_be_duplicate(self):
        """
        Test that city names can be duplicated (different ids)
        It is intentional that different cities with the same name can exist,
        as this is often the case (for example, there are multiple 'Melbourne' cities).
        We might want to change this behavior in the future,
        for example add a country field and require that the combination of country and city name is unique
        """
        City.objects.create(id="DNH", name="Den Haag")
        City.objects.create(id="DEN", name="Den Haag")

        self.assertEqual(City.objects.filter(name="Den Haag").count(), 2)


class HotelModelTest(TestCase):
    """Test the Hotel model"""

    def setUp(self):
        """Set up test data"""
        self.city = City.objects.create(id="DMN", name="Diemen")
        self.hotel = Hotel.objects.create(
            id="DMN001",
            name="Diemen Gasthuis",
            city=self.city
        )


    def test_hotel_creation(self):
        """Test that a hotel can be created with correct attributes"""
        self.assertEqual(self.hotel.id, "DMN001")
        self.assertEqual(self.hotel.name, "Diemen Gasthuis")
        self.assertEqual(self.hotel.city, self.city)
        self.assertIsInstance(self.hotel, Hotel)


    def test_hotel_id_is_unique(self):
        """Test that hotel id must be unique (primary key constraint)"""
        with self.assertRaises(IntegrityError):
            Hotel.objects.create(
                id="DMN001",
                name="Another Hotel",
                city=self.city
            )

    def test_cascade_delete(self):
        """Make sure hotels are deleted when city is deleted"""
        self.city = City.objects.create(id="HZN", name="Huizen")

        Hotel.objects.create(id="HZN001", name="Hotel", city=self.city)
        Hotel.objects.create(id="HZN002", name="Hotel 2", city=self.city)

        self.assertEqual(Hotel.objects.filter(city__id="HZN").count(), 2)

        self.city.delete()

        # Verify all hotels in the specific city were deleted
        self.assertEqual(Hotel.objects.filter(city__id="HZN").count(), 0)


    def test_hotel_requires_city(self):
        """Hotel must have a city"""
        with self.assertRaises(IntegrityError):
            Hotel.objects.create(id="XXX001", name="Hotel", city=None)


    def test_hotel_city_relationship(self):
        """Verify foreign key relationship works"""
        hotel = Hotel.objects.create(
            id="DMN003",
            name="Grand Hotel Diemen",
            city=self.city
        )

        self.assertEqual(hotel.city.id, "DMN")
        self.assertEqual(hotel.city.name, "Diemen")


    def test_filter_hotels_by_city(self):
        """Check that hotels can be searched through city"""
        Hotel.objects.create(id="DMN002", name="Hotel 1", city=self.city)
        Hotel.objects.create(id="DMN003", name="Hotel 2", city=self.city)

        utrecht = City.objects.create(id="UTR", name="Utrecht")
        Hotel.objects.create(id="UTR001", name="Utrecht Hotel", city=utrecht)

        diemen_hotels = Hotel.objects.filter(city=self.city)
        self.assertEqual(diemen_hotels.count(), 3)

        utrecht_hotels = Hotel.objects.filter(city=utrecht)
        self.assertEqual(diemen_hotels.count(), 3)