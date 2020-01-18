from django.db import models


# Create your models here.
class Account(models.Model):
    owner = models.ForeignKey('auth.user',
                              related_name='account_owner',
                              on_delete=models.CASCADE,
                              null=False)
    account_number = models.CharField(max_length=20, null=False, blank=False)
    account_name = models.CharField(max_length=20, default='')
    bank_company = models.CharField(max_length=20, null=False, blank=False)
    account_owner_name = models.CharField(max_length=20,
                                          null=False,
                                          blank=False)
    balance = models.IntegerField(null=False)


class Record(models.Model):
    account = models.ForeignKey(Account,
                                related_name='account',
                                on_delete=models.CASCADE)
    is_deposit = models.BooleanField(null=False)
    transfered_amount = models.IntegerField(null=False)
    remain_balance = models.IntegerField(null=False)
