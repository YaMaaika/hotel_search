from django.db import models


class City(models.Model):
    id = models.CharField(primary_key=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "City"


class Hotel(models.Model):
    id = models.CharField(primary_key=True, max_length=5)
    name = models.CharField(max_length=200)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Hotel"

