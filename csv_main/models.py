from django.db import models
from django.contrib.auth.models import User

class DataScheme(models.Model):
    scheme_name = models.CharField('DataScheme name', max_length=30)
    created_date = models.DateField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


class DataSchemeColumn(models.Model):

    TYPE_CHOICES = (
        ('Company', 'Company'),
        ('Job', 'Job'),
        ('Age', 'Age'),
    )

    column_name = models.CharField('ColumName', max_length=30)
    parent_scheme = models.ForeignKey(DataScheme, on_delete=models.CASCADE)
    # type = models.IntegerField()
    type = models.CharField(max_length=30, choices=TYPE_CHOICES, default=None)