from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name='csv'),
    path('', include('django.contrib.auth.urls')),
    path('data-schemes/', views.data_schema_view, name='data-scheme'),
    path('schema-creation/', views.schema_creation, name='schema-creation'),
    path('delete-schema/<int:id>/', views.delete_schema, name='delete-schema'),
    # path('get_user/', views.get_user, name='get-user')
]