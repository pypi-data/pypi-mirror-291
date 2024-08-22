import importlib
import sys
import traceback

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.timezone import now
from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .forms import VerifyPhoneForm
from .mixins import LoginGetFormClassMixin, RegisterMixin, SendEmailVerificationMixin, ViewCallbackMixin, \
    VerifyEmailMixin
from .serializers import LogoutSerializer, PasswordResetSerializer, ChangePasswordSerializer
from .verify_phone import VerifyPhone
from ..utils import get_user_tokens, get_errors

UserModel = get_user_model()


class LoginAPIView(LoginGetFormClassMixin, APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        form = self.get_form_class()(data=request.data)
        if form.is_valid():
            user = form.user_cache
            tokens = get_user_tokens(user)
            return Response(tokens, status=status.HTTP_200_OK)

        return Response(get_errors(form.errors.as_data()), status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class RegisterAPIView(RegisterMixin, APIView):
    # access_token = None
    # refresh_token = None
    # token = None
    # user = None
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        form = self.get_form_class()(data=request.data)
        if form.is_valid():
            user = form.save()

            self.get_callback('REGISTER_CALLBACK', user)

            self.send_email_verification(request, user)

            self.send_phone_verification(user)

            refresh = RefreshToken.for_user(user)

            return Response({
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh)
            }, status=status.HTTP_201_CREATED)

        return Response(form.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class ResendEmailVerificationLinkAPIView(SendEmailVerificationMixin, ViewCallbackMixin, APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        self.send_email_verification(request, request.user)

        self.get_callback('REGISTER_CALLBACK', request.user)

        return Response({
            "message": _('Email activation link sent successfully')
        })


class VerifyEmailAPIView(VerifyEmailMixin, ViewCallbackMixin, APIView):
    def get(self, request, uidb64, token):
        success, user = self.verify(uidb64, token)
        self.get_callback("VERIFY_EMAIL_CALLBACK", user)
        if success:
            return Response({"message": _('Email was verified successfully.')}, status=status.HTTP_200_OK)
        return Response({"message": _('Something went wrong, please try again!')}, status=status.HTTP_400_BAD_REQUEST)


class VerifyPhoneAPIView(VerifyEmailMixin, ViewCallbackMixin, APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        if request.user.phone_verified_at is not None:
            return Response({
                'message': _('this account was activated before')
            }, status=status.HTTP_400_BAD_REQUEST)

        form = VerifyPhoneForm(request.POST, user=request.user)
        if form.is_valid():
            request.user.phone_verified_at = now()
            request.user.save()
            self.get_callback("VERIFY_PHONE_CALLBACK", request.user)
            return Response({
                'message': _('Phone verified successfully!')
            }, status=status.HTTP_200_OK)
        return Response(form.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class UserLogoutAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = LogoutSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordAPIView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = UserModel
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK, data={'msg': _("Password updated successfully")})
        return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY, data=serializer.errors)


class PasswordResetAPIView(APIView):
    permission_classes = []
    authentication_classes = []
    email_template_name = 'dj_accounts/password_reset_email.html'
    extra_email_context = None
    from_email = None
    html_email_template_name = None
    subject_template_name = 'dj_accounts/password_reset_subject.txt'
    token_generator = default_token_generator

    def post(self, request, *args, **kwargs):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            opts = {
                'use_https': self.request.is_secure(),
                'token_generator': self.token_generator,
                'from_email': self.from_email,
                'email_template_name': self.email_template_name,
                'subject_template_name': self.subject_template_name,
                'request': self.request,
                'html_email_template_name': self.html_email_template_name,
                'extra_email_context': self.extra_email_context,
            }
            serializer.save(opts=opts)
            return Response({"message": "{} {}".format(
                _('We’ve emailed you instructions for setting your password, '
                  'if an account exists with the email you entered. You should receive them shortly.'),
                _('If you don’t receive an email, please make sure you’ve entered '
                  'the address you registered with, and check your spam folder.'))},
                status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class ResendPhoneVerificationAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:
            VerifyPhone().send(request.user.phone)
        except Exception as e:
            parts = ["Traceback (most recent call last):\n"]
            parts.extend(traceback.format_stack(limit=25)[:-2])
            parts.extend(traceback.format_exception(*sys.exc_info())[1:])
            print("".join(parts))

        return Response({"message": _('Code was resent successfully.')}, status=status.HTTP_200_OK)


class UpdateProfileAPIView(APIView):
    """
    An endpoint for changing User Profile Data.
    """

    def get_serializer_class(self):
        serializer_class = getattr(settings, "PROFILE_SERIALIZER", 'dj_accounts.serializer.UpdateUserDataSerializer')
        if type(serializer_class) is str:
            form_class_split = serializer_class.split('.')
            class_name = form_class_split[-1:][0]
            module_name = form_class_split[:-1]
            return getattr(importlib.import_module('.'.join(module_name)), class_name)
        return serializer_class

    permission_classes = (IsAuthenticated,)

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data, instance=request.user)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

# class ChangeEmailAPIView(APIView):
#     """
#     An endpoint for changing Email.
#     """
#     permission_classes = (IsAuthenticated,)
#
#     def get_serializer_class(self):
#         # todo: change this serializer to basic Update Email Form
#         return getattr(settings, "UPDATE_EMAIL_FORM", UpdateEmailForm)
#
#     def put(self, request, *args, **kwargs):
#         validation_from = self.get_serializer_class()(data=request.data, user=request.user)
#         if validation_from.is_valid():
#             validation_from.save()
#             return Response({'message': _('Email Changed Successfully')}, status=status.HTTP_201_CREATED)
#         return Response(validation_from.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
#
#
# class ChangePhoneAPIView(APIView):
#     """
#     An endpoint for changing Phone.
#     """
#     permission_classes = (IsAuthenticated,)
#
#     def get_serializer_class(self):
#         return getattr(settings, "UPDATE_PHONE_FORM", UpdatePhoneNumberForm)
#
#     def put(self, request, *args, **kwargs):
#         validated_fields = self.get_serializer_class()(data=request.data, user=request.user)
#         if validated_fields.is_valid():
#             validated_fields.save()
#             return Response(status=status.HTTP_201_CREATED)
#         return Response(validated_fields.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
