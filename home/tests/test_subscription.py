from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from home.api.v1.serializers import SubscriptionSerializer
from home.models import Plan
from home.tests.fakers import fake_user, fake_subscription, fake_app


class SubscriptionTestCase(APITestCase):
    def setUp(self) -> None:
        self.user1 = fake_user()
        self.user2 = fake_user()
        self.free_plan = Plan.objects.get(name='Free')
        self.standard_plan = Plan.objects.get(name='Standard')
        self.pro_plan = Plan.objects.get(name='Pro')

    def test_create_subscription_free(self):
        app = fake_app(user=self.user1)

        self.client.force_authenticate(user=self.user1)

        response = self.client.post(
            reverse('subscriptions-list'),
            data={'app': app.id, 'plan': self.free_plan.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(
            reverse('subscriptions-list'),
            data={'app': app.id, 'plan': self.free_plan.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data.get('detail'),
            SubscriptionSerializer.default_error_messages[
                'already_subscribed_upgrade'])

    def test_create_subscription_pro(self):
        app = fake_app(user=self.user1)

        self.client.force_authenticate(user=self.user1)

        response = self.client.post(
            reverse('subscriptions-list'),
            data={'app': app.id, 'plan': self.pro_plan.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(
            reverse('subscriptions-list'),
            data={'app': app.id, 'plan': self.free_plan.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data.get('detail'),
            SubscriptionSerializer.default_error_messages['already_subscribed'])

    def test_cancel_subscription(self):
        app = fake_app(user=self.user1)
        sub = fake_subscription(app=app, plan=self.free_plan)

        self.client.force_authenticate(user=self.user1)

        # On delete request, Subscription should be cancelled by setting is_active to False
        self.client.delete(
            reverse('subscriptions-detail', kwargs={'pk': sub.id}))
        sub.refresh_from_db()
        self.assertFalse(sub.is_active)
