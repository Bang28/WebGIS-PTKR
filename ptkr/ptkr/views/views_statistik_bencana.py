from django.shortcuts import render
from django.db.models import Count
from django.db.models.functions import TruncMonth, ExtractYear
from collections import defaultdict
import json
from ptkr.models.models_bangunan import Bangunan
from ptkr.models.models_bencana import Bencana
from datetime import datetime

def get_statistik_rumah_terdampak():
    """Mengambil statistik rumah terdampak berdasarkan bencana yang terjadi"""
    # Query jumlah rumah terdampak berdasarkan jenis bencana
    return Bangunan.objects.values(
        'bencana__jenis_bencana', 'bencana__tanggal_terjadi', 'tingkat_kerusakan'
    ).annotate(jumlah=Count('id')).order_by('bencana__jenis_bencana', 'tingkat_kerusakan')

def get_statistik_kejadian_bencana():
    """Mengambil statistik kejadian bencana berdasarkan tanggal kejadian"""
    # Query jumlah kejadian bencana berdasarkan tanggal terjadi
    return Bencana.objects.values('tanggal_terjadi', 'jenis_bencana').annotate(jumlah=Count('id')).order_by('tanggal_terjadi')

def get_statistik_kejadian_bencana_per_kelurahan():
    """Mengambil statistik kejadian bencana berdasarkan tempat kejadian (kelurahan)"""
    # Query jumlah kejadian bencana per kelurahan termasuk jenis bencana
    return Bencana.objects.values('lokasi_bencana', 'jenis_bencana').annotate(jumlah=Count('id')).order_by('lokasi_bencana', 'jenis_bencana')

def get_statistik_kejadian_bencana_per_bulan_jenis():
    """Mengambil statistik kejadian bencana berdasarkan bulan dan jenis bencana"""
    # Query jumlah kejadian bencana perbulan berdasarkan jenis bencana
    return Bencana.objects.annotate(month=TruncMonth('tanggal_terjadi')).values('month', 'jenis_bencana').annotate(jumlah=Count('id')).order_by('month', 'jenis_bencana')

def get_statistik_kejadian_bencana_per_tahun():
    """Mengambil statistik kejadian bencana berdasarkan tahun dan jenis"""
    # Query jumlah kejadian bencana tahunan per jenis
    return Bencana.objects.annotate(year=ExtractYear('tanggal_terjadi')).values('year', 'jenis_bencana').annotate(jumlah=Count('id')).order_by('year', 'jenis_bencana')

def prepare_data_rumah_terdampak_bencana(rumah_terdampak_bencana):
    """Menyiapkan data chart untuk statistik kerusakan rumah terdampak bencana"""
    
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

    return chart_data_kerusakan_rumah

def prepare_data_bencana_per_tanggal(kejadian_bencana):
    """Menyiapkan data chart untuk statistik kejadian bencana per tanggal terjadi"""
    # Menyiapkan data untuk chart
    data_per_tanggal = defaultdict(lambda: defaultdict(int))
    jenis_bencana_list = [choice[0] for choice in Bencana.JENIS_BENCANA_CHOICES]
    for entry in kejadian_bencana:
        tanggal = entry['tanggal_terjadi'].strftime('%Y-%m-%d')
        jenis = entry['jenis_bencana']
        jumlah = entry['jumlah']
        data_per_tanggal[tanggal][jenis] = jumlah

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

    return chart_data_kejadian_bencana

def prepare_bencana_per_kelurahan(kejadian_bencana_per_kelurahan):
    """Menyiapkan data untuk chart statistik kejadian bencana per kelurahan"""
    
    # Organisasi data untuk digunakan dalam chart
    kelurahan_dict = {}
    for entry in kejadian_bencana_per_kelurahan:
        kelurahan = entry['lokasi_bencana']
        jenis_bencana = entry['jenis_bencana']
        jumlah = entry['jumlah']
        
        if kelurahan not in kelurahan_dict:
            kelurahan_dict[kelurahan] = {'jumlah': 0, 'jenis_bencana': []}
        
        kelurahan_dict[kelurahan]['jumlah'] += jumlah
        kelurahan_dict[kelurahan]['jenis_bencana'].append(f"{jenis_bencana} ({jumlah})")

    # Persiapkan data untuk chart
    chart_data_kelurahan = {
        'labels': list(kelurahan_dict.keys()),
        'datasets': [{
            'label': 'Jumlah Kejadian Bencana per Kelurahan',
            'data': [kelurahan_dict[kel]['jumlah'] for kel in kelurahan_dict],
            'backgroundColor': 'rgba(54, 162, 235, 0.5)',
            'borderColor': 'rgba(54, 162, 235, 1)',
            'borderWidth': 1
        }],
        'jenis_bencana': {kel: kelurahan_dict[kel]['jenis_bencana'] for kel in kelurahan_dict}
    }

    return chart_data_kelurahan

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

