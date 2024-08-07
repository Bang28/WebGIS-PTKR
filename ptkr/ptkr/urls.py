from django.urls import path
from .views import index

app_name = 'ptkr'
urlpatterns = [
    path('', index, name='index')
]
