from django.shortcuts import render, redirect, get_object_or_404
from .models import DataScheme, DataSchemeColumn, User
from django.http import HttpResponse
from django.views.generic import ListView

def index(request):
    return render(request, 'index.html')

def data_scheme_view(request):
    schemes_query = DataScheme.objects.filter(owner_id=request.user)
    return render(request, 'data-schemes.html', {
        'schemes_query': schemes_query,
    })

def delete_schema(request, id):
    DataScheme.objects.filter(id=id).delete()

    return redirect(data_scheme_view)
