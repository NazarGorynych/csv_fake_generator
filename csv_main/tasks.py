
from csv_generator.celery import app
import csv
import os
from celery.contrib import rdb
from faker import Faker
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import DataScheme, DataSchemeColumn, User
from django.core.files.storage import FileSystemStorage
from django.conf import settings

@app.task
def data_generation_task(rows, id):
    fake = Faker('en_US')
    query_object = DataScheme.objects.filter(id=id)
    for object in query_object:
        schema_object = object
    csv_file_name = os.path.join(settings.MEDIA_ROOT, f'csv/{schema_object.scheme_name}')
    with open(csv_file_name, "w") as csv_file:
        columns = DataSchemeColumn.objects.filter(parent_scheme=schema_object).order_by('order')
        column_names = []
        column_types = []
        writer = csv.writer(csv_file)
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

        for row in range(int(rows)):
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
        schema_object.file = csv_file_name
        schema_object.save()
    return

@app.task()
def add(x, y):

    temporart = DataScheme.objects.all()
    return x + y