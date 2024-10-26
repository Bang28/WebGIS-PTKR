from django.urls import path
from .views.views_index import index
from .views.views_dash_peta import dashPeta, get_titik_lokasi
from .views.views_data_bencana import dataBencana
from .views.views_detail import detailInfo, detailBencana
from .views.views_kalkulasi_satu import satuLantai
from .views.views_kalkulasi_dua import duaLantai
from .views.views_kalkulasi_tiga import tigaLantai
from .views.views_statistik_bencana import statistikBencana
from .views.views_email import email

app_name = 'ptkr'
urlpatterns = [
    path('', index, name="index"),
    path('dashboard-peta/', dashPeta, name='dash-peta'),
    path('get-titik-lokasi/<int:bencana_id>/', get_titik_lokasi, name='get_titik_lokasi'),
    path('form-input/satu-lantai/', satuLantai, name='satu'),
    path('form-input/dua-lantai/', duaLantai, name='dua'),
    path('form-input/tiga-lantai/', tigaLantai, name='tiga'),
    path('statistik-bencana/', statistikBencana, name='statistik-bencana'),
    path('data-bencana/detail-informasi/<id>', detailInfo, name='detail-informasi'),
    path('detail-bencana/<id>', detailBencana, name='detail-bencana'),
    path('data-bencana/', dataBencana, name='data-bencana'),
    path('email/', email, name='email'),
]
