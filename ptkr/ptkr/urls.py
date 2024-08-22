from django.urls import path
from .views import beranda, satuLantai, duaLantai, tigaLantai, statistik, detail, signIn, signOut

app_name = 'ptkr'
urlpatterns = [
    path('beranda/', beranda, name='beranda'),
    path('satu-lantai/', satuLantai, name='satu'),
    path('dua-lantai/', duaLantai, name='dua'),
    path('tiga-lantai/', tigaLantai, name='tiga'),
    path('statistik/', statistik, name='statistik'),
    path('detail/<id>', detail, name='detail'),
    path('sign-in/', signIn, name='sign-in'),
    path('sign-out/', signOut, name='sign-out'),
]
