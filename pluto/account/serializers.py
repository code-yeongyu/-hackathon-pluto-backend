from rest_framework import serializers
from account.models import Account
from account.models import Record
import drf_yasg.openapi as openapi


class AccountSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='writer.username')

    class Meta:
        model = Account
        fields = ('owner', 'account_number', 'account_name', 'bank_company',
                  'account_owner_name', 'balance')
        parameters = [
            openapi.Parameter('account_number',
                              openapi.IN_QUERY,
                              description="varchar(20)",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('account_name',
                              openapi.IN_QUERY,
                              description="",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('bank_company',
                              openapi.IN_QUERY,
                              description="",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('account_owner_name',
                              openapi.IN_QUERY,
                              description="",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('balance',
                              openapi.IN_QUERY,
                              description="",
                              type="Integer"),
        ]


class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = ('account', 'is_deposit', 'transfered_amount',
                  'remain_balance')
