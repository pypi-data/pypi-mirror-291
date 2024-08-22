from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth import password_validation
from django.contrib.auth.forms import PasswordResetForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from .forms import RegisterForm, MultipleLoginForm

UserModel = get_user_model()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False, allow_blank=True)
    username = serializers.CharField(required=False, allow_blank=True)
    phone = serializers.CharField(required=False, allow_blank=True)
    password = serializers.CharField(write_only=True)
    cache_user = None

    def validate(self, attrs):
        form = self.get_authentication_form()(data=dict(**attrs))
        if not form.is_valid():
            raise serializers.ValidationError(form.errors)

        self.cache_user = form.get_user()
        return attrs

    def get_authentication_form(self):
        if getattr(settings, 'MULTIPLE_AUTHENTICATION_ACTIVE', False):
            return MultipleLoginForm
        return getattr(settings, 'LOGIN_FORM', AuthenticationForm)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=True, help_text=_("Required, please provide your refresh token"))

    def save(self, **kwargs):
        try:
            RefreshToken(self.validated_data['refresh']).blacklist()
        except TokenError:
            raise ValidationError({"refresh": _('Invalid token.')})


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        max_length=100, help_text=_("Required, please provide your username"))

    email = serializers.EmailField(
        required=True,
        max_length=100, help_text=_("Required, please provide your email"))

    phone = serializers.CharField(
        required=True,
        max_length=100, help_text=_("Required, please provide your phone number"))

    password1 = serializers.CharField(
        required=True,

        help_text=password_validation.password_validators_help_text_html())

    password2 = serializers.CharField(
        required=True,
        help_text=_("Enter the same password as before, for verification."))

    class Meta:
        model = UserModel
        fields = ['username', 'email', 'password1', 'password2', 'phone']

    def validate(self, attrs):
        form = RegisterForm(data=attrs)
        if not form.is_valid():
            raise serializers.ValidationError(form.errors)
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password1')
        user = super(RegisterSerializer, self).create(validated_data)
        user.set_password(password)
        user.save()
        return user


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254)

    form = None

    def validate(self, attrs):
        self.form = PasswordResetForm(data=attrs)
        if not self.form.is_valid():
            raise serializers.ValidationError(self.form.errors)
        return attrs

    def save(self, **kwargs):
        opts = kwargs.get('opts')
        self.form.save(**opts)


class UpdateUserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name']


class UpdateEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['email', 'password']


class UpdatePhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['phone', 'password']


class ChangePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['new_password1', 'new_password2', 'old_password']

    new_password1 = serializers.CharField(required=True, write_only=True)
    new_password2 = serializers.CharField(required=True, write_only=True, validators=[validate_password])
    old_password = serializers.CharField(required=True, write_only=True)
    form = None

    def validate(self, data):
        self.form = PasswordChangeForm(data=data, user=self.context['request'].user)
        if not self.form.is_valid():
            serializers.ValidationError(self.form.errors)
        return data

    def save(self, **kwargs):
        self.form.save()
