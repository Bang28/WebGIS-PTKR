from django.shortcuts import render
from ptkr.models.models_bangunan import Bangunan
from ptkr.models.models_bencana import Bencana

def dataBencana(request):

    # Ambil parameter filter dari request GET
    bencana_id = request.GET.get('bencana')  # Mengambil filter berdasarkan bencana
    kategori = request.GET.get('kategori')  # Mengambil filter berdasarkan tingkat kerusakan
    tahun = request.GET.get('tahun')  # Mengambil filter berdasarkan tahun
    
    all_data = Bangunan.objects.all().order_by('-publish')
    all_bencana = Bencana.objects.all().order_by('-tanggal_terjadi')

    # Filter berdasarkan bencana jika ada
    if bencana_id and bencana_id != "Bencana":
        all_data = all_data.filter(bencana_id=bencana_id)

    # Filter berdasarkan kategori (tingkat kerusakan) jika ada
    if kategori and kategori != "Kategori":
        all_data = all_data.filter(tingkat_kerusakan=kategori)

    # Filter berdasarkan tahun jika ada
    if tahun and tahun != "":
        all_bencana = all_data.filter(bencana__tanggal_terjadi__year=tahun)

    per_bencana = []
    for bencana in all_bencana:
        rumah_terdampak = Bangunan.objects.filter(bencana=bencana)

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
        'all_data': all_data,
        'per_bencana': per_bencana,
        'all_bencana': all_bencana,
    }
    return render(request, 'data-bencana.html', context)