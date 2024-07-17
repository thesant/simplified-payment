from django.shortcuts import get_object_or_404
from ninja import Router
from rolepermissions.checkers import has_permission
from .tasks import send_notification
from challenge import settings
from challenge.payment.models import Transaction
from challenge.payment.schema import TransactionSchema
from challenge.users.models import User
from django.db import transaction as db_transaction
from django_q.tasks import async_task
import requests


payment_router = Router()


@payment_router.post('/', response={200: dict, 400: dict, 403: dict})
def transaction(request, transaction: TransactionSchema):
    payer = get_object_or_404(User, id=transaction.payer)
    payee = get_object_or_404(User, id=transaction.payee)
    if payer.amount < transaction.amount:
        return 400, {'error': 'Insufficient funds'}
    if not has_permission(payer, 'make_transfer'):
        return 403, {'error': 'You do not have permission'}
    with db_transaction.atomic():
        payer.pay(transaction.amount)
        payee.receive(transaction.amount)
        transaction_operation = Transaction(
            amount=transaction.amount,
            payer_id=transaction.payer,
            payee_id=transaction.payee,
        )
        payer.save()
        payee.save()
        transaction_operation.save()
        response = requests.get(settings.AUTHORIZE_TRANSFER_ENDPOINT).json()
        if response.get('status') != "authorized":
            raise Exception()
        async_task(send_notification, payer.first_name, payee.first_name, transaction.amount)
    return 200, {1: 1}
