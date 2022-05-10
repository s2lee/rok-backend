from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class CustomRegisterSerializer(RegisterSerializer):
    nickname = serializers.CharField(
        max_length=15,
        validators=[UniqueValidator(queryset=get_user_model().objects.all())],
    )

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data["nickname"] = self.validated_data.get("nickname", "")

        return data
