from ninja import Schema

from challenge.payment.models import Transaction


class TransactionSchema(Schema):
    class Meta:
        model = Transaction
        exclude = ("id", "date")
