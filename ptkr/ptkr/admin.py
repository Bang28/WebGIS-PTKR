from django.contrib import admin
from django.contrib.gis import admin
from .models.shp import Shp
from .models.ptkr import Bencana, RumahTerdampak

# Register your models here.
@admin.register(Shp)
class AdminShp(admin.ModelAdmin):
    list_display = [
        'name',
        'description',
        'uploaded_date'
    ]

class CustomGeoAdmin(admin.GISModelAdmin):
    gis_widget_kwargs = {
        'attrs' : {
            'default_zoom': 10,
            'default_lat': -7.050,
            'default_lon': 108.891,
            # 'map_template': {}
        }
    }

@admin.register(Bencana)
class AdminBencana(admin.ModelAdmin):
    list_display = [
        'jenis_bencana',
        'tanggal_terjadi'
    ]

@admin.register(RumahTerdampak)
class AdminRumah(CustomGeoAdmin):
    list_display = [
        'pemilik_rumah',
        'kelurahan',
        'koordinat',
        'tingkat_kerusakan'
    ]
