from django.contrib import admin

from challenge.payment.models import Transaction


@admin.register(Transaction)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'payer', 'payee', 'date')
