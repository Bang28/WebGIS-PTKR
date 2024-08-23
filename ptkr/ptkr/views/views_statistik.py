from django.shortcuts import render
from django.db.models import Count
from ptkr.models.ptkr import Bencana, RumahTerdampak
from collections import defaultdict
import json


def statistik(request):
    """fungsi menampilkan statistik bencana dan rumah terdampak"""

    # ambil semua data rumah terdampak bencana
    all_data = RumahTerdampak.objects.all().order_by('-publish')
    list_bencana = Bencana.objects.all().order_by('-tanggal_terjadi')
    # Query untuk statistik rumah terdampak berdasarkan bencana yang terjadi, termasuk tingkat kerusakan dan tanggal kejadian
    rumah_terdampak_bencana = RumahTerdampak.objects.values(
        'bencana__jenis_bencana', 'bencana__tanggal_terjadi', 'tingkat_kerusakan'
    ).annotate(jumlah=Count('id')).order_by('bencana__jenis_bencana', 'tingkat_kerusakan')

    # Query statistik kejadian bencana berdasarkan tanggal kejadian dan jenis bencana
    kejadian_bencana = Bencana.objects.values('tanggal_terjadi', 'jenis_bencana').annotate(jumlah=Count('id')).order_by('tanggal_terjadi')

    # Menyiapkan list unik dari 'jenis_bencana' + 'tanggal_terjadi'
    kerusakan_rumah_labels = sorted(
        set(f"{entry['bencana__jenis_bencana']} ({entry['bencana__tanggal_terjadi'].strftime('%Y-%m-%d')})" 
            for entry in rumah_terdampak_bencana)
    )

    # Memisahkan data berdasarkan tingkat kerusakan
    data_ringan = [0] * len(kerusakan_rumah_labels)
    data_sedang = [0] * len(kerusakan_rumah_labels)
    data_berat = [0] * len(kerusakan_rumah_labels)
    
    for entry in rumah_terdampak_bencana:
        label = f"{entry['bencana__jenis_bencana']} ({entry['bencana__tanggal_terjadi'].strftime('%Y-%m-%d')})"
        index = kerusakan_rumah_labels.index(label)
        if entry['tingkat_kerusakan'] == 'Rusak Ringan':
            data_ringan[index] = entry['jumlah']
        elif entry['tingkat_kerusakan'] == 'Rusak Sedang':
            data_sedang[index] = entry['jumlah']
        elif entry['tingkat_kerusakan'] == 'Rusak Berat':
            data_berat[index] = entry['jumlah']

    # Menyiapkan data untuk chart
    data_per_tanggal = defaultdict(lambda: defaultdict(int))
    jenis_bencana_list = [choice[0] for choice in Bencana.JENIS_BENCANA_CHOICES]
    for entry in kejadian_bencana:
        tanggal = entry['tanggal_terjadi'].strftime('%Y-%m-%d')
        jenis = entry['jenis_bencana']
        jumlah = entry['jumlah']
        data_per_tanggal[tanggal][jenis] = jumlah
    
    # Siapkan data untuk Chart.js
    chart_data_kerusakan_rumah = {
        'labels': kerusakan_rumah_labels,
        'datasets': [
            {
                'label': 'Rusak Ringan',
                'data': data_ringan,
                'backgroundColor': 'gray',
            },
            {
                'label': 'Rusak Sedang',
                'data': data_sedang,
                'backgroundColor': 'yellow',
            },
            {
                'label': 'Rusak Berat',
                'data': data_berat,
                'backgroundColor': 'red',
            },
        ]
    }

    # Membentuk struktur data untuk Chart.js
    labels = sorted(data_per_tanggal.keys())
    datasets = []

    # Warna berbeda untuk setiap jenis bencana
    background_colors = {
        'Gempa Bumi': 'rgba(255, 99, 132, 0.5)',
        'Banjir': 'rgba(54, 162, 235, 0.5)',
        'Topan': 'rgba(255, 206, 86, 0.5)',
        'Kebakaran': 'rgba(75, 192, 192, 0.5)',
        'Tanah Bergerak': 'rgba(153, 102, 255, 0.5)',
        'Tanah Longsor': 'rgba(255, 159, 64, 0.5)'
    }

    for jenis_bencana in jenis_bencana_list:
        dataset = {
            'label': jenis_bencana,
            'data': [],
            'backgroundColor': background_colors[jenis_bencana] 
        }
        for tanggal in labels:
            dataset['data'].append(data_per_tanggal[tanggal][jenis_bencana])
        datasets.append(dataset)

    chart_data_kejadian_bencana = {
        'labels': labels,
        'datasets': datasets
    }

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
        else:
            per_bencana.append({
                'bencana': bencana,
                'tanggal_terjadi': bencana.tanggal_terjadi,
                'daerah': 'N/A',
                'ringan': 0,
                'sedang': 0,
                'berat': 0,
                'id': bencana.id
            })

    
    context = {
        'list_semua_data': all_data,
        'list_per_bencana': per_bencana,
        'chart_data_kerusakan_rumah': json.dumps(chart_data_kerusakan_rumah),
        'chart_data_kejadian_bencana': json.dumps(chart_data_kejadian_bencana),
    }
    return render(request, 'statistik.html', context)