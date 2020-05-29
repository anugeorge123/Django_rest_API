from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext as _

class Country(models.Model):
    countryName = models.CharField(max_length=30,null=True, blank=True)

    def __str__(self):
        return self.countryName

    class Meta:
        verbose_name_plural = ('Country')


class State(models.Model):
    stateName = models.CharField(max_length=30,null=True, blank=True)
    countryName = models.ForeignKey(Country,on_delete=models.CASCADE,)

    def __str__(self):
        return self.stateName

    class Meta:
        verbose_name_plural = ('State')


class City(models.Model):
    cityName  = models.CharField(max_length=30,null=True, blank=True)
    stateName = models.ForeignKey(State,on_delete=models.CASCADE)

    def __str__(self):
        return self.cityName

    class Meta:
        verbose_name_plural = ('City')


class TimeStampModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class UserRole(models.Model):
    role = models.CharField(max_length = 30,null=True, blank=True)

    def __str__(self):
        return self.role

    class Meta:
        verbose_name_plural = ('User Role')


class User(AbstractUser,TimeStampModel):
    userImage = models.FileField(upload_to='images/', max_length=254,null=True, blank=True)
    phone = models.CharField(max_length = 12)
    countryName = models.ForeignKey(Country,on_delete=models.CASCADE,null=True, blank=True)
    stateName = models.ForeignKey(State,on_delete=models.CASCADE,null=True, blank=True)
    cityName = models.ForeignKey(City,on_delete=models.CASCADE,null=True, blank=True)
    otp = models.CharField(max_length=255, null=True, blank=True)
    rp_otp = models.CharField(max_length=255, null=True, blank=True)
    email_verified =  models.BooleanField(_('Email verified'), default=False)
    signup_method = models.CharField(max_length=255,null=True, blank=True)
    role = models.ForeignKey(UserRole,on_delete=models.CASCADE,null=True, blank=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = ('User')
