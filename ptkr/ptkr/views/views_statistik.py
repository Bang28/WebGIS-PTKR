from django.shortcuts import render
from django.db.models import Count
from django.db.models.functions import TruncMonth, ExtractYear
from collections import defaultdict
import json
from ptkr.models.ptkr import Bencana, RumahTerdampak

def get_data_rumah_terdampak():
    """Mengambil semua data rumah terdampak bencana"""
    return RumahTerdampak.objects.all().order_by('-publish')

def get_data_list_bencana():
    """Mengambil semua data bencana"""
    return Bencana.objects.all().order_by('-tanggal_terjadi')

def get_statistik_rumah_terdampak():
    """Mengambil statistik rumah terdampak berdasarkan bencana yang terjadi"""
    return RumahTerdampak.objects.values(
        'bencana__jenis_bencana', 'bencana__tanggal_terjadi', 'tingkat_kerusakan'
    ).annotate(jumlah=Count('id')).order_by('bencana__jenis_bencana', 'tingkat_kerusakan')

def get_statistik_kejadian_bencana():
    """Mengambil statistik kejadian bencana berdasarkan tanggal kejadian dan jenis bencana"""
    return Bencana.objects.values('tanggal_terjadi', 'jenis_bencana').annotate(jumlah=Count('id')).order_by('tanggal_terjadi')

def get_statistik_kejadian_bencana_per_bulan_jenis():
    """Mengambil statistik kejadian bencana berdasarkan bulan dan jenis bencana"""
    return Bencana.objects.annotate(month=TruncMonth('tanggal_terjadi')).values('month', 'jenis_bencana').annotate(jumlah=Count('id')).order_by('month', 'jenis_bencana')

def get_statistik_kejadian_bencana_per_tahun():
    """Mengambil statistik kejadian bencana berdasarkan tahun"""
    return Bencana.objects.annotate(year=ExtractYear('tanggal_terjadi')).values('year').annotate(jumlah=Count('id')).order_by('year')

def prepare_data_for_chart(rumah_terdampak_bencana, kejadian_bencana):
    """Menyiapkan data untuk chart berdasarkan rumah terdampak dan kejadian bencana"""
    
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

    return kerusakan_rumah_labels, data_ringan, data_sedang, data_berat, data_per_tanggal, jenis_bencana_list

def prepare_chart_data(kerusakan_rumah_labels, data_ringan, data_sedang, data_berat, data_per_tanggal, jenis_bencana_list):
    """Menyiapkan data untuk Chart.js"""

    # statistik kerusakan rumah akibat kejadian bencana per tanggal kejadian
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

    # statistik kejadian bencana per tanggal kejadian
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

    return chart_data_kerusakan_rumah, chart_data_kejadian_bencana

def prepare_bulanan_chart_data_per_jenis(kejadian_bencana_per_bulan_jenis):
    """Menyiapkan data untuk chart statistik kejadian bencana berdasarkan bulan dan jenis bencana"""

    data_per_jenis = defaultdict(lambda: defaultdict(int))
    for entry in kejadian_bencana_per_bulan_jenis:
        month = entry['month'].strftime('%Y-%m')
        jenis = entry['jenis_bencana']
        jumlah = entry['jumlah']
        data_per_jenis[month][jenis] = jumlah

    # Menyiapkan data untuk Chart.js
    labels = sorted(data_per_jenis.keys())
    jenis_bencana_list = sorted(set(jenis for jenis_dict in data_per_jenis.values() for jenis in jenis_dict.keys()))

    datasets = []
    background_colors = {
        'Gempa Bumi': 'rgba(255, 99, 132, 0.5)',
        'Banjir': 'rgba(54, 162, 235, 0.5)',
        'Topan': 'rgba(255, 206, 86, 0.5)',
        'Kebakaran': 'rgba(75, 192, 192, 0.5)',
        'Tanah Bergerak': 'rgba(153, 102, 255, 0.5)',
        'Tanah Longsor': 'rgba(255, 159, 64, 0.5)'
    }

    for jenis_bencana in jenis_bencana_list:
        data = [data_per_jenis[month].get(jenis_bencana, 0) for month in labels]
        datasets.append({
            'label': jenis_bencana,
            'data': data,
            'backgroundColor': background_colors.get(jenis_bencana, 'rgba(0, 0, 0, 0.5)')
        })

    chart_data_bulanan = {
        'labels': labels,
        'datasets': datasets
    }
    
    return chart_data_bulanan

