# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from decimal import *
from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.db.models import F
# All arithmetic operation will have 6 digit precision
getcontext().prec = 2

# Get the user model
AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class Account(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    number = models.CharField(max_length=20)
    balance = models.DecimalField(max_digits=15,decimal_places=2,
        default=Decimal(0.0),
        validators=[MinValueValidator(Decimal(0.0))])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'number',)

    def __str__(self):
        return self.number

    def debit(self,amount):
        self.credit(-amount)

    def credit(self,amount):
        self.balance = F('balance')+amount
        self.save()
        self.refresh_from_db()


class Transaction(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL,on_delete=models.PROTECT)
    debit_account = models.ForeignKey(Account,related_name="debits",
        on_delete=models.CASCADE)
    credit_account = models.ForeignKey(Account,related_name="credits",
        on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2,
        validators=[MinValueValidator(Decimal(0.0))])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if not self.pk:
            if self.debit_account.user!=self.credit_account.user:
                raise ValidationError("Invalid account")
            if self.debit_account.balance<self.amount:
                raise ValidationError("Insufficient balance")
        else:
            raise ValidationError("Oops! Transactions are immutable")


    def __str__(self):
        return "{0} -> {1} : ₹{2}".format(
            self.debit_account,
            self.credit_account,
            self.amount,
        )


@receiver(post_save, sender=Transaction)
def new_transaction(sender, instance, created, **kwargs):
    """Transfer balance"""
    if created:
        instance.debit_account.debit(instance.amount)
        instance.credit_account.credit(instance.amount)
