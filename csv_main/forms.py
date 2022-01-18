from django import forms
from django.forms import ModelForm, ModelMultipleChoiceField
from .models import DataScheme, DataSchemeColumn


class PostForm(ModelForm):

    class Meta:
        model = DataSchemeColumn
        fields = '__all__'

