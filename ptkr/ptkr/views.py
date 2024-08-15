from django.shortcuts import render, redirect
from .models.shp import Shp
from .models.ptkr import Bencana, RumahTerdampak

# Create your views here.
def detail(request, id):
    """fungsi menampilkan detail rumah terdampak"""
    detail = RumahTerdampak.objects.get(id=id)
    context = {
        'detail': detail
    }
    return render(request, 'detail.html', context)

def statistik(request):
    """fungsi menampilkan statistik bencana dan rumah terdampak"""
    list_rumah = RumahTerdampak.objects.all()
    context = {
        'list_rumah': list_rumah
    }
    return render(request, 'statistik.html', context)

def tigaLantai(request):
    """fungsi kalkulasi kerusakan bangunan tipe satu lantau"""
    list_bencana = Bencana.objects.all()

    if request.method == 'POST':
        # ambil nilai input dari form post
        # info dasar
        pemilik_rumah = request.POST.get('pemilik_rumah')
        tipe_bangunan = "Tiga lantai"
        provinsi = request.POST.get('provinsi')
        kota = request.POST.get('kota')
        kecamatan = request.POST.get('kecamatan')
        kelurahan = request.POST.get('kelurahan')
        dusun = request.POST.get('dusun')
        rw = request.POST.get('rw')
        rt = request.POST.get('rt')
        bencana = int(request.POST.get('bencana'))
        foto = request.FILES.get('foto')
        
        # tahap 1 (nilai pengamatan visual)
        ket_pondasi = request.POST.get('ket_pondasi')
        ket_kolom = request.POST.get('ket_kolom')
        ket_balok = request.POST.get('ket_balok')
        ket_plantai = request.POST.get('ket_plantai')
        ket_tangga = request.POST.get('ket_tangga')
        ket_atap = request.POST.get('ket_atap')
        ket_dinding = request.POST.get('ket_dinding')

        # tahap 2 (nilai volume kerusakan)
        # struktur bangunan
        vk_pondasi = float(request.POST.get('vk_pondasi'))
        # kolom
        j_kolom = float(request.POST.get('j_kolom'))
        kolom_tr = float(request.POST.get('kolom_tr'))
        kolom_rsr = float(request.POST.get('kolom_rsr'))
        kolom_rr = float(request.POST.get('kolom_rr'))
        kolom_rs = float(request.POST.get('kolom_rs'))
        kolom_rb = float(request.POST.get('kolom_rb'))
        kolom_rsb = float(request.POST.get('kolom_rsb'))
        kolom_kts = float(request.POST.get('kolom_kts'))
        # balok
        j_balok = float(request.POST.get('j_balok'))
        balok_tr = float(request.POST.get('balok_tr'))
        balok_rsr = float(request.POST.get('balok_rsr'))
        balok_rr = float(request.POST.get('balok_rr'))
        balok_rs = float(request.POST.get('balok_rs'))
        balok_rb = float(request.POST.get('balok_rb'))
        balok_rsb = float(request.POST.get('balok_rsb'))
        balok_kts = float(request.POST.get('balok_kts'))
        # plat lantai
        j_plantai = float(request.POST.get('j_plantai'))
        plantai_tr = float(request.POST.get('plantai_tr'))
        plantai_rsr = float(request.POST.get('plantai_rsr'))
        plantai_rr = float(request.POST.get('plantai_rr'))
        plantai_rs = float(request.POST.get('plantai_rs'))
        plantai_rb = float(request.POST.get('plantai_rb'))
        plantai_rsb = float(request.POST.get('plantai_rsb'))
        plantai_kts = float(request.POST.get('plantai_kts'))
        # tangga
        j_tangga = float(request.POST.get('j_tangga'))
        tangga_tr = float(request.POST.get('tangga_tr'))
        tangga_rsr = float(request.POST.get('tangga_rsr'))
        tangga_rr = float(request.POST.get('tangga_rr'))
        tangga_rs = float(request.POST.get('tangga_rs'))
        tangga_rb = float(request.POST.get('tangga_rb'))
        tangga_rsb = float(request.POST.get('tangga_rsb'))
        tangga_kts = float(request.POST.get('tangga_kts'))
        # atap
        v_atap = 1.00
        atap_tr = float(request.POST.get('atap_tr'))
        atap_rsr = float(request.POST.get('atap_rsr'))
        atap_rr = float(request.POST.get('atap_rr'))
        atap_rs = float(request.POST.get('atap_rs'))
        atap_rb = float(request.POST.get('atap_rb'))
        atap_rsb = float(request.POST.get('atap_rsb'))
        atap_kts = float(request.POST.get('atap_kts'))
        # arsitektur bangunan
        # dinding
        v_dinding = 1.00
        dinding_tr = float(request.POST.get('dinding_tr'))
        dinding_rsr = float(request.POST.get('dinding_rsr'))
        dinding_rr = float(request.POST.get('dinding_rr'))
        dinding_rs = float(request.POST.get('dinding_rs'))
        dinding_rb = float(request.POST.get('dinding_rb'))
        dinding_rsb = float(request.POST.get('dinding_rsb'))
        dinding_kts = float(request.POST.get('dinding_kts'))
        # plafon
        v_plafon = 1.00
        plafon_tr = float(request.POST.get('plafon_tr'))
        plafon_rsr = float(request.POST.get('plafon_rsr'))
        plafon_rr = float(request.POST.get('plafon_rr'))
        plafon_rs = float(request.POST.get('plafon_rs'))
        plafon_rb = float(request.POST.get('plafon_rb'))
        plafon_rsb = float(request.POST.get('plafon_rsb'))
        plafon_kts = float(request.POST.get('plafon_kts'))
        # lantai
        v_lantai = 1.00
        lantai_tr = float(request.POST.get('lantai_tr'))
        lantai_rsr = float(request.POST.get('lantai_rsr'))
        lantai_rr = float(request.POST.get('lantai_rr'))
        lantai_rs = float(request.POST.get('lantai_rs'))
        lantai_rb = float(request.POST.get('lantai_rb'))
        lantai_rsb = float(request.POST.get('lantai_rsb'))
        lantai_kts = float(request.POST.get('lantai_kts'))
        # kusen
        j_kusen = float(request.POST.get('j_kusen'))
        kusen_tr = float(request.POST.get('kusen_tr'))
        kusen_rsr = float(request.POST.get('kusen_rsr'))
        kusen_rr = float(request.POST.get('kusen_rr'))
        kusen_rs = float(request.POST.get('kusen_rs'))
        kusen_rb = float(request.POST.get('kusen_rb'))
        kusen_rsb = float(request.POST.get('kusen_rsb'))
        kusen_kts = float(request.POST.get('kusen_kts'))
        # pintu
        j_pintu = float(request.POST.get('j_pintu'))
        pintu_tr = float(request.POST.get('pintu_tr'))
        pintu_rsr = float(request.POST.get('pintu_rsr'))
        pintu_rr = float(request.POST.get('pintu_rr'))
        pintu_rs = float(request.POST.get('pintu_rs'))
        pintu_rb = float(request.POST.get('pintu_rb'))
        pintu_rsb = float(request.POST.get('pintu_rsb'))
        pintu_kts = float(request.POST.get('pintu_kts'))
        # jendela
        j_jendela = float(request.POST.get('j_jendela'))
        jendela_tr = float(request.POST.get('jendela_tr'))
        jendela_rsr = float(request.POST.get('jendela_rsr'))
        jendela_rr = float(request.POST.get('jendela_rr'))
        jendela_rs = float(request.POST.get('jendela_rs'))
        jendela_rb = float(request.POST.get('jendela_rb'))
        jendela_rsb = float(request.POST.get('jendela_rsb'))
        jendela_kts = float(request.POST.get('jendela_kts'))
        # fplafon
        v_fplafon = 1.00
        fplafon_tr = float(request.POST.get('fplafon_tr'))
        fplafon_rsr = float(request.POST.get('fplafon_rsr'))
        fplafon_rr = float(request.POST.get('fplafon_rr'))
        fplafon_rs = float(request.POST.get('fplafon_rs'))
        fplafon_rb = float(request.POST.get('fplafon_rb'))
        fplafon_rsb = float(request.POST.get('fplafon_rsb'))
        fplafon_kts = float(request.POST.get('fplafon_kts'))
        # fdinding
        v_fdinding = 1.00
        fdinding_tr = float(request.POST.get('fdinding_tr'))
        fdinding_rsr = float(request.POST.get('fdinding_rsr'))
        fdinding_rr = float(request.POST.get('fdinding_rr'))
        fdinding_rs = float(request.POST.get('fdinding_rs'))
        fdinding_rb = float(request.POST.get('fdinding_rb'))
        fdinding_rsb = float(request.POST.get('fdinding_rsb'))
        fdinding_kts = float(request.POST.get('fdinding_kts'))
        # fkupin
        v_fkupin = 1.00
        fkupin_tr = float(request.POST.get('fkupin_tr'))
        fkupin_rsr = float(request.POST.get('fkupin_rsr'))
        fkupin_rr = float(request.POST.get('fkupin_rr'))
        fkupin_rs = float(request.POST.get('fkupin_rs'))
        fkupin_rb = float(request.POST.get('fkupin_rb'))
        fkupin_rsb = float(request.POST.get('fkupin_rsb'))
        fkupin_kts = float(request.POST.get('fkupin_kts'))
        # utilitas
        vk_listrik = float(request.POST.get('vk_listrik'))
        vk_air = float(request.POST.get('vk_air'))
        # drainase
        v_drainase = float(request.POST.get('v_drainase'))
        drainase_tr = float(request.POST.get('drainase_tr'))
        drainase_rsr = float(request.POST.get('drainase_rsr'))
        drainase_rr = float(request.POST.get('drainase_rr'))
        drainase_rs = float(request.POST.get('drainase_rs'))
        drainase_rb = float(request.POST.get('drainase_rb'))
        drainase_rsb = float(request.POST.get('drainase_rsb'))
        drainase_kts = float(request.POST.get('drainase_kts'))
        # koordinat
        lat = float(request.POST.get('lat'))
        long = float(request.POST.get('long'))

        tk_komponen = [0.00, 0.20, 0.35, 0.50, 0.70, 0.80, 1.00] #nilai tingkat kerusakan komponen

        # calc & pembobotan untuk mencari tingkat kerusakan komponen struktur bangunan
        bobot_struktur = [0.10, 0.13, 0.12, 0.07, 0.03, 0.10] #nilai bobot dari komponen struktur
        tk_pondasi = vk_pondasi * bobot_struktur[0] #tingkat kerusakan komponen pondasi
        tk_kolom = ((kolom_tr * tk_komponen[0] / j_kolom) + (kolom_rsr * tk_komponen[1] / j_kolom) + (kolom_rr * tk_komponen[2] / j_kolom) + (kolom_rs * tk_komponen[3] / j_kolom) + (kolom_rb * tk_komponen[4] / j_kolom) + (kolom_rsb * tk_komponen[5] / j_kolom) + (kolom_kts * tk_komponen[6] / j_kolom)) * bobot_struktur[1] #tingkat kerusakan komponen kolom
        tk_balok = ((balok_tr * tk_komponen[0] / j_balok) + (balok_rsr * tk_komponen[1] / j_balok) + (balok_rr * tk_komponen[2] / j_balok) + (balok_rs * tk_komponen[3] / j_balok) + (balok_rb * tk_komponen[4] / j_balok) + (balok_rsb * tk_komponen[5] / j_balok) + (balok_kts * tk_komponen[6] / j_balok)) * bobot_struktur[2] #tingkat kerusakan komponen balok
        tk_plantai = ((plantai_tr * tk_komponen[0] / j_plantai) + (plantai_rsr * tk_komponen[1] / j_plantai) + (plantai_rr * tk_komponen[2] / j_plantai) + (plantai_rs * tk_komponen[3] / j_plantai) + (plantai_rb * tk_komponen[4] / j_plantai) + (plantai_rsb * tk_komponen[5] / j_plantai) + (plantai_kts * tk_komponen[6] / j_plantai)) * bobot_struktur[3] #tingkat kerusakan komponen plantai
        tk_tangga = ((tangga_tr * tk_komponen[0] / j_tangga) + (tangga_rsr * tk_komponen[1] / j_tangga) + (tangga_rr * tk_komponen[2] / j_tangga) + (tangga_rs * tk_komponen[3] / j_tangga) + (tangga_rb * tk_komponen[4] / j_tangga) + (tangga_rsb * tk_komponen[5] / j_tangga) + (tangga_kts * tk_komponen[6] / j_tangga)) * bobot_struktur[4] #tingkat kerusakan komponen tangga
        tk_atap = ((atap_tr * tk_komponen[0] / v_atap) + (atap_rsr * tk_komponen[1] / v_atap) + (atap_rr * tk_komponen[2] / v_atap) + (atap_rs * tk_komponen[3] / v_atap) + (atap_rb * tk_komponen[4] / v_atap) + (atap_rsb * tk_komponen[5] / v_atap) + (atap_kts * tk_komponen[6] / v_atap)) * bobot_struktur[5] #tingkat kerusakan komponen atap

        # calc & pembobotan untuk mencari tingkat kerusakan komponen arsitektur bangunan
        bobot_arsitektur = [0.15, 0.06, 0.09, 0.015, 0.01, 0.0125, 0.01, 0.05, 0.01] #nilai dari bobot komponen arsitektur
        tk_dinding = ((dinding_tr * tk_komponen[0] / v_dinding) + (dinding_rsr * tk_komponen[1] / v_dinding) + (dinding_rr * tk_komponen[2] / v_dinding) + (dinding_rs * tk_komponen[3] / v_dinding) + (dinding_rb * tk_komponen[4] / v_dinding) + (dinding_rsb * tk_komponen[5] / v_dinding) + (dinding_kts * tk_komponen[6] / v_dinding)) * bobot_arsitektur[0] #tingkat kerusakan komponen dinding
        tk_plafon = ((plafon_tr * tk_komponen[0] / v_plafon) + (plafon_rsr * tk_komponen[1] / v_plafon) + (plafon_rr * tk_komponen[2] / v_plafon) + (plafon_rs * tk_komponen[3] / v_plafon) + (plafon_rb * tk_komponen[4] / v_plafon) + (plafon_rsb * tk_komponen[5] / v_plafon) + (plafon_kts * tk_komponen[6] / v_plafon)) * bobot_arsitektur[1] #tingkat kerusakan komponen plafon
        tk_lantai = ((lantai_tr * tk_komponen[0] / v_lantai) + (lantai_rsr * tk_komponen[1] / v_lantai) + (lantai_rr * tk_komponen[2] / v_lantai) + (lantai_rs * tk_komponen[3] / v_lantai) + (lantai_rb * tk_komponen[4] / v_lantai) + (lantai_rsb * tk_komponen[5] / v_lantai) + (lantai_kts * tk_komponen[6] / v_lantai)) * bobot_arsitektur[2] #tingkat kerusakan komponen lantai
        tk_kusen = ((kusen_tr * tk_komponen[0] / j_kusen) + (kusen_rsr * tk_komponen[1] / j_kusen) + (kusen_rr * tk_komponen[2] / j_kusen) + (kusen_rs * tk_komponen[3] / j_kusen) + (kusen_rb * tk_komponen[4] / j_kusen) + (kusen_rsb * tk_komponen[5] / j_kusen) + (kusen_kts * tk_komponen[6] / j_kusen)) * bobot_arsitektur[3] #tingkat kerusakan komponen kusen
        tk_pintu = ((pintu_tr * tk_komponen[0] / j_pintu) + (pintu_rsr * tk_komponen[1] / j_pintu) + (pintu_rr * tk_komponen[2] / j_pintu) + (pintu_rs * tk_komponen[3] / j_pintu) + (pintu_rb * tk_komponen[4] / j_pintu) + (pintu_rsb * tk_komponen[5] / j_pintu) + (pintu_kts * tk_komponen[6] / j_pintu)) * bobot_arsitektur[4] #tingkat kerusakan komponen pintu
        tk_jendela = ((jendela_tr * tk_komponen[0] / j_jendela) + (jendela_rsr * tk_komponen[1] / j_jendela) + (jendela_rr * tk_komponen[2] / j_jendela) + (jendela_rs * tk_komponen[3] / j_jendela) + (jendela_rb * tk_komponen[4] / j_jendela) + (jendela_rsb * tk_komponen[5] / j_jendela) + (jendela_kts * tk_komponen[6] / j_jendela)) * bobot_arsitektur[5] #tingkat kerusakan komponen jendela
        tk_fplafon = ((fplafon_tr * tk_komponen[0] / v_fplafon) + (fplafon_rsr * tk_komponen[1] / v_fplafon) + (fplafon_rr * tk_komponen[2] / v_fplafon) + (fplafon_rs * tk_komponen[3] / v_fplafon) + (fplafon_rb * tk_komponen[4] / v_fplafon) + (fplafon_rsb * tk_komponen[5] / v_fplafon) + (fplafon_kts * tk_komponen[6] / v_fplafon)) * bobot_arsitektur[6] #tingkat kerusakan komponen fplafon
        tk_fdinding = ((fdinding_tr * tk_komponen[0] / v_fdinding) + (fdinding_rsr * tk_komponen[1] / v_fdinding) + (fdinding_rr * tk_komponen[2] / v_fdinding) + (fdinding_rs * tk_komponen[3] / v_fdinding) + (fdinding_rb * tk_komponen[4] / v_fdinding) + (fdinding_rsb * tk_komponen[5] / v_fdinding) + (fdinding_kts * tk_komponen[6] / v_fdinding)) * bobot_arsitektur[7] #tingkat kerusakan komponen fdinding
        tk_fkupin = ((fkupin_tr * tk_komponen[0] / v_fkupin) + (fkupin_rsr * tk_komponen[1] / v_fkupin) + (fkupin_rr * tk_komponen[2] / v_fkupin) + (fkupin_rs * tk_komponen[3] / v_fkupin) + (fkupin_rb * tk_komponen[4] / v_fkupin) + (fkupin_rsb * tk_komponen[5] / v_fkupin) + (fkupin_kts * tk_komponen[6] / v_fkupin)) * bobot_arsitektur[8] #tingkat kerusakan komponen fkupin
        
        # calc & pembobotan untuk mencari tingkat kerusakan komponen utilitas bangunan
        bobot_utilitas = [0.02, 0.01, 0.0125] #nilai bobot dari komponen utilitas
        tk_instalasi_listrik = (vk_listrik * bobot_utilitas[0]) #tingkat kerusakan instalasi listrik
        tk_air_bersih = (vk_air * bobot_utilitas[1]) #tingkat kerusakan drainase air
        tk_drainase = ((drainase_tr * tk_komponen[0] / v_drainase) + (drainase_rsr * tk_komponen[1] / v_drainase) + (drainase_rr * tk_komponen[2] / v_drainase) + (drainase_rs * tk_komponen[3] / v_drainase) + (drainase_rb * tk_komponen[4] / v_drainase) + (drainase_rsb * tk_komponen[5] / v_drainase) + (drainase_kts * tk_komponen[6] / v_drainase)) * bobot_utilitas[2] #tingkat kerusakan komponen drainase

        # calc tingkat kerusakan komponen untuk mencari total nilai kerusakan bangunan
        tk_bangunan = tk_pondasi + tk_kolom + tk_balok + tk_atap + tk_dinding + tk_plafon + tk_lantai + tk_kusen + tk_pintu + tk_jendela + tk_fplafon + tk_fdinding + tk_fkupin + tk_instalasi_listrik + tk_air_bersih + tk_drainase
        print(tk_bangunan)
        # kondisi untuk klasifikasi kerusakan berdasarkan total nilai kerusakan bangunan
        if tk_bangunan <= 0.3: #jika nilai tk_bangunan kurang dari atau sama dengan 30% = bangunan rusak ringan
            tk_bangunan = 'rusak ringan'
        elif tk_bangunan > 0.3 and tk_bangunan <= 0.45: #jika nilai tk_bangunan lebih besar dari 30% dan kurang dari atau sama dengan 40% = bangunan rusak sedang
            tk_bangunan = 'rusak sedang'
        else:
            tk_bangunan = 'rusak berat' #jika nilai tk_bangunan diatas 40% = bangunan rusak berat
        
        # simpan data kedalam model rumah terdampak 
        RumahTerdampak.objects.create(pemilik_rumah=pemilik_rumah, tipe_bangunan=tipe_bangunan, provinsi=provinsi, kota=kota, kecamatan=kecamatan,
                                      kelurahan=kelurahan, dusun=dusun, rw=rw, rt=rt, bencana=Bencana.objects.get(id=bencana), foto=foto, lat=lat, long=long, tingkat_kerusakan=tk_bangunan,
                                      ket_pondasi=ket_pondasi, ket_kolom=ket_kolom, ket_balok=ket_balok, ket_plantai=ket_plantai, ket_tangga=ket_tangga, ket_atap=ket_atap, ket_dinding=ket_dinding)
        
        # RumahTerdampak.objects.create(pemilik_rumah=pemilik_rumah, tipe_bangunan=tipe_bangunan, provinsi=provinsi, kota=kota, kecamatan=kecamatan,
        #                               kelurahan=kelurahan, dusun=dusun, rw=rw, rt=rt, bencana=Bencana.objects.get(id=bencana), foto=foto, tingkat_kerusakan=tk_bangunan,
        #                               ket_pondasi=ket_pondasi, ket_kolom=ket_kolom, ket_balok=ket_balok, ket_atap=ket_atap, ket_dinding=ket_dinding,
        #                               tk_pondasi=tk_pondasi, tk_kolom=tk_kolom, tk_balok=tk_balok, tk_atap=tk_atap,
        #                               tk_dinding=tk_dinding, tk_plafon=tk_plafon, tk_lantai=tk_lantai, tk_kusen=tk_kusen, tk_pintu=tk_pintu, tk_jendela=tk_jendela, tk_fplafon=tk_fplafon, tk_fdinding=tk_fdinding, tk_fkupin=tk_fkupin,
        #                               tk_instalasi_listrik=tk_instalasi_listrik, tk_air_bersih=tk_air_bersih, tk_drainase=tk_drainase)
        
        return redirect('ptkr:beranda')
    
    else:
        context = {
            'bencana': list_bencana,
        }
        return render(request, 'forms/tiga-lantai.html', context)
        

