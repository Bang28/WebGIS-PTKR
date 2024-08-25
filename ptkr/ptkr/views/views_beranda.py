from django.shortcuts import render
from ptkr.models.shp import Shp
from ptkr.models.ptkr import RumahTerdampak, Bencana

def beranda(request):
    shp = Shp.objects.all()
    point = RumahTerdampak.objects.all()
    list_bencana = Bencana.objects.all().order_by('tanggal_terjadi')

    # mengambil data rumah terdampak berdasarkan bencana
    per_bencana = []
    for bencana in list_bencana:
        # Memastikan 'bencana' adalah instance yang valid dari model Bencana
        rumah_terdampak = RumahTerdampak.objects.filter(bencana=bencana)

        # Periksa jika ada rumah terdampak yang terkait
        if rumah_terdampak.exists():
            ringan = rumah_terdampak.filter(tingkat_kerusakan='Rusak Ringan').count()
            sedang = rumah_terdampak.filter(tingkat_kerusakan='Rusak Sedang').count()
            berat = rumah_terdampak.filter(tingkat_kerusakan='Rusak Berat').count()

            per_bencana.append({
                'bencana': bencana,
                'tanggal_terjadi': bencana.tanggal_terjadi,
                'daerah': f"Kec. {rumah_terdampak.first().kecamatan}, Kel. {rumah_terdampak.first().kelurahan}, Dk. {rumah_terdampak.first().dusun}",
                'ringan': ringan,
                'sedang': sedang,
                'berat': berat,
                'id': bencana.id
            })

    context = {
        'shp': shp,
        'point': point,
        'artikel': per_bencana,
    }
    return render(request, 'beranda.html', context)