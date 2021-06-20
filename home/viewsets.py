from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from home.api.v1.serializers import (AppSerializer, PlanSerializer,
                                     SubscriptionSerializer)
from home.models import App, Plan, Subscription


class AppViewSet(ModelViewSet):
    serializer_class = AppSerializer
    swagger_tags = ["App"]

    def get_queryset(self):
        return self.request.user.apps.actives()


class PlanViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Plan.objects.actives()
    serializer_class = PlanSerializer
    swagger_tags = ["Plan"]


class SubscriptionViewSet(ModelViewSet):
    serializer_class = SubscriptionSerializer
    swagger_tags = ["Subscription"]

    def get_queryset(self):
        return Subscription.objects.filter(
            app__user=self.request.user).actives()
