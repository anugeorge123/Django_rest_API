from django.db import models
from django.contrib.auth.models import AbstractUser

class Country(models.Model):
    countryName = models.CharField(max_length=30)

    def __str__(self):
        return self.countryName

    class Meta:
        verbose_name_plural = ('Country')


class State(models.Model):
    stateName = models.CharField(max_length=30)
    countryName = models.ForeignKey(Country,on_delete=models.CASCADE)

    def __str__(self):
        return self.stateName

    class Meta:
        verbose_name_plural = ('State')


class City(models.Model):
    cityName  = models.CharField(max_length=30)
    stateName = models.ForeignKey(State,on_delete=models.CASCADE)

    def __str__(self):
        return self.cityName

    class Meta:
        verbose_name_plural = ('City')


class TimeStampModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class User(AbstractUser,TimeStampModel):
    userImage = models.FileField(upload_to='images/', max_length=254)
    phone = models.CharField(max_length = 12)
    countryName = models.ForeignKey(Country,on_delete=models.CASCADE)
    stateName = models.ForeignKey(State,on_delete=models.CASCADE)
    cityName = models.ForeignKey(City,on_delete=models.CASCADE)
    otp = models.CharField(max_length=255, null=True, blank=True)
    rp_otp = models.CharField(max_length=255, null=True, blank=True)
