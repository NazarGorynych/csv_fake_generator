from django.shortcuts import render, redirect, get_object_or_404
from .models import DataScheme, DataSchemeColumn, User
from .forms import DataSchemeCreationForm, DataSchemeColumnCreationForm
from django.forms import formset_factory


def index(request):
    return render(request, 'index.html')


def data_schema_view(request):
    schemas_query = DataScheme.objects.filter(owner_id=request.user)
    return render(request, 'data-schemas.html', {
        'schemas_query': schemas_query,
    })


def schema_creation(request):
    master_user = request.user
    ColumnFormset = formset_factory(DataSchemeColumnCreationForm, extra=2)
    column_formset = ColumnFormset()
    if request.method == 'POST':
        schema_form = DataSchemeCreationForm(request.POST)
        column_formset = ColumnFormset(request.POST, request.FILES)
        if schema_form.is_valid():
            schema_form = schema_form.save(commit=False)
            schema_form.owner = master_user
            schema_form.save()
            new_schema = DataScheme.objects.latest('id')
            if column_formset.is_valid():
                print('is_valid')
                for form in column_formset:
                    if form.is_valid():
                        form = form.save(commit=False)
                        form.parent_schema = new_schema
                        form.save()
                        print('success')
                    else:
                        print('das_ist_totalen_Blyat')
            else:
                print('not valid')
    schema_form = DataSchemeCreationForm()
    return render(request, 'schema-creation.html', {
        'schema_form': schema_form,
        'column_formset': column_formset,
    })


def delete_schema(request, id):
    DataScheme.objects.filter(id=id).delete()

    return redirect(data_schema_view)
