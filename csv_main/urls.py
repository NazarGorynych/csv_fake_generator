from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name='csv'),
    path('', include('django.contrib.auth.urls')),
    path('data-schemes/', views.data_schema_view, name='data-scheme'),
    path('schema-creation/', views.schema_creation, name='schema-creation'),
    path('delete-schema/<int:id>/', views.delete_schema, name='delete-schema'),
    path('data-sets/', views.data_sets, name='data-sets'),
    path('data-generation/<int:id>', views.data_generation, name='data-generation'),
    path('data-download/<path:file>', views.data_download, name='data-download')
]