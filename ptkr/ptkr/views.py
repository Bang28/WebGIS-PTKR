from django.shortcuts import render
from .models.shp import Shp

# Create your views here.
def statistik(request):
    return render(request, 'statistik.html')

def tigaLantai(request):
    return render(request, 'forms/tiga-lantai.html')

def duaLantai(request):
    return render(request, 'forms/dua-lantai.html')

def satuLantai(request):
    return render(request, 'forms/satu-lantai.html')

def beranda(request):
    shp = Shp.objects.all()
    context = {
        'shp': shp
    }
    return render(request, 'beranda.html', context)