from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from home.models import App
from home.tests.fakers import fake_user, fake_app


class AppTestCase(APITestCase):
    def setUp(self) -> None:
        self.user1 = fake_user()
        self.user2 = fake_user()

    def test_get_apps(self):
        fake_app(user=self.user1)

        self.client.force_authenticate(user=self.user1)
        response = self.client.get(reverse('apps-list'))
        self.assertEqual(response.data.get('count'), 1)

        # User2 shouldn't see User1's Apps
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(reverse('apps-list'))
        self.assertEqual(response.data.get('count'), 0)

    def test_create_app(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(
            reverse('apps-list'),
            data={'name': 'Django App',
                  'type': App.TypeChoices.MOBILE,
                  'framework': App.FrameworkChoices.DJANGO,
                  },
            format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_app(self):
        app = fake_app(user=self.user1, framework=App.FrameworkChoices.DJANGO,
                       name='Django App')

        self.client.force_authenticate(user=self.user1)
        self.client.patch(
            reverse('apps-detail', kwargs={'pk': app.id}),
            data={'name': 'React Native App',
                  'framework': App.FrameworkChoices.REACT_NATIVE,
                  },
            format='json')
        app.refresh_from_db()
        self.assertEqual(app.name, 'React Native App')
        self.assertEqual(app.framework, App.FrameworkChoices.REACT_NATIVE)

    def test_deactivate_app(self):
        app = fake_app(user=self.user1)
        self.assertTrue(app.is_active)

        self.client.force_authenticate(user=self.user1)

        # On delete request, App should be soft deleted by setting is_active to False
        self.client.delete(reverse('apps-detail', kwargs={'pk': app.id}))
        app.refresh_from_db()
        self.assertFalse(app.is_active)
