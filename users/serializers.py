from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from rest_framework import serializers
from django.contrib.auth import get_user_model
from dj_rest_auth.serializers import LoginSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import TokenModel

from django.core.exceptions import ValidationError as DjangoValidationError

from users.models import TeacherDetail, OrgDetail


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = get_user_model()
#         fields = ('email', 'password')


class UserLoginSerializer(LoginSerializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    username = None


class UserRegistrationSerializer(RegisterSerializer):
    username = None
    type = serializers.CharField(max_length=30)

    def update(self, instance, validated_data):
        super().update(instance, validated_data)

    def create(self, validated_data):
        super().create(validated_data)

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)

        self.cleaned_data = self.get_cleaned_data()
        user = adapter.save_user(request, user, self, commit=False)
        if "password1" in self.cleaned_data:
            try:
                adapter.clean_password(self.cleaned_data['password1'], user=user)
            except DjangoValidationError as exc:
                raise serializers.ValidationError(
                    detail=serializers.as_serializer_error(exc)
                )
        user.type = self.validated_data.get('type', '')
        user.save()
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user


class TeacherDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherDetail
        fields = ('full_name', 'phone_number', 'user')


class OrgDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrgDetail
        fields = ('org_name', 'mobile_number', 'phone_number', 'address', 'user')


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = TokenModel
        fields = ('key', 'user')
