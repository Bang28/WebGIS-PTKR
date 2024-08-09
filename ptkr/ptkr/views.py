from django.shortcuts import render
from .models.shp import Shp

# Create your views here.
def statistik(request):
    return render(request, 'statistik.html')

def tigaLantai(request):
    return render(request, 'forms/tigaLantai.html')

def duaLantai(request):
    return render(request, 'forms/duaLantai.html')

def satuLantai(request):
    return render(request, 'forms/satuLantai.html')

def beranda(request):
    shp = Shp.objects.all()
    context = {
        'shp': shp
    }
    return render(request, 'beranda.html', context)