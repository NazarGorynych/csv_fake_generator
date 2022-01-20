from django import forms
from django.forms import ModelForm, inlineformset_factory
from .models import DataScheme, DataSchemeColumn


class DataSchemeCreationForm(ModelForm):

    class Meta:
        model = DataScheme
        fields = '__all__'
        exclude = ['owner', ]
    #
    # def scheme_save(self, commit=True):
    #     DataScheme = super(DataSchemeCreationForm, self).save(commit=False)
    #     if commit:
    #         DataScheme.save()
    #     return DataScheme

class DataSchemeColumnCreationForm(ModelForm):


    class Meta:
        model = DataSchemeColumn
        fields = '__all__'
        exclude = ['parent_scheme', ]

    # def column_save(self, commit=True):
    #     DataSchemeColumn = super(DataSchemeColumnCreationForm, self).save(commit=False)
    #     if commit:
    #         DataSchemeColumn.save()
    #     return DataSchemeColumn
