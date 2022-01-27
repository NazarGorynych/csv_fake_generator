import csv
import os

from csv_generator.celery import app
from faker import Faker
from faker.providers import BaseProvider
from .models import DataScheme, DataSchemeColumn
from django.conf import settings

@app.task
def data_generation_task(rows, id):
    fake = Faker('en_US')
    fake.add_provider(BaseProvider)

    # Get parent Schema object
    query_object = DataScheme.objects.filter(id=id)
    for object in query_object:
        schema_object = object

    # File creation + generation
    csv_file_name = os.path.join(settings.MEDIA_ROOT, f'csv/{schema_object.scheme_name}')
    with open(csv_file_name, "w") as csv_file:
        column_names = []
        column_types = []

        # Find all columns of schema
        columns = DataSchemeColumn.objects \
            .filter(parent_scheme=schema_object).order_by('order')

        # Fill in two lists two find crossection of faker dictionary
        for column in columns:
            column_names.append(column.column_name)
            column_types.append(column.type)

        # Write first row with names of columns
        writer = csv.writer(csv_file)
        writer.writerow(column_names)

        # Write row from crossection of values
        for row in range(int(rows)):
            value_list = {
                "Name": fake.name(),
                "Email": fake.email(),
                "Job": fake.job(),
                "Phone Number": fake.phone_number(),
                "Text": fake.paragraph(nb_sentences=5),
                "Boolean": fake.pybool(),
                "Address": fake.address(),
                "Link": fake.url(),
                "Age": fake.random_int(min=18, max=100),
            }
            new2_dict = {key: value_list[key] for key in column_types if key in value_list }
            writer.writerow(new2_dict[key] for key in column_types)

        # Save to FileField of Schema object
        schema_object.file = csv_file_name
        schema_object.save()
    return
