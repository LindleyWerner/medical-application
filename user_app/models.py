from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


# Create your models here.
class Funcionalidades(models.Model):
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

class Custom_user(models.Model):
    django_user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    is_doctor = models.BooleanField(default=False)
    is_nurse = models.BooleanField(default=False)
    is_pharmacy = models.BooleanField(default=False)
    is_adm = models.BooleanField(default=False)
    is_user = models.BooleanField(default=False)
    #password_tryed = models.IntegerField(default=0)

    def __str__(self):
        if self.is_user:
            return "User" + ': ' + self.django_user.first_name + ' ('+ self.django_user.username + ')'
        elif self.is_nurse:
            return "Nurse" + ': ' + self.django_user.first_name + ' ('+ self.django_user.username + ')'
        elif self.is_pharmacy:
            return "Pharmacy" + ': ' + self.django_user.first_name + ' ('+ self.django_user.username + ')'
        elif self.is_doctor:
            return "Doctor" + ': ' + self.django_user.first_name + ' ('+ self.django_user.username + ')'
        elif self.is_adm:
            return "Adm" + ': ' + self.django_user.first_name + ' ('+ self.django_user.username + ')'
        else:
            return None