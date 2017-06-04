from django.db import models
from django.conf import settings

# Create your models here.
class Funcionalidade(models.Model):
    name = models.CharField(max_length=30)
    logo = models.FileField()
    url = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class Adm_user(models.Model):
    django_user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    full_name = models.CharField(max_length=70)
    cnpj = models.CharField(max_length=18)
    address = models.CharField(max_length=70)
    phones = models.CharField(max_length=30)
    site = models.CharField(max_length=50, default="")
    adm_father = models.IntegerField(default=1);
    password_tryed = models.IntegerField(default=0)

    def __str__(self):
        return "Adm" + ': ' + self.full_name + ' ('+ self.django_user.username + ')'


class Pending_adm(models.Model):
    validation_code = models.CharField(max_length=50)
    cnpj = models.CharField(max_length=18)
    email = models.EmailField(max_length=50, unique=True)
    adm_father = models.IntegerField(default=-1);

    def __str__(self):
        return "Adm" + ': ' + self.email


class Pending_doctor(models.Model):
    validation_code = models.CharField(max_length=50)
    crm = models.CharField(max_length=15)
    email = models.EmailField(max_length=50, unique=True)
    adm_father = models.IntegerField(default=-1);

    def __str__(self):
        return "Doctor" + ': ' + self.email