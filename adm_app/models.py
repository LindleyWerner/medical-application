from django.db import models
from django.conf import settings

# Create your models here.
class Funcionalidade(models.Model):
    name = models.CharField(max_length=30)
    logo = models.FileField()
    url = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Adm_user(models.Model):
    django_user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    validation_code = models.CharField(max_length=50)
    full_name = models.CharField(max_length=70)
    cnpj = models.CharField(max_length=18)
    address = models.CharField(max_length=70)
    phones = models.CharField(max_length=30)
    site = models.CharField(max_length=50, default="")
    password_tryed = models.IntegerField(default=0)

    def __str__(self):
        return "Adm" + ': ' + self.full_name + ' ('+ self.django_user.username + ')'