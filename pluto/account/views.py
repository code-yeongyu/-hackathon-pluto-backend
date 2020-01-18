from account.serializers import RecordSerializer
from rest_framework.views import APIView
from rest_framework import permissions, status
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.response import Response
from account.models import Record
from account.models import Account
from account.serializers import AccountSerializer
from account.serializers import RecordSerializer
from rest_framework import generics
from rest_framework.decorators import api_view

from drf_yasg.utils import swagger_auto_schema


class AccountOverall(APIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    @swagger_auto_schema(
        operation_description="Get my accounts",
        responses={
            200: 'Account Created Successfully',
            404: 'Failed to create account.'
        },
        manual_parameters=AccountSerializer.Meta.parameters,
    )
    def post(self, request):
        if request.user.is_authenticated:
            serializer = AccountSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(owner=request.user)
                return JsonResponse(serializer.data,
                                    status=status.HTTP_201_CREATED)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@swagger_auto_schema(method='get',
                     operation_description="Get my accounts",
                     responses={
                         200: 'Account Created Successfully',
                         404: 'Failed to find requested value.'
                     })
@api_view(['GET'])
def my_accounts_view(request, ):
    object_to_return = get_object_or_404(Account, owner=request.user)
    return Response(AccountSerializer(object_to_return).data)


@swagger_auto_schema(method='get',
                     operation_description="Get my transaction records",
                     responses={
                         200: 'Account Created Successfully',
                         404: 'Failed to find requested value.'
                     })
@api_view(['GET'])
def my_records_view(request, ):
    account = get_object_or_404(Account, owner=request.user)
    object_to_return = get_object_or_404(Record, account=account)
    return Response(RecordSerializer(object_to_return).data)
