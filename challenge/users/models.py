from decimal import Decimal

from django.contrib.auth.models import AbstractUser
from django.db import models

from challenge.users.validators import validate_cpf


class User(AbstractUser):
    cpf = models.CharField(max_length=14, unique=True, validators=[validate_cpf])
    email = models.EmailField(unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        self.cpf = self.cpf.replace('.', '').replace('-', '').replace(' ', '')
        super(User, self).save(*args, **kwargs)

    def pay(self, value: Decimal):
        if not isinstance(value, Decimal):
            raise TypeError('value must be of type Decimal')

        self.amount -= value

    def receive(self, value: Decimal):
        if not isinstance(value, Decimal):
            raise TypeError('value must be of type Decimal')

        self.amount += value
