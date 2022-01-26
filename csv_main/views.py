import csv
from  celery.utils.log import get_logger
from faker import Faker
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import DataScheme, DataSchemeColumn, User
from .forms import DataSchemeCreationForm, DataSchemeColumnCreationForm, RowsForm
from django.forms import formset_factory, inlineformset_factory, modelformset_factory
from .tasks import data_generation_task, add
from django.conf import settings


def index(request):
    return render(request, 'csv_main/index.html')


def data_schema_view(request):
    schemas_query = DataScheme.objects.filter(owner_id=request.user)
    return render(request, 'csv_main/data-schemas.html', {
        'schemas_query': schemas_query,
    })


def schema_creation(request):
    master_user = request.user
    ColumnFormset = inlineformset_factory(DataScheme, DataSchemeColumn,
                                          extra=4, exclude=('parent_scheme', ))
    if request.method == 'POST':
        schema_form = DataSchemeCreationForm(request.POST)
        if schema_form.is_valid():
            schema_form = schema_form.save(commit=False)
            schema_form.owner = master_user
            schema_form.save()
            new_schema = DataScheme.objects.latest('id')
            column_formset = ColumnFormset(request.POST, instance=new_schema)
            if column_formset.is_valid():
                column_formset.save()
        return redirect(data_sets)
    schema_form = DataSchemeCreationForm()
    column_formset = ColumnFormset(instance=None)
    return render(request, 'csv_main/schema-creation.html', {
        'schema_form': schema_form,
        'column_formset': column_formset,
    })


def data_generation(request, id):
    rows = request.session.get('rows_input')
    data_generation_task.delay(rows, id)
    # add.delay(1, 2)
    return redirect(data_sets)

def data_download(request, file):
    file_name = file.rsplit('/', 1)[-1]
    with open(file, 'rb') as file:
        response = HttpResponse(file.read(), content_type="text/csv")
        response['Content-Disposition'] = f'attachment; filename="{file_name}.csv"'
    return response

def data_sets(request):
    schemas_query = DataScheme.objects.filter(owner_id=request.user)
    rows = RowsForm()
    if request.method == 'POST':
        rows = RowsForm(request.POST)
        request.session['rows_input'] = request.POST.get('rows_quantity')
    return render(request, 'csv_main/data-sets.html', {
        'schemas_query': schemas_query,
        'rows': rows,
    })


def delete_schema(request, id):
    DataScheme.objects.filter(id=id).delete()

    return redirect(data_schema_view)
