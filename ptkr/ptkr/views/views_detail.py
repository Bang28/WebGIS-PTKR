from django.shortcuts import render, get_object_or_404
from ptkr.models.models_bangunan import Bangunan
from ptkr.models.models_bencana import Bencana

def detailBencana(request, id):
    """fungsi menampilkan detail bencana"""
    bencana = get_object_or_404(Bencana, id=id)
    rumah_terdampak = Bangunan.objects.filter(bencana=bencana)
    first = rumah_terdampak.first()

    # Ambil parameter filter dari request GET
    kategori = request.GET.get('kategori')  # Mengambil filter berdasarkan tingkat kerusakan

    # Filter berdasarkan kategori (tingkat kerusakan) jika ada
    if kategori and kategori != "Kategori":
        rumah_terdampak = rumah_terdampak.filter(tingkat_kerusakan=kategori)

    
    context = {
        'bencana': bencana,
        'rumah_terdampak': rumah_terdampak,
        'first': first,
    }
    return render(request, 'detail-bencana.html', context)

def detailInfo(request, id):
    """fungsi menampilkan detail rumah terdampak bencana"""
    detail = Bangunan.objects.get(id=id)
    context = {
        'detail': detail,
    }
    return render(request, 'detail-informasi.html', context)