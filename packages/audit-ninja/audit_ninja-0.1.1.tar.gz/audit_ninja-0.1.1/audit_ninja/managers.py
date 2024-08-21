from django.db import models

class CustomQuerySet(models.QuerySet):
    def update(self, *args, **kwargs):
        print(f"Calling CustomQuerySet")
        result = super().update(*args, **kwargs)
        print(f"Updated {result} rows in QuerySet {self.__class__.__name__}.")
        return result
    
class CustomManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model', None)
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        return CustomQuerySet(self.model, using=self._db)
