from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.utils.translation import ugettext_lazy as _
from allauth.account import app_settings as allauth_settings
from allauth.account.forms import ResetPasswordForm
from allauth.utils import email_address_exists, generate_unique_username
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from rest_framework import serializers
from rest_auth.serializers import PasswordResetSerializer

from home.models import Plan, App, Subscription

User = get_user_model()


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {
                    'input_type': 'password'
                }
            },
            'email': {
                'required': True,
                'allow_blank': False,
            }
        }

    def _get_request(self):
        request = self.context.get('request')
        if request and not isinstance(request, HttpRequest) and hasattr(request,
                                                                        '_request'):
            request = request._request
        return request

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    _("A user is already registered with this e-mail address."))
        return email

    def create(self, validated_data):
        user = User(
            email=validated_data.get('email'),
            name=validated_data.get('name'),
            username=generate_unique_username([
                validated_data.get('name'),
                validated_data.get('email'),
                'user'
            ])
        )
        user.set_password(validated_data.get('password'))
        user.save()
        request = self._get_request()
        setup_user_email(request, user, [])
        return user

    def save(self, request=None):
        """rest_auth passes request so we must override to accept it"""
        return super().save()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name']


class PasswordSerializer(PasswordResetSerializer):
    """Custom serializer for rest_auth to solve reset password error"""
    password_reset_form_class = ResetPasswordForm


class BaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = None
        exclude = ('is_active',)
        extra_kwargs = {
            'created_at': {
                'read_only': True,
            },
            'updated_at': {
                'read_only': True,
            }
        }


class PlanSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Plan


class AppSerializer(serializers.ModelSerializer):
    class Meta(BaseSerializer.Meta):
        model = App
        exclude = BaseSerializer.Meta.exclude + ('user',)

    def save(self, **kwargs):
        self.validated_data['user_id'] = self.context.get('request').user.id
        return super(AppSerializer, self).save(**kwargs)


class SubscriptionSerializer(serializers.ModelSerializer):
    default_error_messages = {
        'already_subscribed': _('You already have subscription'),
        'already_subscribed_upgrade': _('You already have subscription, '
                                        'you can upgrade your subscription'),

    }

    class Meta(BaseSerializer.Meta):
        model = Subscription

    def validate(self, attrs):
        request = self.context.get('request')
        user = request.user
        current_sub = Subscription.objects.select_related('plan').filter(
            app__user=user).actives().first()
        if current_sub:
            # TODO: get rid of magic string
            if current_sub.plan.name != 'Pro':
                raise serializers.ValidationError(
                    self.error_messages['already_subscribed_upgrade'])
            raise serializers.ValidationError(
                self.error_messages['already_subscribed'])

        return attrs