def duaLantai(request):
    """fungsi kalkulasi kerusakan bangunan tipe satu lantau"""
    list_bencana = Bencana.objects.all()

    if request.method == 'POST':
        # ambil nilai input dari form post
        # info dasar
        pemilik_rumah = request.POST.get('pemilik_rumah')
        tipe_bangunan = "Dua lantai"
        provinsi = request.POST.get('provinsi')
        kota = request.POST.get('kota')
        kecamatan = request.POST.get('kecamatan')
        kelurahan = request.POST.get('kelurahan')
        dusun = request.POST.get('dusun')
        rw = request.POST.get('rw')
        rt = request.POST.get('rt')
        bencana = int(request.POST.get('bencana'))
        foto = request.FILES.get('foto')
        
        # tahap 1 (nilai pengamatan visual)
        ket_pondasi = request.POST.get('ket_pondasi')
        ket_kolom = request.POST.get('ket_kolom')
        ket_balok = request.POST.get('ket_balok')
        ket_plantai = request.POST.get('ket_plantai')
        ket_tangga = request.POST.get('ket_tangga')
        ket_atap = request.POST.get('ket_atap')
        ket_dinding = request.POST.get('ket_dinding')

        # tahap 2 (nilai volume kerusakan)
        # struktur bangunan
        vk_pondasi = float(request.POST.get('vk_pondasi'))
        # kolom
        j_kolom = float(request.POST.get('j_kolom'))
        kolom_tr = float(request.POST.get('kolom_tr'))
        kolom_rsr = float(request.POST.get('kolom_rsr'))
        kolom_rr = float(request.POST.get('kolom_rr'))
        kolom_rs = float(request.POST.get('kolom_rs'))
        kolom_rb = float(request.POST.get('kolom_rb'))
        kolom_rsb = float(request.POST.get('kolom_rsb'))
        kolom_kts = float(request.POST.get('kolom_kts'))
        # balok
        j_balok = float(request.POST.get('j_balok'))
        balok_tr = float(request.POST.get('balok_tr'))
        balok_rsr = float(request.POST.get('balok_rsr'))
        balok_rr = float(request.POST.get('balok_rr'))
        balok_rs = float(request.POST.get('balok_rs'))
        balok_rb = float(request.POST.get('balok_rb'))
        balok_rsb = float(request.POST.get('balok_rsb'))
        balok_kts = float(request.POST.get('balok_kts'))
        # plat lantai
        j_plantai = float(request.POST.get('j_plantai'))
        plantai_tr = float(request.POST.get('plantai_tr'))
        plantai_rsr = float(request.POST.get('plantai_rsr'))
        plantai_rr = float(request.POST.get('plantai_rr'))
        plantai_rs = float(request.POST.get('plantai_rs'))
        plantai_rb = float(request.POST.get('plantai_rb'))
        plantai_rsb = float(request.POST.get('plantai_rsb'))
        plantai_kts = float(request.POST.get('plantai_kts'))
        # tangga
        j_tangga = float(request.POST.get('j_tangga'))
        tangga_tr = float(request.POST.get('tangga_tr'))
        tangga_rsr = float(request.POST.get('tangga_rsr'))
        tangga_rr = float(request.POST.get('tangga_rr'))
        tangga_rs = float(request.POST.get('tangga_rs'))
        tangga_rb = float(request.POST.get('tangga_rb'))
        tangga_rsb = float(request.POST.get('tangga_rsb'))
        tangga_kts = float(request.POST.get('tangga_kts'))
        # atap
        v_atap = 1.00
        atap_tr = float(request.POST.get('atap_tr'))
        atap_rsr = float(request.POST.get('atap_rsr'))
        atap_rr = float(request.POST.get('atap_rr'))
        atap_rs = float(request.POST.get('atap_rs'))
        atap_rb = float(request.POST.get('atap_rb'))
        atap_rsb = float(request.POST.get('atap_rsb'))
        atap_kts = float(request.POST.get('atap_kts'))
        # arsitektur bangunan
        # dinding
        v_dinding = 1.00
        dinding_tr = float(request.POST.get('dinding_tr'))
        dinding_rsr = float(request.POST.get('dinding_rsr'))
        dinding_rr = float(request.POST.get('dinding_rr'))
        dinding_rs = float(request.POST.get('dinding_rs'))
        dinding_rb = float(request.POST.get('dinding_rb'))
        dinding_rsb = float(request.POST.get('dinding_rsb'))
        dinding_kts = float(request.POST.get('dinding_kts'))
        # plafon
        v_plafon = 1.00
        plafon_tr = float(request.POST.get('plafon_tr'))
        plafon_rsr = float(request.POST.get('plafon_rsr'))
        plafon_rr = float(request.POST.get('plafon_rr'))
        plafon_rs = float(request.POST.get('plafon_rs'))
        plafon_rb = float(request.POST.get('plafon_rb'))
        plafon_rsb = float(request.POST.get('plafon_rsb'))
        plafon_kts = float(request.POST.get('plafon_kts'))
        # lantai
        v_lantai = 1.00
        lantai_tr = float(request.POST.get('lantai_tr'))
        lantai_rsr = float(request.POST.get('lantai_rsr'))
        lantai_rr = float(request.POST.get('lantai_rr'))
        lantai_rs = float(request.POST.get('lantai_rs'))
        lantai_rb = float(request.POST.get('lantai_rb'))
        lantai_rsb = float(request.POST.get('lantai_rsb'))
        lantai_kts = float(request.POST.get('lantai_kts'))
        # kusen
        j_kusen = float(request.POST.get('j_kusen'))
        kusen_tr = float(request.POST.get('kusen_tr'))
        kusen_rsr = float(request.POST.get('kusen_rsr'))
        kusen_rr = float(request.POST.get('kusen_rr'))
        kusen_rs = float(request.POST.get('kusen_rs'))
        kusen_rb = float(request.POST.get('kusen_rb'))
        kusen_rsb = float(request.POST.get('kusen_rsb'))
        kusen_kts = float(request.POST.get('kusen_kts'))
        # pintu
        j_pintu = float(request.POST.get('j_pintu'))
        pintu_tr = float(request.POST.get('pintu_tr'))
        pintu_rsr = float(request.POST.get('pintu_rsr'))
        pintu_rr = float(request.POST.get('pintu_rr'))
        pintu_rs = float(request.POST.get('pintu_rs'))
        pintu_rb = float(request.POST.get('pintu_rb'))
        pintu_rsb = float(request.POST.get('pintu_rsb'))
        pintu_kts = float(request.POST.get('pintu_kts'))
        # jendela
        j_jendela = float(request.POST.get('j_jendela'))
        jendela_tr = float(request.POST.get('jendela_tr'))
        jendela_rsr = float(request.POST.get('jendela_rsr'))
        jendela_rr = float(request.POST.get('jendela_rr'))
        jendela_rs = float(request.POST.get('jendela_rs'))
        jendela_rb = float(request.POST.get('jendela_rb'))
        jendela_rsb = float(request.POST.get('jendela_rsb'))
        jendela_kts = float(request.POST.get('jendela_kts'))
        # fplafon
        v_fplafon = 1.00
        fplafon_tr = float(request.POST.get('fplafon_tr'))
        fplafon_rsr = float(request.POST.get('fplafon_rsr'))
        fplafon_rr = float(request.POST.get('fplafon_rr'))
        fplafon_rs = float(request.POST.get('fplafon_rs'))
        fplafon_rb = float(request.POST.get('fplafon_rb'))
        fplafon_rsb = float(request.POST.get('fplafon_rsb'))
        fplafon_kts = float(request.POST.get('fplafon_kts'))
        # fdinding
        v_fdinding = 1.00
        fdinding_tr = float(request.POST.get('fdinding_tr'))
        fdinding_rsr = float(request.POST.get('fdinding_rsr'))
        fdinding_rr = float(request.POST.get('fdinding_rr'))
        fdinding_rs = float(request.POST.get('fdinding_rs'))
        fdinding_rb = float(request.POST.get('fdinding_rb'))
        fdinding_rsb = float(request.POST.get('fdinding_rsb'))
        fdinding_kts = float(request.POST.get('fdinding_kts'))
        # fkupin
        v_fkupin = 1.00
        fkupin_tr = float(request.POST.get('fkupin_tr'))
        fkupin_rsr = float(request.POST.get('fkupin_rsr'))
        fkupin_rr = float(request.POST.get('fkupin_rr'))
        fkupin_rs = float(request.POST.get('fkupin_rs'))
        fkupin_rb = float(request.POST.get('fkupin_rb'))
        fkupin_rsb = float(request.POST.get('fkupin_rsb'))
        fkupin_kts = float(request.POST.get('fkupin_kts'))
        # utilitas
        vk_listrik = float(request.POST.get('vk_listrik'))
        vk_air = float(request.POST.get('vk_air'))
        # drainase
        v_drainase = float(request.POST.get('v_drainase'))
        drainase_tr = float(request.POST.get('drainase_tr'))
        drainase_rsr = float(request.POST.get('drainase_rsr'))
        drainase_rr = float(request.POST.get('drainase_rr'))
        drainase_rs = float(request.POST.get('drainase_rs'))
        drainase_rb = float(request.POST.get('drainase_rb'))
        drainase_rsb = float(request.POST.get('drainase_rsb'))
        drainase_kts = float(request.POST.get('drainase_kts'))
        # koordinat
        lat = float(request.POST.get('lat'))
        long = float(request.POST.get('long'))

        tk_komponen = [0.00, 0.20, 0.35, 0.50, 0.70, 0.80, 1.00] #nilai tingkat kerusakan komponen

        # calc & pembobotan untuk mencari tingkat kerusakan komponen struktur bangunan
        bobot_struktur = [0.10, 0.13, 0.12, 0.07, 0.03, 0.10] #nilai bobot dari komponen struktur
        tk_pondasi = vk_pondasi * bobot_struktur[0] #tingkat kerusakan komponen pondasi
        tk_kolom = ((kolom_tr * tk_komponen[0] / j_kolom) + (kolom_rsr * tk_komponen[1] / j_kolom) + (kolom_rr * tk_komponen[2] / j_kolom) + (kolom_rs * tk_komponen[3] / j_kolom) + (kolom_rb * tk_komponen[4] / j_kolom) + (kolom_rsb * tk_komponen[5] / j_kolom) + (kolom_kts * tk_komponen[6] / j_kolom)) * bobot_struktur[1] #tingkat kerusakan komponen kolom
        tk_balok = ((balok_tr * tk_komponen[0] / j_balok) + (balok_rsr * tk_komponen[1] / j_balok) + (balok_rr * tk_komponen[2] / j_balok) + (balok_rs * tk_komponen[3] / j_balok) + (balok_rb * tk_komponen[4] / j_balok) + (balok_rsb * tk_komponen[5] / j_balok) + (balok_kts * tk_komponen[6] / j_balok)) * bobot_struktur[2] #tingkat kerusakan komponen balok
        tk_plantai = ((plantai_tr * tk_komponen[0] / j_plantai) + (plantai_rsr * tk_komponen[1] / j_plantai) + (plantai_rr * tk_komponen[2] / j_plantai) + (plantai_rs * tk_komponen[3] / j_plantai) + (plantai_rb * tk_komponen[4] / j_plantai) + (plantai_rsb * tk_komponen[5] / j_plantai) + (plantai_kts * tk_komponen[6] / j_plantai)) * bobot_struktur[3] #tingkat kerusakan komponen plantai
        tk_tangga = ((tangga_tr * tk_komponen[0] / j_tangga) + (tangga_rsr * tk_komponen[1] / j_tangga) + (tangga_rr * tk_komponen[2] / j_tangga) + (tangga_rs * tk_komponen[3] / j_tangga) + (tangga_rb * tk_komponen[4] / j_tangga) + (tangga_rsb * tk_komponen[5] / j_tangga) + (tangga_kts * tk_komponen[6] / j_tangga)) * bobot_struktur[4] #tingkat kerusakan komponen tangga
        tk_atap = ((atap_tr * tk_komponen[0] / v_atap) + (atap_rsr * tk_komponen[1] / v_atap) + (atap_rr * tk_komponen[2] / v_atap) + (atap_rs * tk_komponen[3] / v_atap) + (atap_rb * tk_komponen[4] / v_atap) + (atap_rsb * tk_komponen[5] / v_atap) + (atap_kts * tk_komponen[6] / v_atap)) * bobot_struktur[5] #tingkat kerusakan komponen atap

        # calc & pembobotan untuk mencari tingkat kerusakan komponen arsitektur bangunan
        bobot_arsitektur = [0.15, 0.06, 0.09, 0.015, 0.01, 0.0125, 0.01, 0.05, 0.01] #nilai dari bobot komponen arsitektur
        tk_dinding = ((dinding_tr * tk_komponen[0] / v_dinding) + (dinding_rsr * tk_komponen[1] / v_dinding) + (dinding_rr * tk_komponen[2] / v_dinding) + (dinding_rs * tk_komponen[3] / v_dinding) + (dinding_rb * tk_komponen[4] / v_dinding) + (dinding_rsb * tk_komponen[5] / v_dinding) + (dinding_kts * tk_komponen[6] / v_dinding)) * bobot_arsitektur[0] #tingkat kerusakan komponen dinding
        tk_plafon = ((plafon_tr * tk_komponen[0] / v_plafon) + (plafon_rsr * tk_komponen[1] / v_plafon) + (plafon_rr * tk_komponen[2] / v_plafon) + (plafon_rs * tk_komponen[3] / v_plafon) + (plafon_rb * tk_komponen[4] / v_plafon) + (plafon_rsb * tk_komponen[5] / v_plafon) + (plafon_kts * tk_komponen[6] / v_plafon)) * bobot_arsitektur[1] #tingkat kerusakan komponen plafon
        tk_lantai = ((lantai_tr * tk_komponen[0] / v_lantai) + (lantai_rsr * tk_komponen[1] / v_lantai) + (lantai_rr * tk_komponen[2] / v_lantai) + (lantai_rs * tk_komponen[3] / v_lantai) + (lantai_rb * tk_komponen[4] / v_lantai) + (lantai_rsb * tk_komponen[5] / v_lantai) + (lantai_kts * tk_komponen[6] / v_lantai)) * bobot_arsitektur[2] #tingkat kerusakan komponen lantai
        tk_kusen = ((kusen_tr * tk_komponen[0] / j_kusen) + (kusen_rsr * tk_komponen[1] / j_kusen) + (kusen_rr * tk_komponen[2] / j_kusen) + (kusen_rs * tk_komponen[3] / j_kusen) + (kusen_rb * tk_komponen[4] / j_kusen) + (kusen_rsb * tk_komponen[5] / j_kusen) + (kusen_kts * tk_komponen[6] / j_kusen)) * bobot_arsitektur[3] #tingkat kerusakan komponen kusen
        tk_pintu = ((pintu_tr * tk_komponen[0] / j_pintu) + (pintu_rsr * tk_komponen[1] / j_pintu) + (pintu_rr * tk_komponen[2] / j_pintu) + (pintu_rs * tk_komponen[3] / j_pintu) + (pintu_rb * tk_komponen[4] / j_pintu) + (pintu_rsb * tk_komponen[5] / j_pintu) + (pintu_kts * tk_komponen[6] / j_pintu)) * bobot_arsitektur[4] #tingkat kerusakan komponen pintu
        tk_jendela = ((jendela_tr * tk_komponen[0] / j_jendela) + (jendela_rsr * tk_komponen[1] / j_jendela) + (jendela_rr * tk_komponen[2] / j_jendela) + (jendela_rs * tk_komponen[3] / j_jendela) + (jendela_rb * tk_komponen[4] / j_jendela) + (jendela_rsb * tk_komponen[5] / j_jendela) + (jendela_kts * tk_komponen[6] / j_jendela)) * bobot_arsitektur[5] #tingkat kerusakan komponen jendela
        tk_fplafon = ((fplafon_tr * tk_komponen[0] / v_fplafon) + (fplafon_rsr * tk_komponen[1] / v_fplafon) + (fplafon_rr * tk_komponen[2] / v_fplafon) + (fplafon_rs * tk_komponen[3] / v_fplafon) + (fplafon_rb * tk_komponen[4] / v_fplafon) + (fplafon_rsb * tk_komponen[5] / v_fplafon) + (fplafon_kts * tk_komponen[6] / v_fplafon)) * bobot_arsitektur[6] #tingkat kerusakan komponen fplafon
        tk_fdinding = ((fdinding_tr * tk_komponen[0] / v_fdinding) + (fdinding_rsr * tk_komponen[1] / v_fdinding) + (fdinding_rr * tk_komponen[2] / v_fdinding) + (fdinding_rs * tk_komponen[3] / v_fdinding) + (fdinding_rb * tk_komponen[4] / v_fdinding) + (fdinding_rsb * tk_komponen[5] / v_fdinding) + (fdinding_kts * tk_komponen[6] / v_fdinding)) * bobot_arsitektur[7] #tingkat kerusakan komponen fdinding
        tk_fkupin = ((fkupin_tr * tk_komponen[0] / v_fkupin) + (fkupin_rsr * tk_komponen[1] / v_fkupin) + (fkupin_rr * tk_komponen[2] / v_fkupin) + (fkupin_rs * tk_komponen[3] / v_fkupin) + (fkupin_rb * tk_komponen[4] / v_fkupin) + (fkupin_rsb * tk_komponen[5] / v_fkupin) + (fkupin_kts * tk_komponen[6] / v_fkupin)) * bobot_arsitektur[8] #tingkat kerusakan komponen fkupin
        
        # calc & pembobotan untuk mencari tingkat kerusakan komponen utilitas bangunan
        bobot_utilitas = [0.02, 0.01, 0.0125] #nilai bobot dari komponen utilitas
        tk_instalasi_listrik = (vk_listrik * bobot_utilitas[0]) #tingkat kerusakan instalasi listrik
        tk_air_bersih = (vk_air * bobot_utilitas[1]) #tingkat kerusakan drainase air
        tk_drainase = ((drainase_tr * tk_komponen[0] / v_drainase) + (drainase_rsr * tk_komponen[1] / v_drainase) + (drainase_rr * tk_komponen[2] / v_drainase) + (drainase_rs * tk_komponen[3] / v_drainase) + (drainase_rb * tk_komponen[4] / v_drainase) + (drainase_rsb * tk_komponen[5] / v_drainase) + (drainase_kts * tk_komponen[6] / v_drainase)) * bobot_utilitas[2] #tingkat kerusakan komponen drainase

        # calc tingkat kerusakan komponen untuk mencari total nilai kerusakan bangunan
        tk_bangunan = tk_pondasi + tk_kolom + tk_balok + tk_atap + tk_dinding + tk_plafon + tk_lantai + tk_kusen + tk_pintu + tk_jendela + tk_fplafon + tk_fdinding + tk_fkupin + tk_instalasi_listrik + tk_air_bersih + tk_drainase
        print(tk_bangunan)
        # kondisi untuk klasifikasi kerusakan berdasarkan total nilai kerusakan bangunan
        if tk_bangunan <= 0.3: #jika nilai tk_bangunan kurang dari atau sama dengan 30% = bangunan rusak ringan
            tk_bangunan = 'rusak ringan'
        elif tk_bangunan > 0.3 and tk_bangunan <= 0.45: #jika nilai tk_bangunan lebih besar dari 30% dan kurang dari atau sama dengan 40% = bangunan rusak sedang
            tk_bangunan = 'rusak sedang'
        else:
            tk_bangunan = 'rusak berat' #jika nilai tk_bangunan diatas 40% = bangunan rusak berat
        
        # simpan data kedalam model rumah terdampak 
        RumahTerdampak.objects.create(pemilik_rumah=pemilik_rumah, tipe_bangunan=tipe_bangunan, provinsi=provinsi, kota=kota, kecamatan=kecamatan,
                                      kelurahan=kelurahan, dusun=dusun, rw=rw, rt=rt, bencana=Bencana.objects.get(id=bencana), foto=foto, lat=lat, long=long, tingkat_kerusakan=tk_bangunan,
                                      ket_pondasi=ket_pondasi, ket_kolom=ket_kolom, ket_balok=ket_balok, ket_plantai=ket_plantai, ket_tangga=ket_tangga, ket_atap=ket_atap, ket_dinding=ket_dinding)
        
        # RumahTerdampak.objects.create(pemilik_rumah=pemilik_rumah, tipe_bangunan=tipe_bangunan, provinsi=provinsi, kota=kota, kecamatan=kecamatan,
        #                               kelurahan=kelurahan, dusun=dusun, rw=rw, rt=rt, bencana=Bencana.objects.get(id=bencana), foto=foto, tingkat_kerusakan=tk_bangunan,
        #                               ket_pondasi=ket_pondasi, ket_kolom=ket_kolom, ket_balok=ket_balok, ket_atap=ket_atap, ket_dinding=ket_dinding,
        #                               tk_pondasi=tk_pondasi, tk_kolom=tk_kolom, tk_balok=tk_balok, tk_atap=tk_atap,
        #                               tk_dinding=tk_dinding, tk_plafon=tk_plafon, tk_lantai=tk_lantai, tk_kusen=tk_kusen, tk_pintu=tk_pintu, tk_jendela=tk_jendela, tk_fplafon=tk_fplafon, tk_fdinding=tk_fdinding, tk_fkupin=tk_fkupin,
        #                               tk_instalasi_listrik=tk_instalasi_listrik, tk_air_bersih=tk_air_bersih, tk_drainase=tk_drainase)
        
        return redirect('ptkr:beranda')
    
    else:
        context = {
            'bencana': list_bencana,
        }
        return render(request, 'forms/dua-lantai.html', context)

