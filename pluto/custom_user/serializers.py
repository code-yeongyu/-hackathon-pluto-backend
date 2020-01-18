from rest_framework import serializers
from custom_user.models import Profile
import drf_yasg.openapi as openapi


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('nickname', 'exp')
        parameters = [
            openapi.Parameter('nickname',
                              openapi.IN_QUERY,
                              description="varchar(10)",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('exp',
                              openapi.IN_QUERY,
                              description="",
                              type="Integer"),
        ]