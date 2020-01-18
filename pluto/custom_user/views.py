from django.core.paginator import Paginator
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from custom_user.models import Profile
from custom_user.serializers import ProfileSerializer
from custom_user.forms import RegisterForm
from rest_framework.decorators import api_view
import math
from drf_yasg.utils import swagger_auto_schema
import drf_yasg.openapi as openapi


def get_level(exp):
    total = 0
    level = 1
    while True:
        level += 1
        total += int(math.log10(level + 1) * 200) - 40
        if exp < total:
            break
    return level


class ProfileAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Get the informations of requested user",
        responses={200: 'Successfully returned the requested value.'},
        manual_parameters=ProfileSerializer.Meta.parameters)
    def get(self, request):
        if request.user.is_authenticated:
            profile = Profile.objects.get(user=request.user)
            data = ProfileSerializer(profile).data
            data['level'] = get_level(data['exp'])
            return Response(data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Update the informations of requested user",
        responses={
            200: 'Successfully updated the requested value.',
            406: 'Errors occured with given datas'
        },
        manual_parameters=ProfileSerializer.Meta.parameters,
    )
    def patch(self, request):
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors,
                        status=status.HTTP_406_NOT_ACCEPTABLE)


@swagger_auto_schema(method='post',
                     operation_description="Resgiter a new account",
                     responses={
                         201: 'Account Created Successfully',
                         406: 'Errors occured with given datas'
                     },
                     manual_parameters=RegisterForm.Meta.parameters)
@api_view(['POST'])
def register(request):
    form = RegisterForm(request.POST)
    if form.is_valid():
        user = form.save(commit=False)
        user.save()
        profile = Profile.objects.get_or_create(user=user)
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(status=status.HTTP_201_CREATED)
    return Response(form.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


@swagger_auto_schema(
    method='get',
    operation_description="Get rankings from begin to end",
    responses={200: 'Successfully returned the requested value.'},
    manual_parameters=[
        openapi.Parameter('begin',
                          openapi.IN_QUERY,
                          description="varchar(10)",
                          type="Integer"),
        openapi.Parameter('end',
                          openapi.IN_QUERY,
                          description="JSON typed integer array",
                          type="Integer"),
    ])
@api_view(['GET'])
def page_ranking(request):
    begin = request.GET.get('begin')
    end = request.GET.get('end')
    profiles = Profile.objects.all().order_by('exp').reverse()
    serializer = ProfileSerializer(profiles, many=True)
    users = serializer.data[begin:end]
    for user in users:
        user['level'] = get_level(user['exp'])
    return Response(users)