from django import forms
from django.forms import ModelForm, inlineformset_factory
from .models import DataScheme, DataSchemeColumn
from djangoformsetjs.utils import formset_media_js

class DataSchemeCreationForm(ModelForm):

    class Meta:
        model = DataScheme
        fields = '__all__'
        exclude = ['owner', 'file', ]
    #
    # def scheme_save(self, commit=True):
    #     DataScheme = super(DataSchemeCreationForm, self).save(commit=False)
    #     if commit:
    #         DataScheme.save()
    #     return DataScheme

class DataSchemeColumnCreationForm(ModelForm):


    class Meta:
        # js = formset_media_js
        model = DataSchemeColumn
        fields = '__all__'
        exclude = ['parent_scheme', ]


class RowsForm(forms.Form):
    rows_quantity = forms.IntegerField(min_value=1, initial=10)