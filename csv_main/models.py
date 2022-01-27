from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class DataScheme(models.Model):

    scheme_name = models.CharField('DataScheme name', max_length=30)
    created_date = models.DateField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(blank=False)

    def __str__(self):
        return self.scheme_name


class DataSchemeColumn(models.Model):

    TYPE_CHOICES = (
        ('Name', 'Name'),
        ('Email', 'Email'),
        ('Job', 'Job'),
        ('Phone Number', 'Phone Number'),
        ('Text', 'Text'),
        ('Boolean', 'Boolean'),
        ('Address', 'Address'),
        ('Link', 'Link'),
        ('Age', 'Age')
    )

    column_name = models.CharField('ColumName', max_length=30)
    parent_scheme = models.ForeignKey(DataScheme, on_delete=models.CASCADE)
    # type = models.IntegerField()
    type = models.CharField(max_length=30, choices=TYPE_CHOICES, default=None)
    order = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), ])
    int_range = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)], unique=True,
                                            blank=True, null=True)

    def __str__(self):
        return self.column_name