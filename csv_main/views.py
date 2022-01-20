import csv

from faker import Faker
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import DataScheme, DataSchemeColumn, User
from .forms import DataSchemeCreationForm, DataSchemeColumnCreationForm
from django.forms import formset_factory, inlineformset_factory, modelformset_factory



def index(request):
    return render(request, 'index.html')


def data_schema_view(request):
    schemas_query = DataScheme.objects.filter(owner_id=request.user)
    return render(request, 'data-schemas.html', {
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
            new_schema = DataScheme.objects.latest('scheme_name')
            column_formset = ColumnFormset(request.POST, instance=new_schema)
            if column_formset.is_valid():
                column_formset.save()
    schema_form = DataSchemeCreationForm()
    column_formset = ColumnFormset(instance=None)
    return render(request, 'schema-creation.html', {
        'schema_form': schema_form,
        'column_formset': column_formset,
    })


def data_sets(request):
    fake = Faker('en_US')
    # master_user = request.user
    schema_object = DataScheme.objects.latest('scheme_name')
    # schema_object = DataScheme.objects.filter(id='id')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename={schema_object.scheme_name}.csv'
    writer = csv.writer(response)
    columns = DataSchemeColumn.objects.filter(parent_scheme=schema_object).order_by('order')
    column_names = []
    column_types = []
    for column in columns:
        column_names.append(column.column_name)
        column_types.append(column.type)
    writer.writerow(column_names)
    column_names = set(column_names)
    fake_list = {
        "Company": fake.name(),
        # "Phone Number": fake1.phone_number(),
        "Email": fake.email(),
        # "Address": fake.address(),
        # "Time": fake.time(),
        "Link": fake.url(),
        "Text": fake.word(),
    }

    new_dict = {k: fake_list[k] for k in column_types if k in fake_list}

    for row in range(5):
        value_list = {
            "Company": fake.name(),
            # "Phone Number": fake1.phone_number(),
            "Email": fake.email(),
            # "Address": fake.address(),
            # "Time": fake.time(),
            "Link": fake.url(),
            "Text": fake.word(),
        }
        new2_dict = {key: value_list[key] for key in new_dict if key in value_list }
        writer.writerow(new2_dict[key] for key in column_types)

    # for row in range(5):
    #     writer.writerow(fake_list[f"{type}"] for type in column_types)

    return response


def delete_schema(request, id):
    DataScheme.objects.filter(id=id).delete()

    return redirect(data_schema_view)
