from dps.models import Transaction
from django.contrib import admin

class TransactionAdmin(admin.ModelAdmin):
    pass


class TransactionInlineAdmin(generic.GenericTabularInline):
    model = Transaction

    def has_add_permission(self, request):
        return False

    
admin.site.register(Transaction, TransactionAdmin)
