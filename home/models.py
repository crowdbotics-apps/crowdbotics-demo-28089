from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from home.managers import BaseModelQueryset


class BaseModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    objects = models.Manager.from_queryset(BaseModelQueryset)()

    class Meta:
        abstract = True

    def delete(self, user=None, using=None, keep_parents=False):
        self.is_active = False
        self.save(update_fields=['is_active'])
        return 1

    def save(self, *args, **kwargs):
        if self.pk:
            self.updated_at = timezone.now()
        super(BaseModel, self).save(*args, **kwargs)


class Plan(BaseModel):
    name = models.CharField(max_length=20)
    description = models.TextField()
    price = models.DecimalField(default=0, max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.price}"


class App(BaseModel):
    class TypeChoices(models.TextChoices):
        WEB = 'Web', _('Web')
        MOBILE = 'Mobile', _('Mobile')

    class FrameworkChoices(models.TextChoices):
        DJANGO = 'Django', _('Django')
        REACT_NATIVE = 'React Native', _('React Native')

    name = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    type = models.CharField(max_length=6, choices=TypeChoices.choices)
    framework = models.CharField(max_length=12,
                                 choices=FrameworkChoices.choices)
    domain_name = models.CharField(max_length=50, blank=True)
    screenshot = models.URLField(blank=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT,
                             related_name='apps')

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f"{self.name} - {self.type}/{self.framework} - {self.domain_name}"


class Subscription(BaseModel):
    plan = models.ForeignKey('home.Plan', on_delete=models.PROTECT)
    app = models.ForeignKey('home.App', on_delete=models.PROTECT)