def prepare_tahunan_pie_chart_data(kejadian_bencana_per_tahun):
    """Menyiapkan data untuk pie chart statistik kejadian bencana per tahun"""

    labels = []
    data = []

    for entry in kejadian_bencana_per_tahun:
        labels.append(str(entry['year']))
        data.append(entry['jumlah'])

    # Menyiapkan data untuk Chart.js
    chart_data_tahunan = {
        'labels': labels,
        'datasets': [{
            'data': data,
            'backgroundColor': [
                'rgba(255, 99, 132, 0.5)',
                'rgba(54, 162, 235, 0.5)',
                'rgba(255, 206, 86, 0.5)',
                'rgba(75, 192, 192, 0.5)',
                'rgba(153, 102, 255, 0.5)',
                'rgba(255, 159, 64, 0.5)'
            ],
            'hoverBackgroundColor': [
                'rgba(255, 99, 132, 0.7)',
                'rgba(54, 162, 235, 0.7)',
                'rgba(255, 206, 86, 0.7)',
                'rgba(75, 192, 192, 0.7)',
                'rgba(153, 102, 255, 0.7)',
                'rgba(255, 159, 64, 0.7)'
            ]
        }]
    }

    return chart_data_tahunan

def get_per_bencana_data(list_bencana):
    """Mengambil data rumah terdampak berdasarkan bencana"""
    
    per_bencana = []
    for bencana in list_bencana:
        rumah_terdampak = RumahTerdampak.objects.filter(bencana=bencana)

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
    return per_bencana

def statistik(request):
    """Fungsi utama untuk menampilkan statistik bencana dan rumah terdampak"""
    
    all_data = get_data_rumah_terdampak()
    list_bencana = get_data_list_bencana()
    rumah_terdampak_bencana = get_statistik_rumah_terdampak()
    kejadian_bencana = get_statistik_kejadian_bencana()
    kejadian_bencana_per_bulan_jenis = get_statistik_kejadian_bencana_per_bulan_jenis()
    kejadian_bencana_per_tahun = get_statistik_kejadian_bencana_per_tahun()
    
    kerusakan_rumah_labels, data_ringan, data_sedang, data_berat, data_per_tanggal, jenis_bencana_list = prepare_data_for_chart(rumah_terdampak_bencana, kejadian_bencana)
    chart_data_kerusakan_rumah, chart_data_kejadian_bencana = prepare_chart_data(kerusakan_rumah_labels, data_ringan, data_sedang, data_berat, data_per_tanggal, jenis_bencana_list)
    chart_data_bulanan_jenis = prepare_bulanan_chart_data_per_jenis(kejadian_bencana_per_bulan_jenis)
    chart_data_tahunan = prepare_tahunan_pie_chart_data(kejadian_bencana_per_tahun)
    per_bencana = get_per_bencana_data(list_bencana)
    
    context = {
        'list_semua_data': all_data,
        'list_per_bencana': per_bencana,
        'chart_data_kerusakan_rumah': json.dumps(chart_data_kerusakan_rumah),
        'chart_data_kejadian_bencana': json.dumps(chart_data_kejadian_bencana),
        'chart_data_bulanan': json.dumps(chart_data_bulanan_jenis),
        'chart_data_tahunan': json.dumps(chart_data_tahunan),
    }
    
    return render(request, 'statistik.html', context)