def prepare_tahunan_bar_chart_data(kejadian_bencana_per_tahun):
    """Menyiapkan data untuk bar chart statistik kejadian bencana per tahun"""

    # Mengorganisir data per tahun dengan jumlah kejadian per jenis bencana
    data_per_tahun = {}
    for entry in kejadian_bencana_per_tahun:
        tahun = entry['year']
        jenis = entry['jenis_bencana']
        jumlah = entry['jumlah']
        if tahun not in data_per_tahun:
            data_per_tahun[tahun] = {}
        data_per_tahun[tahun][jenis] = jumlah

    labels = []
    data = []
    tooltip_data = []

    for year, jenis_data in data_per_tahun.items():
        labels.append(str(year))
        total = sum(jenis_data.values())
        data.append(total)
        tooltip_data.append(jenis_data)

    # Menyiapkan data untuk Chart.js
    chart_data_tahunan = {
        'labels': labels,
        'datasets': [{
            'data': data,
            'tooltip_data': tooltip_data,  # Tambahkan data untuk tooltip
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

def statistikBencana(request):
    """Fungsi utama untuk menampilkan statistik bencana dan rumah terdampak"""

    # Mendapatkan parameter filter tahun dari request GET
    tahun = request.GET.get('tahun', None)

    # Mendapatkan tahun saat ini
    tahun_sekarang = datetime.now().year

    # Jika tidak ada filter tahun, gunakan tahun sekarang
    if tahun is None:
        tahun = tahun_sekarang
    else:
        # Mengonversi tahun ke integer jika ada
        tahun = int(tahun)

    # Memfilter berdasarkan tahun jika dipilih
    if tahun:
        rumah_terdampak_bencana = get_statistik_rumah_terdampak().filter(bencana__tanggal_terjadi__year=tahun)
        kejadian_bencana = get_statistik_kejadian_bencana().filter(tanggal_terjadi__year=tahun)
        kejadian_bencana_per_kelurahan = get_statistik_kejadian_bencana_per_kelurahan().filter(tanggal_terjadi__year=tahun)
        kejadian_bencana_per_bulan_jenis = get_statistik_kejadian_bencana_per_bulan_jenis().filter(tanggal_terjadi__year=tahun)
        kejadian_bencana_per_tahun = get_statistik_kejadian_bencana_per_tahun()
    else:
        # Jika tidak ada filter tahun, ambil semua data
        rumah_terdampak_bencana = get_statistik_rumah_terdampak()
        kejadian_bencana = get_statistik_kejadian_bencana()
        kejadian_bencana_per_kelurahan = get_statistik_kejadian_bencana_per_kelurahan()
        kejadian_bencana_per_bulan_jenis = get_statistik_kejadian_bencana_per_bulan_jenis()
        kejadian_bencana_per_tahun = get_statistik_kejadian_bencana_per_tahun()
    
    # akses ke prepare data chart
    chart_data_kerusakan_rumah = prepare_data_rumah_terdampak_bencana(rumah_terdampak_bencana)
    chart_data_kejadian_bencana = prepare_data_bencana_per_tanggal(kejadian_bencana)
    chart_data_kelurahan = prepare_bencana_per_kelurahan(kejadian_bencana_per_kelurahan)
    chart_data_bulanan_jenis = prepare_bulanan_chart_data_per_jenis(kejadian_bencana_per_bulan_jenis)
    chart_data_tahunan = prepare_tahunan_bar_chart_data(kejadian_bencana_per_tahun)
    
    context = {
        'chart_data_kerusakan_rumah': json.dumps(chart_data_kerusakan_rumah),
        'chart_data_kejadian_bencana': json.dumps(chart_data_kejadian_bencana),
        'chart_data_bencana_kelurahan': json.dumps(chart_data_kelurahan),
        'chart_data_bulanan': json.dumps(chart_data_bulanan_jenis),
        'chart_data_tahunan': json.dumps(chart_data_tahunan),
    }
    
    return render(request, 'statistik-bencana.html', context)
