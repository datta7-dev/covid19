from django.db import models

# Create your models here.


class Global(models.Model):
    TotalConfirmed = models.BigIntegerField()
    TotalDeaths = models.BigIntegerField()
    TotalRecovered = models.BigIntegerField()
    date = models.DateField(primary_key=True)

    def __int__(self):
        return self.date


class CountryData(models.Model):
    CountryCode = models.CharField(max_length=20, primary_key=True)
    Country = models.CharField(max_length=64)
    NewConfirmed = models.BigIntegerField()
    TotalConfirmed = models.BigIntegerField()
    NewDeaths = models.BigIntegerField()
    TotalDeaths = models.BigIntegerField()
    NewRecovered = models.BigIntegerField()
    TotalRecovered = models.BigIntegerField()
    date = models.DateField()

    def __str__(self):
        return self.CountryCode


class India(models.Model):
    TotalConfirmed = models.BigIntegerField()
    TotalDeaths = models.BigIntegerField()
    TotalRecovered = models.BigIntegerField()
    date = models.DateField(primary_key=True)

    def __int__(self):
        return self.date


class IndiaRegion(models.Model):
    Region = models.CharField(max_length=50)
    NewConfirmed = models.BigIntegerField()
    TotalConfirmed = models.BigIntegerField()
    NewDeaths = models.BigIntegerField()
    TotalDeaths = models.BigIntegerField()
    NewRecovered = models.BigIntegerField()
    TotalRecovered = models.BigIntegerField()
    date = models.DateField()

    def __str__(self):
        return self.Region
