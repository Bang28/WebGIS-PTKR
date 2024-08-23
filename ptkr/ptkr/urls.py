from django.urls import path
from .views.views_auth import signIn, signOut
from .views.views_beranda import beranda
from .views.views_detail import detailRumah, detailBencana
from .views.views_kalkulasi_satu import satuLantai
from .views.views_kalkulasi_dua import duaLantai
from .views.views_kalkulasi_tiga import tigaLantai
from .views.views_statistik import statistik

app_name = 'ptkr'
urlpatterns = [
    path('beranda/', beranda, name='beranda'),
    path('satu-lantai/', satuLantai, name='satu'),
    path('dua-lantai/', duaLantai, name='dua'),
    path('tiga-lantai/', tigaLantai, name='tiga'),
    path('statistik/', statistik, name='statistik'),
    path('detail/<id>', detailRumah, name='detail-rumah'),
    path('sign-in/', signIn, name='sign-in'),
    path('sign-out/', signOut, name='sign-out'),
    path('detail-bencana/<id>', detailBencana, name='detail-bencana'),
]
