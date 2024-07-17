from decimal import Decimal
from django.db import models
from challenge.users.models import User


class Transaction(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), editable=False)
    payer = models.ForeignKey(User, on_delete=models.DO_NOTHING, editable=False)
    payee = models.ForeignKey(User, on_delete=models.DO_NOTHING, editable=False, related_name='payee_user')
    date = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return f'From {self.payer.first_name} to {self.payee.first_name} - R${self.amount}'
