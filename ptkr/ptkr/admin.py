from django.contrib import admin
from .models.shp import Shp

# Register your models here.
@admin.register(Shp)
class AdminShp(admin.ModelAdmin):
    list_display = [
        'name',
        'description',
        'uploaded_date'
    ]
