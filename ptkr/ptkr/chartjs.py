from django.shortcuts import render, redirect
from collections import defaultdict
from .models.shp import Shp
from .models.ptkr import Bencana, RumahTerdampak
import plotly.express as px
from django.db.models import Count
from plotly.offline import plot
import plotly.graph_objs as go
import json

def statistik(request):
    """fungsi menampilkan statistik bencana dan rumah terdampak"""
    list_rumah = RumahTerdampak.objects.all()
    # Query untuk statistik rumah terdampak berdasarkan bencana yang terjadi, termasuk tingkat kerusakan dan tanggal kejadian
    rumah_terdampak_bencana = RumahTerdampak.objects.values(
        'bencana__jenis_bencana', 'bencana__tanggal_terjadi', 'tingkat_kerusakan'
    ).annotate(jumlah=Count('id')).order_by('bencana__jenis_bencana', 'tingkat_kerusakan')

    # Menyiapkan list unik dari 'jenis_bencana' + 'tanggal_terjadi'
    jenis_bencana_labels = sorted(
        set(f"{entry['bencana__jenis_bencana']} ({entry['bencana__tanggal_terjadi'].strftime('%Y-%m-%d')})" 
            for entry in rumah_terdampak_bencana)
    )

    # Memisahkan data berdasarkan tingkat kerusakan
    data_ringan = [0] * len(jenis_bencana_labels)
    data_sedang = [0] * len(jenis_bencana_labels)
    data_berat = [0] * len(jenis_bencana_labels)

    for entry in rumah_terdampak_bencana:
        label = f"{entry['bencana__jenis_bencana']} ({entry['bencana__tanggal_terjadi'].strftime('%Y-%m-%d')})"
        index = jenis_bencana_labels.index(label)
        if entry['tingkat_kerusakan'] == 'Rusak ringan':
            data_ringan[index] = entry['jumlah']
        elif entry['tingkat_kerusakan'] == 'Rusak sedang':
            data_sedang[index] = entry['jumlah']
        elif entry['tingkat_kerusakan'] == 'Rusak berat':
            data_berat[index] = entry['jumlah']

    # Siapkan data untuk Chart.js
    chart_data = {
        'labels': jenis_bencana_labels,
        'datasets': [
            {
                'label': 'Ringan',
                'data': data_ringan,
                'backgroundColor': 'blue',
            },
            {
                'label': 'Sedang',
                'data': data_sedang,
                'backgroundColor': 'yellow',
            },
            {
                'label': 'Berat',
                'data': data_berat,
                'backgroundColor': 'red',
            },
        ]
    }
    
    context = {
        'list_rumah': list_rumah,
        'statistik_kerusakan_rumah': chart_data,
    }
    return render(request, 'statistik.html', context)

def statistik(request):
    """fungsi menampilkan statistik bencana dan rumah terdampak"""
    list_rumah = RumahTerdampak.objects.all()
    # Query untuk statistik rumah terdampak berdasarkan bencana yang terjadi, termasuk tingkat kerusakan dan tanggal kejadian
    rumah_terdampak_bencana = RumahTerdampak.objects.values(
        'bencana__jenis_bencana', 'bencana__tanggal_terjadi', 'tingkat_kerusakan'
    ).annotate(jumlah=Count('id')).order_by('bencana__jenis_bencana', 'tingkat_kerusakan')

    # Menyiapkan list unik dari 'jenis_bencana' + 'tanggal_terjadi'
    jenis_bencana_labels = sorted(
        set(f"{entry['bencana__jenis_bencana']} ({entry['bencana__tanggal_terjadi'].strftime('%Y-%m-%d')})" 
            for entry in rumah_terdampak_bencana)
    )

    # Memisahkan data berdasarkan tingkat kerusakan
    data_ringan = [0] * len(jenis_bencana_labels)
    data_sedang = [0] * len(jenis_bencana_labels)
    data_berat = [0] * len(jenis_bencana_labels)

    for entry in rumah_terdampak_bencana:
        label = f"{entry['bencana__jenis_bencana']} ({entry['bencana__tanggal_terjadi'].strftime('%Y-%m-%d')})"
        index = jenis_bencana_labels.index(label)
        if entry['tingkat_kerusakan'] == 'Rusak ringan':
            data_ringan[index] = entry['jumlah']
        elif entry['tingkat_kerusakan'] == 'Rusak sedang':
            data_sedang[index] = entry['jumlah']
        elif entry['tingkat_kerusakan'] == 'Rusak berat':
            data_berat[index] = entry['jumlah']

    # Siapkan data untuk Chart.js
    chart_data = {
        'labels': jenis_bencana_labels,
        'datasets': [
            {
                'label': 'Ringan',
                'data': data_ringan,
                'backgroundColor': 'blue',
            },
            {
                'label': 'Sedang',
                'data': data_sedang,
                'backgroundColor': 'yellow',
            },
            {
                'label': 'Berat',
                'data': data_berat,
                'backgroundColor': 'red',
            },
        ]
    }
    
    context = {
        'list_rumah': list_rumah,
        'chart_data': json.dumps(chart_data),
    }
    return render(request, 'statistik.html', context)

