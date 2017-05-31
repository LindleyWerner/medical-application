from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


# Create your models here.
class Funcionalidade(models.Model):
    name = models.CharField(max_length=30)
    logo = models.FileField()
    url = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    user = models.ForeignKey(User, default=1)
    doctor = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    pub_date = models.DateTimeField('Date published')
    place = models.CharField(max_length=100)

    def __str__(self):
        return self.doctor + ': ' + str(self.pub_date)


class Simple_user(models.Model):
    django_user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    full_name = models.CharField(max_length=70)
    birth_date = models.CharField(max_length=10)
    gender = models.CharField(max_length=10)
    address = models.CharField(max_length=70)
    phones = models.CharField(max_length=30)
    password_tryed = models.IntegerField(default=0)

    def __str__(self):
        return "User" + ': ' + self.django_user.first_name + ' (' + self.django_user.username + ')'
