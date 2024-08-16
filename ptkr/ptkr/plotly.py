from django.shortcuts import render
from .models.ptkr import Bencana, RumahTerdampak
import plotly.express as px
from django.db.models import Count
from plotly.offline import plot
import plotly.graph_objs as go

# Create your views here.

def generate_statistik_charts():
    # Query untuk statistik rumah terdampak berdasarkan tingkat kerusakan dan tanggal publikasi
    kerusakan_data = RumahTerdampak.objects.values('tingkat_kerusakan', 'publish').annotate(jumlah=Count('id'))

    # Query untuk statistik kejadian bencana berdasarkan jenis bencana dan tanggal
    bencana_data = Bencana.objects.values('jenis_bencana', 'tanggal_terjadi').annotate(jumlah=Count('id'))

    # Query untuk statistik rumah terdampak berdasarkan bencana yang terjadi, termasuk tingkat kerusakan
    rumah_terdampak_bencana = RumahTerdampak.objects.values('bencana__jenis_bencana', 'bencana__tanggal_terjadi', 'tingkat_kerusakan').annotate(jumlah=Count('id'))

    # Membuat bar chart untuk Statistik Rumah Terdampak Bencana
    tingkat_kerusakan = [entry['tingkat_kerusakan'] for entry in kerusakan_data]
    jumlah_rumah = [entry['jumlah'] for entry in kerusakan_data]
    tanggal_publish = [entry['publish'].strftime('%Y-%m-%d') for entry in kerusakan_data]
    kerusakan_chart = go.Bar(x=tanggal_publish, y=jumlah_rumah, name='Rumah Terdampak', text=tingkat_kerusakan)


    layout_kerusakan = go.Layout(
        title="Statistik Rumah Terdampak Bencana",
        xaxis=dict(title="Tanggal Publikasi"),
        yaxis=dict(title="Jumlah Rumah"),
        # hovermode='x'
    )
    fig_kerusakan = go.Figure(data=[kerusakan_chart], layout=layout_kerusakan)
    kerusakan_plot_div = plot(fig_kerusakan, output_type='div')

    # Membuat bar chart untuk Statistik Kejadian Bencana
    jenis_bencana = [entry['jenis_bencana'] for entry in bencana_data]
    tanggal_bencana = [entry['tanggal_terjadi'].strftime('%Y-%m-%d') for entry in bencana_data]
    jumlah_bencana = [entry['jumlah'] for entry in bencana_data]
    bencana_chart = go.Bar(x=tanggal_bencana, y=jumlah_bencana, name='Kejadian Bencana', text=jenis_bencana)

    layout_bencana = go.Layout(
        title="Statistik Kejadian Bencana",
        xaxis=dict(title="Tanggal Kejadian Bencana"),
        yaxis=dict(title="Jumlah Bencana"),
        # hovermode='x'
    )
    fig_bencana = go.Figure(data=[bencana_chart], layout=layout_bencana)
    bencana_plot_div = plot(fig_bencana, output_type='div')

    # Membuat bar chart untuk Statistik Rumah Terdampak Berdasarkan Bencana
    bencana_types = [entry['bencana__jenis_bencana'] for entry in rumah_terdampak_bencana]
    jumlah_rumah_terdampak = [entry['jumlah'] for entry in rumah_terdampak_bencana]
    tanggal_terjadi = [entry['bencana__tanggal_terjadi'].strftime('%Y-%m-%d') for entry in rumah_terdampak_bencana]
    tingkat_kerusakan_text = [f"{entry['tingkat_kerusakan']} - {entry['jumlah']} rumah" for entry in rumah_terdampak_bencana]

    # Menentukan warna bar berdasarkan tingkat kerusakan
    warna_bars = [
        'blue' if entry['tingkat_kerusakan'] == 'Rusak ringan' else 
        'yellow' if entry['tingkat_kerusakan'] == 'Rusak sedang' else 
        'red' for entry in rumah_terdampak_bencana
    ]
    
    rumah_terdampak_chart = go.Bar(
        x=bencana_types, 
        y=jumlah_rumah_terdampak, 
        name='Rumah Terdampak',  
        text=[f"{entry['bencana__tanggal_terjadi'].strftime('%d-%m-%Y')} - {tk}" for entry, tk in zip(rumah_terdampak_bencana, tingkat_kerusakan_text)],
        marker=dict(color=warna_bars)  # Mengatur warna bar berdasarkan tingkat kerusakan
    )

    layout_rumah_terdampak = go.Layout(
        title="Statistik Rumah Terdampak Berdasarkan Bencana",
        xaxis=dict(title="Jenis Bencana"),
        yaxis=dict(title="Jumlah Rumah Terdampak"),
        # hovermode='x'
    )
    fig_rumah_terdampak = go.Figure(data=[rumah_terdampak_chart], layout=layout_rumah_terdampak)
    rumah_terdampak_plot_div = plot(fig_rumah_terdampak, output_type='div')

    return kerusakan_plot_div, bencana_plot_div, rumah_terdampak_plot_div


