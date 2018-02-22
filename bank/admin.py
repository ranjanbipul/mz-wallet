# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import  *

# Register your models here.

class AccountAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'number',
        'balance'
    )


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'debit_account', 'credit_account', 'amount',)
    def has_change_permission(self, request, obj=None):
        if obj:
            return False
        else:
            return True

admin.site.register(Account, AccountAdmin)
admin.site.register(Transaction, TransactionAdmin)
