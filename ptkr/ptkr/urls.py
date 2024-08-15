from django.urls import path
from .views import beranda, satuLantai, duaLantai, tigaLantai, statistik, detail

app_name = 'ptkr'
urlpatterns = [
    path('beranda/', beranda, name='beranda'),
    path('satu-lantai/', satuLantai, name='satu'),
    path('dua-lantai/', duaLantai, name='dua'),
    path('tiga-lantai/', tigaLantai, name='tiga'),
    path('statistik/', statistik, name='statistik'),
    path('detail/<id>', detail, name='detail'),
]
