from django.shortcuts import render, redirect
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