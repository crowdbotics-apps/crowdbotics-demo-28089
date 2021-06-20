from django.db import models


class BaseModelQueryset(models.QuerySet):
    def actives(self):
        return self.filter(is_active=True)
