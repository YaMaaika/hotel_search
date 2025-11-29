from django.db import models


class City(models.Model):
    # 'id' is a three-letter code (for example 'AMS' for Amsterdam), present with the API data
    # TODO: add max length=3 for city id?
    id = models.CharField(primary_key=True)
    # I intentially did not make the city name unique, since there can be multiple cities with the same name (i.e. 'Melbourne')
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "City"


class Hotel(models.Model):
    # 'id' is typically a string with the city code followed by a number, i.e 'AMS001', present on the API data
    id = models.CharField(primary_key=True, max_length=5)
    name = models.CharField(max_length=200)
    # The Hotel is linked to the City model through the 'city' foreign key
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Hotel"

