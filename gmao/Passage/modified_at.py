from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Doleance(BaseModel):
    pass
    # vos champs existants


class Intervention(BaseModel):
    pass
    # vos champs existants


class Personnel(BaseModel):
    pass
    # vos champs existants