def generate_statistik_charts_1():
    # Query untuk statistik rumah terdampak berdasarkan tingkat kerusakan dan tanggal publikasi
    kerusakan_data = RumahTerdampak.objects.values('tingkat_kerusakan', 'publish').annotate(jumlah=Count('id'))

    # Query untuk statistik kejadian bencana berdasarkan jenis bencana dan tanggal
    bencana_data = Bencana.objects.values('jenis_bencana', 'tanggal_terjadi').annotate(jumlah=Count('id'))

    # Query untuk statistik rumah terdampak berdasarkan bencana yang terjadi, termasuk tingkat kerusakan
    rumah_terdampak_bencana = RumahTerdampak.objects.values(
        'bencana__jenis_bencana', 'bencana__tanggal_terjadi', 'tingkat_kerusakan'
    ).annotate(jumlah=Count('id'))

    # Membuat bar chart untuk Statistik Rumah Terdampak Bencana
    tingkat_kerusakan = [entry['tingkat_kerusakan'] for entry in kerusakan_data]
    jumlah_rumah = [entry['jumlah'] for entry in kerusakan_data]
    tanggal_publish = [entry['publish'].strftime('%Y-%m-%d') for entry in kerusakan_data]

    kerusakan_chart = go.Bar(x=tanggal_publish, y=jumlah_rumah, name='Rumah Terdampak', text=tingkat_kerusakan)

    layout_kerusakan = go.Layout(
        title="Statistik Rumah Terdampak Bencana",
        xaxis=dict(title="Tanggal Publikasi"),
        yaxis=dict(title="Jumlah Rumah"),
        hovermode='x'
    )
    fig_kerusakan = go.Figure(data=[kerusakan_chart], layout=layout_kerusakan)
    kerusakan_plot_div = plot(fig_kerusakan, output_type='div')

    # Membuat bar chart untuk Statistik Kejadian Bencana berdasarkan jenis dan tanggal
    jenis_bencana = [entry['jenis_bencana'] for entry in bencana_data]
    tanggal_bencana = [entry['tanggal_terjadi'].strftime('%Y-%m-%d') for entry in bencana_data]
    jumlah_bencana = [entry['jumlah'] for entry in bencana_data]
    
    bencana_chart = go.Bar(x=tanggal_bencana, y=jumlah_bencana, name='Kejadian Bencana', text=jenis_bencana)

    layout_bencana = go.Layout(
        title="Statistik Kejadian Bencana",
        xaxis=dict(title="Tanggal Kejadian"),
        yaxis=dict(title="Jumlah Bencana"),
        hovermode='x'
    )
    fig_bencana = go.Figure(data=[bencana_chart], layout=layout_bencana)
    bencana_plot_div = plot(fig_bencana, output_type='div')

    # Mengelompokkan data berdasarkan tingkat kerusakan
    data_ringan = rumah_terdampak_bencana.filter(tingkat_kerusakan='Rusak ringan')
    data_sedang = rumah_terdampak_bencana.filter(tingkat_kerusakan='Rusak sedang')
    data_berat = rumah_terdampak_bencana.filter(tingkat_kerusakan='Rusak berat')

    # Membuat trace untuk setiap tingkat kerusakan
    bar_ringan = go.Bar(
        x=[entry['bencana__jenis_bencana'] for entry in data_ringan],
        y=[entry['jumlah'] for entry in data_ringan],
        name='Ringan',
        text=[f"{entry['bencana__tanggal_terjadi'].strftime('%Y-%m-%d')} - Ringan" for entry in data_ringan],
        marker=dict(color='blue')
    )
    
    bar_sedang = go.Bar(
        x=[entry['bencana__jenis_bencana'] for entry in data_sedang],
        y=[entry['jumlah'] for entry in data_sedang],
        name='Sedang',
        text=[f"{entry['bencana__tanggal_terjadi'].strftime('%Y-%m-%d')} - Sedang" for entry in data_sedang],
        marker=dict(color='yellow')
    )
    
    bar_berat = go.Bar(
        x=[entry['bencana__jenis_bencana'] for entry in data_berat],
        y=[entry['jumlah'] for entry in data_berat],
        name='Berat',
        text=[f"{entry['bencana__tanggal_terjadi'].strftime('%Y-%m-%d')} - Berat" for entry in data_berat],
        marker=dict(color='red')
    )

    # Menggabungkan semua trace ke dalam satu Figure
    fig_rumah_terdampak = go.Figure(data=[bar_ringan, bar_sedang, bar_berat])

    layout_rumah_terdampak = go.Layout(
        title="Statistik Rumah Terdampak Berdasarkan Bencana",
        xaxis=dict(title="Jenis Bencana"),
        yaxis=dict(title="Jumlah Rumah Terdampak"),
        barmode='group',  # Mengatur agar bar tidak bertumpuk melainkan berdampingan
        # hovermode='x'
    )
    fig_rumah_terdampak.update_layout(layout_rumah_terdampak)
    rumah_terdampak_plot_div = plot(fig_rumah_terdampak, output_type='div')

    return kerusakan_plot_div, bencana_plot_div, rumah_terdampak_plot_div

def charts(request):
    kerusakan_chart, bencana_chart, rumah_terdampak_chart = generate_statistik_charts()

    return render(request, 'charts.html', {
        'kerusakan_chart': kerusakan_chart,
        'bencana_chart': bencana_chart,
        'rumah_terdampak_chart': rumah_terdampak_chart,
    })