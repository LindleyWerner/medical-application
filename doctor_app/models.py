from django.db import models
from django.conf import settings

# Create your models here.
class Funcionalidade(models.Model):
    name = models.CharField(max_length=30)
    logo = models.FileField()
    url = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Doctor_user(models.Model):
    django_user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    full_name = models.CharField(max_length=70)
    birth_date = models.CharField(max_length=10)
    gender = models.CharField(max_length=10)
    crm = models.CharField(max_length=15)
    address = models.CharField(max_length=70)
    phones = models.CharField(max_length=30)
    adm_father = models.IntegerField(default=1);
    password_tryed = models.IntegerField(default=0)

    def __str__(self):
        return "Doctor" + ': ' + self.django_user.first_name + ' ('+ self.django_user.username + ')'