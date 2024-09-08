from django.shortcuts import render, get_object_or_404
from ptkr.models.ptkr import Bencana, Bangunan

def detailBencana(request, id):
    """fungsi menampilkan detail bencana"""
    bencana = get_object_or_404(Bencana, id=id)
    rumah_terdampak = Bangunan.objects.filter(bencana=bencana)
    first = rumah_terdampak.first()
    context = {
        'bencana': bencana,
        'rumah_terdampak': rumah_terdampak,
        'first': first,
    }
    return render(request, 'detail-bencana.html', context)

def detailRumah(request, id):
    """fungsi menampilkan detail rumah terdampak bencana"""
    detail = Bangunan.objects.get(id=id)
    context = {
        'detail': detail,
    }
    return render(request, 'detail.html', context)