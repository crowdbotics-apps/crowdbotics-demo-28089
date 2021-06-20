from decimal import Decimal

from django.test import TestCase

from home.models import Plan


class PlanTestCase(TestCase):
    def test_plan_migration(self):
        self.assertEqual(Plan.objects.count(), 3)
        self.assertEqual(list(Plan.objects.values_list('name', flat=True)),
                         ['Free', 'Standard', 'Pro'])
        self.assertEqual(Plan.objects.get(name='Free').price, Decimal(0))
        self.assertEqual(Plan.objects.get(name='Standard').price, Decimal(10))
        self.assertEqual(Plan.objects.get(name='Pro').price, Decimal(25))
