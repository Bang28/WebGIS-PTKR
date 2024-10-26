from django.shortcuts import render
from ptkr.models.models_shp import Shp
from ptkr.models.models_bangunan import Bangunan
from ptkr.models.models_bencana import Bencana
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from django.urls import reverse

def get_titik_lokasi(request, bencana_id):
    """menampilkan point di map tanpa reload halaman"""
    try:
        rumah_terdampak = Bangunan.objects.filter(bencana_id=bencana_id)
        lokasi_rumah = []

        for rumah in rumah_terdampak:
            lokasi_rumah.append({
                'pemilik_rumah': rumah.pemilik_rumah,
                'foto': rumah.foto.url,
                'bencana':rumah.bencana.jenis_bencana,
                'tanggal':rumah.bencana.tanggal_terjadi.date(),
                'lat': rumah.lat,
                'lng': rumah.long,
                'tingkat_kerusakan': rumah.tingkat_kerusakan,
                'url': reverse('ptkr:detail-informasi', args=[rumah.id])
            })

        return JsonResponse({'lokasi_rumah': lokasi_rumah})
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Data tidak ditemukan'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def dashPeta(request):
    """Render point to map"""

    tahun_sekarang = datetime.now().year
    
    shp = Shp.objects.all()
    point = Bangunan.objects.filter(bencana__tanggal_terjadi__year=tahun_sekarang)
    list_bencana = Bencana.objects.all().order_by('-tanggal_terjadi')

    # mengambil data rumah terdampak berdasarkan bencana
    per_bencana = []
    for bencana in list_bencana:
        # Memastikan 'bencana' adalah instance yang valid dari model Bencana
        rumah_terdampak = Bangunan.objects.filter(bencana=bencana)

        # Periksa jika ada rumah terdampak yang terkait
        if rumah_terdampak.exists():
            ringan = rumah_terdampak.filter(tingkat_kerusakan='Rusak Ringan').count()
            sedang = rumah_terdampak.filter(tingkat_kerusakan='Rusak Sedang').count()
            berat = rumah_terdampak.filter(tingkat_kerusakan='Rusak Berat').count()
            all = rumah_terdampak.count()

            per_bencana.append({
                'bencana': bencana,
                'tanggal_terjadi': bencana.tanggal_terjadi,
                'lokasi': f"Kel. {rumah_terdampak.first().kelurahan}, Dk. {rumah_terdampak.first().dusun}",
                'ringan': ringan,
                'sedang': sedang,
                'berat': berat,
                'all':all,
                'id': bencana.id
            })

    context = {
        'shp': shp,
        'point': point,
        'artikel': per_bencana,
    }
    return render(request, 'dashboard-peta.html', context)