# render to template white js (method 1/2 sama)
# <script>
#     // Data chart yang dikirim dari view
#     const chartData = JSON.parse('{{ chart_data|escapejs }}');

#     const ctx = document.getElementById('rumahTerdampakChart').getContext('2d');
#     const rumahTerdampakChart = new Chart(ctx, {
#         type: 'bar',
#         data: chartData,
#         options: {
#             responsive: true,
#             scales: {
#                 x: {
#                     beginAtZero: true,
#                     title: {
#                         display: true,
#                         text: 'Jenis Bencana'
#                     }
#                 },
#                 y: {
#                     beginAtZero: true,
#                     title: {
#                         display: true,
#                         text: 'Jumlah Rumah Terdampak'
#                     }
#                 }
#             },
#             plugins: {
#                 tooltip: {
#                     callbacks: {
#                         label: function(tooltipItem) {
#                             return tooltipItem.dataset.label + ': ' + tooltipItem.raw + ' rumah';
#                         }
#                     }
#                 }
#             }
#         }
#     });
# </script>


def statistik(request):
    """fungsi menampilkan statistik bencana dan rumah terdampak"""

    # ambil semua data rumah terdampak bencana
    all_data = RumahTerdampak.objects.all().order_by('-publish')
    list_bencana = Bencana.objects.all().order_by('-tanggal_terjadi')
    # Query untuk statistik rumah terdampak berdasarkan bencana yang terjadi, termasuk tingkat kerusakan dan tanggal kejadian
    rumah_terdampak_bencana = RumahTerdampak.objects.values(
        'bencana__jenis_bencana', 'bencana__tanggal_terjadi', 'tingkat_kerusakan'
    ).annotate(jumlah=Count('id')).order_by('bencana__jenis_bencana', 'tingkat_kerusakan')

    # Statistik kejadian bencana berdasarkan tanggal kejadian
    # kejadian_bencana = Bencana.objects.values('tanggal_terjadi', 'jenis_bencana').annotate(jumlah=Count('id')).order_by('tanggal_terjadi')
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

    # Menyiapkan data untuk statistik kejadian bencana
    # tanggal_labels = [entry['tanggal_terjadi'].strftime('%Y-%m-%d') for entry in kejadian_bencana]
    # jenis_bencana_data = [entry['jumlah'] for entry in kejadian_bencana]

    # Menyiapkan data untuk chart
    data_per_tanggal = defaultdict(lambda: defaultdict(int))
    jenis_bencana_list = [choice[0] for choice in Bencana.JENIS_BENCANA_CHOICES]
    for entry in kejadian_bencana:
        tanggal = entry['tanggal_terjadi'].strftime('%Y-%m-%d')
        jenis = entry['jenis_bencana']
        jumlah = entry['jumlah']
        data_per_tanggal[tanggal][jenis] = jumlah
    

    # Warna-warna unik untuk setiap jenis bencana
    # bencana_colors = {
    #     'Gempa Bumi': 'rgba(54, 162, 235, 0.6)',
    #     'Banjir': 'rgba(75, 192, 192, 0.6)',
    #     'Topan': 'rgba(255, 159, 64, 0.6)',
    #     'Kebakaran': 'rgba(255, 99, 132, 0.6)',
    #     'Tanah Bergerak': 'rgba(153, 102, 255, 0.6)',
    #     'Tanah Longsor': 'rgba(255, 206, 86, 0.6)',
    # }

    # # Menghitung data untuk setiap jenis bencana
    # datasets_bencana = []
    # for jenis_bencana, color in bencana_colors.items():
    #     data_bencana = [entry['jumlah'] if entry['jenis_bencana'] == jenis_bencana else 0 for entry in kejadian_bencana]
    #     datasets_bencana.append({
    #         'label': jenis_bencana,
    #         'data': data_bencana,
    #         'backgroundColor': color,
    #     })

    # Siapkan data untuk Chart.js
    chart_data_kerusakan_rumah = {
        'labels': kerusakan_rumah_labels,
        'datasets': [
            {
                'label': 'Ringan',
                'data': data_ringan,
                'backgroundColor': 'gray',
            },
            {
                'label': 'Sedang',
                'data': data_sedang,
                'backgroundColor': 'yellow',
            },
            {
                'label': 'Berat',
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

    # chart_data_kejadian_bencana = {
    #     'labels': tanggal_labels,
    #     'datasets': datasets_bencana
    # }

    # chart_data_kejadian_bencana = {
    #     'labels': tanggal_labels,
    #     'datasets': [
    #         {
    #             'label': 'Jumlah Kejadian',
    #             'data': jenis_bencana_data,
    #             'backgroundColor': 'green',
    #         }
    #     ]
    # }

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



# hasil final
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
    
    context = {
        'list_semua_data': all_data,
        'list_per_bencana': per_bencana,
        'chart_data_kerusakan_rumah': json.dumps(chart_data_kerusakan_rumah),
        'chart_data_kejadian_bencana': json.dumps(chart_data_kejadian_bencana),
    }
    return render(request, 'statistik.html', context)