def satuLantai(request):
    """fungsi kalkulasi kerusakan bangunan tipe satu lantai"""
    list_bencana = Bencana.objects.all()

    if request.method == 'POST':
        # ambil nilai input dari form post
        # info dasar
        pemilik_rumah = request.POST.get('pemilik_rumah')
        tipe_bangunan = "Satu lantai"
        provinsi = request.POST.get('provinsi')
        kota = request.POST.get('kota')
        kecamatan = request.POST.get('kecamatan')
        kelurahan = request.POST.get('kelurahan')
        dusun = request.POST.get('dusun')
        rw = request.POST.get('rw')
        rt = request.POST.get('rt')
        bencana = int(request.POST.get('bencana'))
        foto = request.FILES.get('foto')
        
        # tahap 1 (nilai pengamatan visual)
        ket_pondasi = request.POST.get('ket_pondasi')
        ket_kolom = request.POST.get('ket_kolom')
        ket_balok = request.POST.get('ket_balok')
        ket_atap = request.POST.get('ket_atap')
        ket_dinding = request.POST.get('ket_dinding')

        # tahap 2 (nilai volume kerusakan)
        # struktur bangunan
        vk_pondasi = float(request.POST.get('vk_pondasi'))
        # kolom
        j_kolom = float(request.POST.get('j_kolom'))
        kolom_tr = float(request.POST.get('kolom_tr'))
        kolom_rsr = float(request.POST.get('kolom_rsr'))
        kolom_rr = float(request.POST.get('kolom_rr'))
        kolom_rs = float(request.POST.get('kolom_rs'))
        kolom_rb = float(request.POST.get('kolom_rb'))
        kolom_rsb = float(request.POST.get('kolom_rsb'))
        kolom_kts = float(request.POST.get('kolom_kts'))
        # balok
        j_balok = float(request.POST.get('j_balok'))
        balok_tr = float(request.POST.get('balok_tr'))
        balok_rsr = float(request.POST.get('balok_rsr'))
        balok_rr = float(request.POST.get('balok_rr'))
        balok_rs = float(request.POST.get('balok_rs'))
        balok_rb = float(request.POST.get('balok_rb'))
        balok_rsb = float(request.POST.get('balok_rsb'))
        balok_kts = float(request.POST.get('balok_kts'))
        # atap
        v_atap = 1.00
        atap_tr = float(request.POST.get('atap_tr'))
        atap_rsr = float(request.POST.get('atap_rsr'))
        atap_rr = float(request.POST.get('atap_rr'))
        atap_rs = float(request.POST.get('atap_rs'))
        atap_rb = float(request.POST.get('atap_rb'))
        atap_rsb = float(request.POST.get('atap_rsb'))
        atap_kts = float(request.POST.get('atap_kts'))
        # arsitektur bangunan
        # dinding
        v_dinding = 1.00
        dinding_tr = float(request.POST.get('dinding_tr'))
        dinding_rsr = float(request.POST.get('dinding_rsr'))
        dinding_rr = float(request.POST.get('dinding_rr'))
        dinding_rs = float(request.POST.get('dinding_rs'))
        dinding_rb = float(request.POST.get('dinding_rb'))
        dinding_rsb = float(request.POST.get('dinding_rsb'))
        dinding_kts = float(request.POST.get('dinding_kts'))
        # plafon
        v_plafon = 1.00
        plafon_tr = float(request.POST.get('plafon_tr'))
        plafon_rsr = float(request.POST.get('plafon_rsr'))
        plafon_rr = float(request.POST.get('plafon_rr'))
        plafon_rs = float(request.POST.get('plafon_rs'))
        plafon_rb = float(request.POST.get('plafon_rb'))
        plafon_rsb = float(request.POST.get('plafon_rsb'))
        plafon_kts = float(request.POST.get('plafon_kts'))
        # lantai
        v_lantai = 1.00
        lantai_tr = float(request.POST.get('lantai_tr'))
        lantai_rsr = float(request.POST.get('lantai_rsr'))
        lantai_rr = float(request.POST.get('lantai_rr'))
        lantai_rs = float(request.POST.get('lantai_rs'))
        lantai_rb = float(request.POST.get('lantai_rb'))
        lantai_rsb = float(request.POST.get('lantai_rsb'))
        lantai_kts = float(request.POST.get('lantai_kts'))
        # kusen
        j_kusen = float(request.POST.get('j_kusen'))
        kusen_tr = float(request.POST.get('kusen_tr'))
        kusen_rsr = float(request.POST.get('kusen_rsr'))
        kusen_rr = float(request.POST.get('kusen_rr'))
        kusen_rs = float(request.POST.get('kusen_rs'))
        kusen_rb = float(request.POST.get('kusen_rb'))
        kusen_rsb = float(request.POST.get('kusen_rsb'))
        kusen_kts = float(request.POST.get('kusen_kts'))
        # pintu
        j_pintu = float(request.POST.get('j_pintu'))
        pintu_tr = float(request.POST.get('pintu_tr'))
        pintu_rsr = float(request.POST.get('pintu_rsr'))
        pintu_rr = float(request.POST.get('pintu_rr'))
        pintu_rs = float(request.POST.get('pintu_rs'))
        pintu_rb = float(request.POST.get('pintu_rb'))
        pintu_rsb = float(request.POST.get('pintu_rsb'))
        pintu_kts = float(request.POST.get('pintu_kts'))
        # jendela
        j_jendela = float(request.POST.get('j_jendela'))
        jendela_tr = float(request.POST.get('jendela_tr'))
        jendela_rsr = float(request.POST.get('jendela_rsr'))
        jendela_rr = float(request.POST.get('jendela_rr'))
        jendela_rs = float(request.POST.get('jendela_rs'))
        jendela_rb = float(request.POST.get('jendela_rb'))
        jendela_rsb = float(request.POST.get('jendela_rsb'))
        jendela_kts = float(request.POST.get('jendela_kts'))
        # fplafon
        v_fplafon = 1.00
        fplafon_tr = float(request.POST.get('fplafon_tr'))
        fplafon_rsr = float(request.POST.get('fplafon_rsr'))
        fplafon_rr = float(request.POST.get('fplafon_rr'))
        fplafon_rs = float(request.POST.get('fplafon_rs'))
        fplafon_rb = float(request.POST.get('fplafon_rb'))
        fplafon_rsb = float(request.POST.get('fplafon_rsb'))
        fplafon_kts = float(request.POST.get('fplafon_kts'))
        # fdinding
        v_fdinding = 1.00
        fdinding_tr = float(request.POST.get('fdinding_tr'))
        fdinding_rsr = float(request.POST.get('fdinding_rsr'))
        fdinding_rr = float(request.POST.get('fdinding_rr'))
        fdinding_rs = float(request.POST.get('fdinding_rs'))
        fdinding_rb = float(request.POST.get('fdinding_rb'))
        fdinding_rsb = float(request.POST.get('fdinding_rsb'))
        fdinding_kts = float(request.POST.get('fdinding_kts'))
        # fkupin
        v_fkupin = 1.00
        fkupin_tr = float(request.POST.get('fkupin_tr'))
        fkupin_rsr = float(request.POST.get('fkupin_rsr'))
        fkupin_rr = float(request.POST.get('fkupin_rr'))
        fkupin_rs = float(request.POST.get('fkupin_rs'))
        fkupin_rb = float(request.POST.get('fkupin_rb'))
        fkupin_rsb = float(request.POST.get('fkupin_rsb'))
        fkupin_kts = float(request.POST.get('fkupin_kts'))
        # utilitas
        vk_listrik = float(request.POST.get('vk_listrik'))
        vk_air = float(request.POST.get('vk_air'))
        # drainase
        v_drainase = float(request.POST.get('v_drainase'))
        drainase_tr = float(request.POST.get('drainase_tr'))
        drainase_rsr = float(request.POST.get('drainase_rsr'))
        drainase_rr = float(request.POST.get('drainase_rr'))
        drainase_rs = float(request.POST.get('drainase_rs'))
        drainase_rb = float(request.POST.get('drainase_rb'))
        drainase_rsb = float(request.POST.get('drainase_rsb'))
        drainase_kts = float(request.POST.get('drainase_kts'))
        # koordinat
        lat = float(request.POST.get('lat'))
        long = float(request.POST.get('long'))

        tk_komponen = [0.00, 0.20, 0.35, 0.50, 0.70, 0.80, 1.00] #nilai tingkat kerusakan komponen

        # calc & pembobotan untuk mencari tingkat kerusakan komponen struktur bangunan
        bobot_struktur = [0.12, 0.10, 0.08, 0.07] #nilai bobot dari komponen struktur
        tk_pondasi = vk_pondasi * bobot_struktur[0] #tingkat kerusakan komponen pondasi
        tk_kolom = ((kolom_tr * tk_komponen[0] / j_kolom) + (kolom_rsr * tk_komponen[1] / j_kolom) + (kolom_rr * tk_komponen[2] / j_kolom) + (kolom_rs * tk_komponen[3] / j_kolom) + (kolom_rb * tk_komponen[4] / j_kolom) + (kolom_rsb * tk_komponen[5] / j_kolom) + (kolom_kts * tk_komponen[6] / j_kolom)) * bobot_struktur[1] #tingkat kerusakan komponen kolom
        tk_balok = ((balok_tr * tk_komponen[0] / j_balok) + (balok_rsr * tk_komponen[1] / j_balok) + (balok_rr * tk_komponen[2] / j_balok) + (balok_rs * tk_komponen[3] / j_balok) + (balok_rb * tk_komponen[4] / j_balok) + (balok_rsb * tk_komponen[5] / j_balok) + (balok_kts * tk_komponen[6] / j_balok)) * bobot_struktur[2] #tingkat kerusakan komponen balok
        tk_atap = ((atap_tr * tk_komponen[0] / v_atap) + (atap_rsr * tk_komponen[1] / v_atap) + (atap_rr * tk_komponen[2] / v_atap) + (atap_rs * tk_komponen[3] / v_atap) + (atap_rb * tk_komponen[4] / v_atap) + (atap_rsb * tk_komponen[5] / v_atap) + (atap_kts * tk_komponen[6] / v_atap)) * bobot_struktur[3] #tingkat kerusakan komponen atap

        # calc & pembobotan untuk mencari tingkat kerusakan komponen arsitektur bangunan
        bobot_arsitektur = [0.215, 0.10, 0.145, 0.01, 0.015, 0.02, 0.03, 0.04, 0.02] #nilai dari bobot komponen arsitektur
        tk_dinding = ((dinding_tr * tk_komponen[0] / v_dinding) + (dinding_rsr * tk_komponen[1] / v_dinding) + (dinding_rr * tk_komponen[2] / v_dinding) + (dinding_rs * tk_komponen[3] / v_dinding) + (dinding_rb * tk_komponen[4] / v_dinding) + (dinding_rsb * tk_komponen[5] / v_dinding) + (dinding_kts * tk_komponen[6] / v_dinding)) * bobot_arsitektur[0] #tingkat kerusakan komponen dinding
        tk_plafon = ((plafon_tr * tk_komponen[0] / v_plafon) + (plafon_rsr * tk_komponen[1] / v_plafon) + (plafon_rr * tk_komponen[2] / v_plafon) + (plafon_rs * tk_komponen[3] / v_plafon) + (plafon_rb * tk_komponen[4] / v_plafon) + (plafon_rsb * tk_komponen[5] / v_plafon) + (plafon_kts * tk_komponen[6] / v_plafon)) * bobot_arsitektur[1] #tingkat kerusakan komponen plafon
        tk_lantai = ((lantai_tr * tk_komponen[0] / v_lantai) + (lantai_rsr * tk_komponen[1] / v_lantai) + (lantai_rr * tk_komponen[2] / v_lantai) + (lantai_rs * tk_komponen[3] / v_lantai) + (lantai_rb * tk_komponen[4] / v_lantai) + (lantai_rsb * tk_komponen[5] / v_lantai) + (lantai_kts * tk_komponen[6] / v_lantai)) * bobot_arsitektur[2] #tingkat kerusakan komponen lantai
        tk_kusen = ((kusen_tr * tk_komponen[0] / j_kusen) + (kusen_rsr * tk_komponen[1] / j_kusen) + (kusen_rr * tk_komponen[2] / j_kusen) + (kusen_rs * tk_komponen[3] / j_kusen) + (kusen_rb * tk_komponen[4] / j_kusen) + (kusen_rsb * tk_komponen[5] / j_kusen) + (kusen_kts * tk_komponen[6] / j_kusen)) * bobot_arsitektur[3] #tingkat kerusakan komponen kusen
        tk_pintu = ((pintu_tr * tk_komponen[0] / j_pintu) + (pintu_rsr * tk_komponen[1] / j_pintu) + (pintu_rr * tk_komponen[2] / j_pintu) + (pintu_rs * tk_komponen[3] / j_pintu) + (pintu_rb * tk_komponen[4] / j_pintu) + (pintu_rsb * tk_komponen[5] / j_pintu) + (pintu_kts * tk_komponen[6] / j_pintu)) * bobot_arsitektur[4] #tingkat kerusakan komponen pintu
        tk_jendela = ((jendela_tr * tk_komponen[0] / j_jendela) + (jendela_rsr * tk_komponen[1] / j_jendela) + (jendela_rr * tk_komponen[2] / j_jendela) + (jendela_rs * tk_komponen[3] / j_jendela) + (jendela_rb * tk_komponen[4] / j_jendela) + (jendela_rsb * tk_komponen[5] / j_jendela) + (jendela_kts * tk_komponen[6] / j_jendela)) * bobot_arsitektur[5] #tingkat kerusakan komponen jendela
        tk_fplafon = ((fplafon_tr * tk_komponen[0] / v_fplafon) + (fplafon_rsr * tk_komponen[1] / v_fplafon) + (fplafon_rr * tk_komponen[2] / v_fplafon) + (fplafon_rs * tk_komponen[3] / v_fplafon) + (fplafon_rb * tk_komponen[4] / v_fplafon) + (fplafon_rsb * tk_komponen[5] / v_fplafon) + (fplafon_kts * tk_komponen[6] / v_fplafon)) * bobot_arsitektur[6] #tingkat kerusakan komponen fplafon
        tk_fdinding = ((fdinding_tr * tk_komponen[0] / v_fdinding) + (fdinding_rsr * tk_komponen[1] / v_fdinding) + (fdinding_rr * tk_komponen[2] / v_fdinding) + (fdinding_rs * tk_komponen[3] / v_fdinding) + (fdinding_rb * tk_komponen[4] / v_fdinding) + (fdinding_rsb * tk_komponen[5] / v_fdinding) + (fdinding_kts * tk_komponen[6] / v_fdinding)) * bobot_arsitektur[7] #tingkat kerusakan komponen fdinding
        tk_fkupin = ((fkupin_tr * tk_komponen[0] / v_fkupin) + (fkupin_rsr * tk_komponen[1] / v_fkupin) + (fkupin_rr * tk_komponen[2] / v_fkupin) + (fkupin_rs * tk_komponen[3] / v_fkupin) + (fkupin_rb * tk_komponen[4] / v_fkupin) + (fkupin_rsb * tk_komponen[5] / v_fkupin) + (fkupin_kts * tk_komponen[6] / v_fkupin)) * bobot_arsitektur[8] #tingkat kerusakan komponen fkupin
        
        # calc & pembobotan untuk mencari tingkat kerusakan komponen utilitas bangunan
        bobot_utilitas = [0.01, 0.01, 0.015] #nilai bobot dari komponen utilitas
        tk_instalasi_listrik = (vk_listrik * bobot_utilitas[0]) #tingkat kerusakan instalasi listrik
        tk_air_bersih = (vk_air * bobot_utilitas[1]) #tingkat kerusakan drainase air
        tk_drainase = ((drainase_tr * tk_komponen[0] / v_drainase) + (drainase_rsr * tk_komponen[1] / v_drainase) + (drainase_rr * tk_komponen[2] / v_drainase) + (drainase_rs * tk_komponen[3] / v_drainase) + (drainase_rb * tk_komponen[4] / v_drainase) + (drainase_rsb * tk_komponen[5] / v_drainase) + (drainase_kts * tk_komponen[6] / v_drainase)) * bobot_utilitas[2] #tingkat kerusakan komponen drainase

        # calc tingkat kerusakan komponen untuk mencari total nilai kerusakan bangunan
        tk_bangunan = tk_pondasi + tk_kolom + tk_balok + tk_atap + tk_dinding + tk_plafon + tk_lantai + tk_kusen + tk_pintu + tk_jendela + tk_fplafon + tk_fdinding + tk_fkupin + tk_instalasi_listrik + tk_air_bersih + tk_drainase
        print(tk_bangunan)
        # kondisi untuk klasifikasi kerusakan berdasarkan total nilai kerusakan bangunan
        if tk_bangunan <= 0.3: #jika nilai tk_bangunan kurang dari atau sama dengan 30% = bangunan rusak ringan
            tk_bangunan = 'rusak ringan'
        elif tk_bangunan > 0.3 and tk_bangunan <= 0.45: #jika nilai tk_bangunan lebih besar dari 30% dan kurang dari atau sama dengan 40% = bangunan rusak sedang
            tk_bangunan = 'rusak sedang'
        else:
            tk_bangunan = 'rusak berat' #jika nilai tk_bangunan diatas 40% = bangunan rusak berat
        
        # simpan data kedalam model rumah terdampak 
        RumahTerdampak.objects.create(pemilik_rumah=pemilik_rumah, tipe_bangunan=tipe_bangunan, provinsi=provinsi, kota=kota, kecamatan=kecamatan,
                                      kelurahan=kelurahan, dusun=dusun, rw=rw, rt=rt, bencana=Bencana.objects.get(id=bencana), foto=foto, lat=lat, long=long, tingkat_kerusakan=tk_bangunan,
                                      ket_pondasi=ket_pondasi, ket_kolom=ket_kolom, ket_balok=ket_balok, ket_atap=ket_atap, ket_dinding=ket_dinding)
        
        # RumahTerdampak.objects.create(pemilik_rumah=pemilik_rumah, tipe_bangunan=tipe_bangunan, provinsi=provinsi, kota=kota, kecamatan=kecamatan,
        #                               kelurahan=kelurahan, dusun=dusun, rw=rw, rt=rt, bencana=Bencana.objects.get(id=bencana), foto=foto, tingkat_kerusakan=tk_bangunan,
        #                               ket_pondasi=ket_pondasi, ket_kolom=ket_kolom, ket_balok=ket_balok, ket_atap=ket_atap, ket_dinding=ket_dinding,
        #                               tk_pondasi=tk_pondasi, tk_kolom=tk_kolom, tk_balok=tk_balok, tk_atap=tk_atap,
        #                               tk_dinding=tk_dinding, tk_plafon=tk_plafon, tk_lantai=tk_lantai, tk_kusen=tk_kusen, tk_pintu=tk_pintu, tk_jendela=tk_jendela, tk_fplafon=tk_fplafon, tk_fdinding=tk_fdinding, tk_fkupin=tk_fkupin,
        #                               tk_instalasi_listrik=tk_instalasi_listrik, tk_air_bersih=tk_air_bersih, tk_drainase=tk_drainase)
        
        return redirect('ptkr:beranda')
    
    else:
        context = {
            'bencana': list_bencana,
        }
        return render(request, 'forms/satu-lantai.html', context)

def beranda(request):
    shp = Shp.objects.all()
    point = RumahTerdampak.objects.all()
    context = {
        'shp': shp,
        'point': point
    }
    return render(request, 'beranda.html', context)