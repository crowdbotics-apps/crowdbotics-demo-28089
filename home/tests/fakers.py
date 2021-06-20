from django.contrib.auth import get_user_model
from model_bakery import baker


def fake_user(**kwargs):
    return baker.make(get_user_model(), **kwargs)


def fake_subscription(**kwargs):
    return baker.make('home.Subscription', **kwargs)


def fake_app(**kwargs):
    return baker.make('home.App', **kwargs)
