from django.shortcuts import render, redirect, HttpResponse
from .models import DataScheme, DataSchemeColumn
from .forms import DataSchemeCreationForm, RowsForm
from django.forms import inlineformset_factory
from .tasks import data_generation_task


def index(request):
    return render(request, 'csv_main/index.html')

# Render all schemas
def data_schema_view(request):
    schemas_query = DataScheme.objects.filter(owner_id=request.user)
    return render(request, 'csv_main/data-schemas.html', {
        'schemas_query': schemas_query,
    })


# Create an instance of a schema
def schema_creation(request):
    master_user = request.user
    ColumnFormset = inlineformset_factory(DataScheme, DataSchemeColumn,
                                          extra=1, can_delete=True,
                                          exclude=('parent_scheme', ))
    if request.method == 'POST':
        schema_form = DataSchemeCreationForm(request.POST)
        if schema_form.is_valid():
            schema_form = schema_form.save(commit=False)
            schema_form.owner = master_user
            schema_form.save()

            # validate each form
            new_schema = DataScheme.objects.latest('id')
            column_formset = ColumnFormset(request.POST, instance=new_schema)
            for form in column_formset:
                if form.is_valid():
                    form.save()
            how = column_formset.total_form_count()
            print(how)
        return redirect(data_sets)
    schema_form = DataSchemeCreationForm()
    column_formset = ColumnFormset(instance=None)
    return render(request, 'csv_main/schema-creation.html', {
        'schema_form': schema_form,
        'column_formset': column_formset,
    })


# Activate celery backround task processing
def data_generation(request, id):
    rows = request.session.get('rows_input')
    data_generation_task.delay(rows, id)
    return redirect(data_sets)


# Download generated file.csv
def data_download(request, file):
    file_name = file.rsplit('/', 1)[-1]
    with open(file, 'rb') as file:
        response = HttpResponse(file.read(), content_type="text/csv")
        response['Content-Disposition'] = f'attachment; filename="{file_name}.csv"'
    return response


# Display all data sets which user can generate or download
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


# KOSTYL Delete schema because I don't know JS
def delete_schema(request, id):
    DataScheme.objects.filter(id=id).delete()

    return redirect(data_schema_view)
