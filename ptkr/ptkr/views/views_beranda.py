from django.shortcuts import render
from ptkr.models.shp import Shp
from ptkr.models.ptkr import RumahTerdampak

def beranda(request):
    shp = Shp.objects.all()
    point = RumahTerdampak.objects.all()

    context = {
        'shp': shp,
        'point': point
    }
    return render(request, 'beranda.html', context)