from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.gis import admin
from import_export.admin import ImportExportModelAdmin
from ptkr.models.models_shp import Shp
from ptkr.models.models_bangunan import Bangunan
from ptkr.models.models_bencana import Bencana
from ptkr.models.models_struktur_bangunan import StrukturBangunan
from ptkr.models.models_arsitektur_bangunan import ArsitekturBangunan
from ptkr.models.models_utilitas_bangunan import UtilitasBangunan

# Register your models here.
@admin.register(Shp)
class AdminShp(admin.ModelAdmin):
    list_display = ['name','description','uploaded_date']

class CustomGeoAdmin(admin.GISModelAdmin):
    gis_widget_kwargs = {
        'attrs' : {
            'default_zoom': 13,
            'default_lat': -7.204620857883746,
            'default_lon':  109.06153678894044,
            # 'map_template': {}
        }
    }

@admin.register(Bencana)
class AdminBencana(admin.ModelAdmin):
    list_display = ['jenis_bencana','tanggal_terjadi']
    search_fields = ['jenis_bencana', 'tanggal_terjadi']
    list_filter = ['jenis_bencana', 'tanggal_terjadi']
    list_per_page = 10


class AdminStrukturBangunan(admin.StackedInline):
    model = StrukturBangunan

class AdminArsitekturBangunan(admin.StackedInline):
    model = ArsitekturBangunan

class AdminUtilitasBangunan(admin.StackedInline):
    model = UtilitasBangunan

@admin.register(Bangunan)
class AdminRumah(ImportExportModelAdmin, CustomGeoAdmin):
    list_display = ['pemilik_rumah','tipe_bangunan','kelurahan','jenis_bencana','tingkat_kerusakan']
    search_fields = ['pemilik_rumah','lat','long']
    list_filter = ['publish', 'tingkat_kerusakan', 'tipe_bangunan', 'kelurahan', 'bencana']
    readonly_fields = ['preview_img', 'tingkat_kerusakan', 'publish']
    list_per_page = 10

    inlines = [
        AdminStrukturBangunan,
        AdminArsitekturBangunan,
        AdminUtilitasBangunan,
    ]

    def jenis_bencana(self, obj):
        return obj.bencana.jenis_bencana