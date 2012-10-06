from dps.models import Transaction
from django.contrib import admin

class TransactionAdmin(admin.ModelAdmin):
    pass

admin.site.register(Transaction, TransactionAdmin)
