from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.gis.geos import Point
from django.db import transaction
from django.contrib import messages
from ptkr.models.models_bangunan import Bangunan
from ptkr.models.models_bencana import Bencana
from ptkr.models.models_struktur_bangunan import StrukturBangunan
from ptkr.models.models_arsitektur_bangunan import ArsitekturBangunan
from ptkr.models.models_utilitas_bangunan import UtilitasBangunan

def satuLantai(request):
    """fungsi kalkulasi kerusakan bangunan tipe satu lantai"""
    tahun_sekarang = datetime.now().year
    
    list_bencana = Bencana.objects.all().order_by('-tanggal_terjadi')
    list_point = Bangunan.objects.filter(publish__year=tahun_sekarang)

    if request.method == 'POST':
        try:
            # ambil nilai input data info dasar dari form html
            info_dasar_fields = [
                'pemilik_rumah', 'provinsi', 'kota', 'kecamatan', 'kelurahan', 
                'dusun', 'rw', 'rt', 'bencana'
            ]
            info_dasar = {field: request.POST.get(field) for field in info_dasar_fields}
            info_dasar['tipe_bangunan'] = 'Satu Lantai'
            info_dasar['foto'] = request.FILES.get('foto')
            info_dasar['bencana'] = int(info_dasar['bencana'])

            # ambil nilai input data tahap 1 (nilai pengamatan visual)
            pondasi = float(request.POST.get('vk_pondasi'))
            pengamatan_visual = [
                'ket_pondasi', 'ket_kolom', 'ket_balok', 
                'ket_atap', 'ket_dinding'
            ]
            visual_data = {field: request.POST.get(field) for field in pengamatan_visual}

            # ambil nilai input tahap 2 (nilai volume kerusakan)
            kerusakan_komponen_struktur = {
                'kolom': ['j_kolom', 'kolom_tr', 'kolom_rsr', 'kolom_rr', 'kolom_rs', 'kolom_rb', 'kolom_rsb', 'kolom_kts'],
                'balok': ['j_balok', 'balok_tr', 'balok_rsr', 'balok_rr', 'balok_rs', 'balok_rb', 'balok_rsb', 'balok_kts'],
                'atap': ['v_atap', 'atap_tr', 'atap_rsr', 'atap_rr', 'atap_rs', 'atap_rb', 'atap_rsb', 'atap_kts'],
            }

            data_kerusakan_struktur = {}
            for komponen, fields in kerusakan_komponen_struktur.items():
                # Periksa apakah komponen adalah 'atap'
                if komponen == 'atap':
                    data_kerusakan_struktur[komponen] = {
                        field: float(request.POST.get(field, '0')) / 100 for field in fields
                    }
                else:
                    data_kerusakan_struktur[komponen] = {
                        field: float(request.POST.get(field, '0')) for field in fields
                    }

            kerusakan_komponen_arsitektur = {
                'dinding': ['v_dinding', 'dinding_tr', 'dinding_rsr', 'dinding_rr', 'dinding_rs', 'dinding_rb', 'dinding_rsb', 'dinding_kts'],
                'plafon': ['v_plafon', 'plafon_tr', 'plafon_rsr', 'plafon_rr', 'plafon_rs', 'plafon_rb', 'plafon_rsb', 'plafon_kts'],
                'lantai': ['v_lantai', 'lantai_tr', 'lantai_rsr', 'lantai_rr', 'lantai_rs', 'lantai_rb', 'lantai_rsb', 'lantai_kts'],
                'kusen': ['j_kusen', 'kusen_tr', 'kusen_rsr', 'kusen_rr', 'kusen_rs', 'kusen_rb', 'kusen_rsb', 'kusen_kts'],
                'pintu': ['j_pintu', 'pintu_tr', 'pintu_rsr', 'pintu_rr', 'pintu_rs', 'pintu_rb', 'pintu_rsb', 'pintu_kts'],
                'jendela': ['j_jendela', 'jendela_tr', 'jendela_rsr', 'jendela_rr', 'jendela_rs', 'jendela_rb', 'jendela_rsb', 'jendela_kts'],
                'fplafon': ['v_fplafon', 'fplafon_tr', 'fplafon_rsr', 'fplafon_rr', 'fplafon_rs', 'fplafon_rb', 'fplafon_rsb', 'fplafon_kts'],
                'fdinding': ['v_fdinding', 'fdinding_tr', 'fdinding_rsr', 'fdinding_rr', 'fdinding_rs', 'fdinding_rb', 'fdinding_rsb', 'fdinding_kts'],
                'fkupin': ['v_fkupin', 'fkupin_tr', 'fkupin_rsr', 'fkupin_rr', 'fkupin_rs', 'fkupin_rb', 'fkupin_rsb', 'fkupin_kts'],
            }
            
            komponen_persen_to_desimal = ['dinding', 'plafon', 'lantai', 'fplafon', 'fdinding', 'fkupin']
            data_kerusakan_arsitektur = {}
            for komponen, fields, in kerusakan_komponen_arsitektur.items():
                # rubah nilai persen ke desimal
                if komponen in komponen_persen_to_desimal:
                    data_kerusakan_arsitektur[komponen] = {
                        field: float(request.POST.get(field, '0')) / 100 for field in fields
                    }
                else:
                    data_kerusakan_arsitektur[komponen] = {
                        field: float(request.POST.get(field, '0')) for field in fields
                    }

            kerusakan_komponen_utilitas = {
                'utilitas': ['vk_listrik', 'vk_air'],
                'drainase': ['v_drainase', 'drainase_tr', 'drainase_rsr', 'drainase_rr', 'drainase_rs', 'drainase_rb', 'drainase_rsb', 'drainase_kts']
            }

            data_kerusakan_utilitas = {}
            for komponen, fields, in kerusakan_komponen_utilitas.items():
                data_kerusakan_utilitas[komponen] = {field: float(request.POST.get(field, '0')) for field in fields }


            # ambil nilai koordinat lokasi
            lat = float(request.POST.get('lat'))
            long = float(request.POST.get('long'))
            geom = Point(long, lat)

            # nilai tingkat kerusakan dan bobot komponen
            tk_komponen = [0.00, 0.20, 0.35, 0.50, 0.70, 0.80, 1.00] 
            bobot_struktur = [0.10, 0.08, 0.07]
            bobot_arsitektur = [0.215, 0.10, 0.145, 0.01, 0.015, 0.02, 0.03, 0.04, 0.02]
            bobot_utilitas = [0.01, 0.01, 0.015]

            def calc_kerusakan_struktur(data_kerusakan_struktur, komponen_fields, bobot_komponen):
                """fungsi kalkulasi tingkat kerusakan struktur berdasarkan data kerusakan dan bobot komponen"""
                tk_hasil = {}
                for idx, (komponen, fields) in enumerate(komponen_fields.items()):
                    j_komponen = data_kerusakan_struktur[komponen].get(fields[0], 1)
                    if j_komponen == 0:  # Cek jika j_komponen adalah nol
                        j_komponen = 1   # Atur nilai default untuk menghindari pembagian oleh nol
                    komponen_rusak = sum(
                        (data_kerusakan_struktur[komponen].get(field) * tk_komponen[i] / j_komponen)
                        for i, field in enumerate(fields[1:])
                    )
                    tk_hasil[komponen] = komponen_rusak * bobot_komponen[idx]

                return tk_hasil
            
            def calc_kerusakan_arsitektur(data_kerusakan_arsitektur, komponen_fields, bobot_komponen):
                """fungsi kalkulasi tingkat kerusakan arsitektur berdasarkan data kerusakan dan bobot komponen"""
                tk_hasil = {}
                for idx, (komponen, fields) in enumerate(komponen_fields.items()):
                    j_komponen = data_kerusakan_arsitektur[komponen].get(fields[0], 1)
                    if j_komponen == 0:  # Cek jika j_komponen adalah nol
                        j_komponen = 1   # Atur nilai default untuk menghindari pembagian oleh nol
                    komponen_rusak = sum(
                        (data_kerusakan_arsitektur[komponen].get(field) * tk_komponen[i] / j_komponen)
                        for i, field in enumerate(fields[1:])
                    )
                    tk_hasil[komponen] = komponen_rusak * bobot_komponen[idx]

                return tk_hasil
            
            def calc_kerusakan_utilitas(data_kerusakan_utilitas, komponen_fields, bobot_komponen):
                """fungsi kalkulasi tingkat kerusakan utilitas berdasarkan data kerusakan dan bobot komponen"""
                tk_hasil = {}
                if isinstance(komponen_fields, list):
                    # Jika komponen_fields adalah list, kita proses berbeda
                    komponen_rusak = 0
                    j_komponen = data_kerusakan_utilitas.get(komponen_fields[0], 1)
                    if j_komponen == 0:
                        j_komponen = 1
                    for i, field in enumerate(komponen_fields[1:]):
                        komponen_rusak += data_kerusakan_utilitas.get(field, 0) * tk_komponen[i] / j_komponen
                    tk_hasil['utilitas'] = komponen_rusak * bobot_komponen
                else:
                    for idx, (komponen, fields) in enumerate(komponen_fields.items()):
                        j_komponen = data_kerusakan_utilitas[komponen].get(fields[0], 1)
                        if j_komponen == 0:
                            j_komponen = 1
                        komponen_rusak = sum(
                            (data_kerusakan_utilitas[komponen].get(field) * tk_komponen[i] / j_komponen)
                            for i, field in enumerate(fields[1:])
                        )
                        tk_hasil[komponen] = komponen_rusak * bobot_komponen[idx]

                return tk_hasil

                        
            # hitung kerusakan struktur & artisektur
            tk_pondasi = pondasi * 0.12 
            print('TK Pondasi: ', tk_pondasi)
            tk_struktur = calc_kerusakan_struktur(data_kerusakan_struktur, kerusakan_komponen_struktur, bobot_struktur)
            print('TK Struktur: ', tk_struktur)
            tk_arsitektur = calc_kerusakan_arsitektur(data_kerusakan_arsitektur, kerusakan_komponen_arsitektur, bobot_arsitektur)
            print('TK Arsitektur: ', tk_arsitektur)
            tk_drainase = calc_kerusakan_utilitas(data_kerusakan_utilitas, {'drainase': kerusakan_komponen_utilitas['drainase']}, [bobot_utilitas[2]])
            print('TK Drainase: ', tk_drainase)

            # hitung kerusakan utilitas listrik dan air
            vk_listrik = data_kerusakan_utilitas['utilitas']['vk_listrik']
            vk_air = data_kerusakan_utilitas['utilitas']['vk_air']
            tk_instalasi_listrik = vk_listrik * bobot_utilitas[0]
            tk_air_bersih = vk_air * bobot_utilitas[1]
            print('Total TK listrik: ', tk_instalasi_listrik)
            print('Total TK Air: ', tk_air_bersih)
            
            # total tingkat kerusakan
            ttl_tk_struktur = sum(tk_struktur.values())
            ttl_tk_arsitektur = sum(tk_arsitektur.values())
            ttl_tk_drainase = sum(tk_drainase.values())
            print('Total TK Struktur: ', ttl_tk_struktur)
            print('Total TK Arsitektur: ', ttl_tk_arsitektur)
            print('Total TK Drainase: ', ttl_tk_drainase)

            # hitung tingkat kerusakan bangunan
            hasil_akhir = (tk_pondasi + ttl_tk_struktur + ttl_tk_arsitektur + ttl_tk_drainase + tk_instalasi_listrik + tk_air_bersih) * 100
            ttl_nilai_kerusakan = round(hasil_akhir, 2)
            print('Total TK: ', ttl_nilai_kerusakan)

            # klasifikasi tingkat kerusakan
            if ttl_nilai_kerusakan <= 30:
                tingkat_kerusakan = 'Rusak Ringan'
            elif 30 < ttl_nilai_kerusakan <= 45:
                tingkat_kerusakan = 'Rusak Sedang'
            else:
                tingkat_kerusakan = 'Rusak Berat'

            # simpan ke dalam models
            try:
                with transaction.atomic():
                    # simpan data bangunan
                    bangunan = Bangunan(
                        pemilik_rumah=info_dasar['pemilik_rumah'],
                        tipe_bangunan=info_dasar['tipe_bangunan'],
                        provinsi=info_dasar['provinsi'],
                        kota=info_dasar['kota'],
                        kecamatan=info_dasar['kecamatan'],
                        kelurahan=info_dasar['kelurahan'],
                        dusun=info_dasar['dusun'],
                        rw=info_dasar['rw'],
                        rt=info_dasar['rt'],
                        bencana=Bencana.objects.get(id=info_dasar['bencana']),
                        foto=info_dasar['foto'],
                        lat=lat,
                        long=long,
                        koordinat=geom,

                        ket_pondasi=visual_data['ket_pondasi'], 
                        ket_kolom=visual_data['ket_kolom'], 
                        ket_balok=visual_data['ket_balok'],
                        ket_atap=visual_data['ket_atap'], 
                        ket_dinding=visual_data['ket_dinding'], 
                        
                        tingkat_kerusakan=tingkat_kerusakan,
                        ttl_nilai_kerusakan=ttl_nilai_kerusakan,
                    )
                    bangunan.full_clean()
                    bangunan.save()

                    # simpan data struktur bangunan
                    struktur_bangunan = StrukturBangunan(
                        vk_pondasi=tk_pondasi,
                        tk_pondasi=tk_pondasi,

                        j_kolom=data_kerusakan_struktur['kolom']['j_kolom'],
                        kolom_tr=data_kerusakan_struktur['kolom']['kolom_tr'],
                        kolom_rsr=data_kerusakan_struktur['kolom']['kolom_rsr'],
                        kolom_rr=data_kerusakan_struktur['kolom']['kolom_rr'],
                        kolom_rs=data_kerusakan_struktur['kolom']['kolom_rs'],
                        kolom_rb=data_kerusakan_struktur['kolom']['kolom_rb'],
                        kolom_rsb=data_kerusakan_struktur['kolom']['kolom_rsb'],
                        kolom_kts=data_kerusakan_struktur['kolom']['kolom_kts'],
                        tk_kolom=tk_struktur['kolom'],

                        j_balok=data_kerusakan_struktur['balok']['j_balok'],
                        balok_tr=data_kerusakan_struktur['balok']['balok_tr'],
                        balok_rsr=data_kerusakan_struktur['balok']['balok_rsr'],
                        balok_rr=data_kerusakan_struktur['balok']['balok_rr'],
                        balok_rs=data_kerusakan_struktur['balok']['balok_rs'],
                        balok_rb=data_kerusakan_struktur['balok']['balok_rb'],
                        balok_rsb=data_kerusakan_struktur['balok']['balok_rsb'],
                        balok_kts=data_kerusakan_struktur['balok']['balok_kts'],
                        tk_balok=tk_struktur['balok'],

                        v_atap=data_kerusakan_struktur['atap']['v_atap'],
                        atap_tr=data_kerusakan_struktur['atap']['atap_tr'],
                        atap_rsr=data_kerusakan_struktur['atap']['atap_rsr'],
                        atap_rr=data_kerusakan_struktur['atap']['atap_rr'],
                        atap_rs=data_kerusakan_struktur['atap']['atap_rs'],
                        atap_rb=data_kerusakan_struktur['atap']['atap_rb'],
                        atap_rsb=data_kerusakan_struktur['atap']['atap_rsb'],
                        atap_kts=data_kerusakan_struktur['atap']['atap_kts'],
                        tk_atap=tk_struktur['atap'],

                        bangunan=bangunan,
                    )
                    struktur_bangunan.save()
                    
                    # simpan data arsitektur bangunan
                    arsitektur_bangunan = ArsitekturBangunan(
                        v_dinding=data_kerusakan_arsitektur['dinding']['v_dinding'],
                        dinding_tr=data_kerusakan_arsitektur['dinding']['dinding_tr'],
                        dinding_rsr=data_kerusakan_arsitektur['dinding']['dinding_rsr'],
                        dinding_rr=data_kerusakan_arsitektur['dinding']['dinding_rr'],
                        dinding_rs=data_kerusakan_arsitektur['dinding']['dinding_rs'],
                        dinding_rb=data_kerusakan_arsitektur['dinding']['dinding_rb'],
                        dinding_rsb=data_kerusakan_arsitektur['dinding']['dinding_rsb'],
                        dinding_kts=data_kerusakan_arsitektur['dinding']['dinding_kts'],
                        tk_dinding=tk_arsitektur['dinding'],

                        v_plafon=data_kerusakan_arsitektur['plafon']['v_plafon'],
                        plafon_tr=data_kerusakan_arsitektur['plafon']['plafon_tr'],
                        plafon_rsr=data_kerusakan_arsitektur['plafon']['plafon_rsr'],
                        plafon_rr=data_kerusakan_arsitektur['plafon']['plafon_rr'],
                        plafon_rs=data_kerusakan_arsitektur['plafon']['plafon_rs'],
                        plafon_rb=data_kerusakan_arsitektur['plafon']['plafon_rb'],
                        plafon_rsb=data_kerusakan_arsitektur['plafon']['plafon_rsb'],
                        plafon_kts=data_kerusakan_arsitektur['plafon']['plafon_kts'],
                        tk_plafon=tk_arsitektur['plafon'],

                        v_lantai=data_kerusakan_arsitektur['lantai']['v_lantai'],
                        lantai_tr=data_kerusakan_arsitektur['lantai']['lantai_tr'],
                        lantai_rsr=data_kerusakan_arsitektur['lantai']['lantai_rsr'],
                        lantai_rr=data_kerusakan_arsitektur['lantai']['lantai_rr'],
                        lantai_rs=data_kerusakan_arsitektur['lantai']['lantai_rs'],
                        lantai_rb=data_kerusakan_arsitektur['lantai']['lantai_rb'],
                        lantai_rsb=data_kerusakan_arsitektur['lantai']['lantai_rsb'],
                        lantai_kts=data_kerusakan_arsitektur['lantai']['lantai_kts'],
                        tk_lantai=tk_arsitektur['lantai'],

                        j_kusen=data_kerusakan_arsitektur['kusen']['j_kusen'],
                        kusen_tr=data_kerusakan_arsitektur['kusen']['kusen_tr'],
                        kusen_rsr=data_kerusakan_arsitektur['kusen']['kusen_rsr'],
                        kusen_rr=data_kerusakan_arsitektur['kusen']['kusen_rr'],
                        kusen_rs=data_kerusakan_arsitektur['kusen']['kusen_rs'],
                        kusen_rb=data_kerusakan_arsitektur['kusen']['kusen_rb'],
                        kusen_rsb=data_kerusakan_arsitektur['kusen']['kusen_rsb'],
                        kusen_kts=data_kerusakan_arsitektur['kusen']['kusen_kts'],
                        tk_kusen=tk_arsitektur['kusen'],
                        
                        j_pintu=data_kerusakan_arsitektur['pintu']['j_pintu'],
                        pintu_tr=data_kerusakan_arsitektur['pintu']['pintu_tr'],
                        pintu_rsr=data_kerusakan_arsitektur['pintu']['pintu_rsr'],
                        pintu_rr=data_kerusakan_arsitektur['pintu']['pintu_rr'],
                        pintu_rs=data_kerusakan_arsitektur['pintu']['pintu_rs'],
                        pintu_rb=data_kerusakan_arsitektur['pintu']['pintu_rb'],
                        pintu_rsb=data_kerusakan_arsitektur['pintu']['pintu_rsb'],
                        pintu_kts=data_kerusakan_arsitektur['pintu']['pintu_kts'],
                        tk_pintu=tk_arsitektur['pintu'],
                        
                        j_jendela=data_kerusakan_arsitektur['jendela']['j_jendela'],
                        jendela_tr=data_kerusakan_arsitektur['jendela']['jendela_tr'],
                        jendela_rsr=data_kerusakan_arsitektur['jendela']['jendela_rsr'],
                        jendela_rr=data_kerusakan_arsitektur['jendela']['jendela_rr'],
                        jendela_rs=data_kerusakan_arsitektur['jendela']['jendela_rs'],
                        jendela_rb=data_kerusakan_arsitektur['jendela']['jendela_rb'],
                        jendela_rsb=data_kerusakan_arsitektur['jendela']['jendela_rsb'],
                        jendela_kts=data_kerusakan_arsitektur['jendela']['jendela_kts'],
                        tk_jendela=tk_arsitektur['jendela'],

                        v_fplafon=data_kerusakan_arsitektur['fplafon']['v_fplafon'],
                        fplafon_tr=data_kerusakan_arsitektur['fplafon']['fplafon_tr'],
                        fplafon_rsr=data_kerusakan_arsitektur['fplafon']['fplafon_rsr'],
                        fplafon_rr=data_kerusakan_arsitektur['fplafon']['fplafon_rr'],
                        fplafon_rs=data_kerusakan_arsitektur['fplafon']['fplafon_rs'],
                        fplafon_rb=data_kerusakan_arsitektur['fplafon']['fplafon_rb'],
                        fplafon_rsb=data_kerusakan_arsitektur['fplafon']['fplafon_rsb'],
                        fplafon_kts=data_kerusakan_arsitektur['fplafon']['fplafon_kts'],
                        tk_fplafon=tk_arsitektur['fplafon'],
                        
                        v_fdinding=data_kerusakan_arsitektur['fdinding']['v_fdinding'],
                        fdinding_tr=data_kerusakan_arsitektur['fdinding']['fdinding_tr'],
                        fdinding_rsr=data_kerusakan_arsitektur['fdinding']['fdinding_rsr'],
                        fdinding_rr=data_kerusakan_arsitektur['fdinding']['fdinding_rr'],
                        fdinding_rs=data_kerusakan_arsitektur['fdinding']['fdinding_rs'],
                        fdinding_rb=data_kerusakan_arsitektur['fdinding']['fdinding_rb'],
                        fdinding_rsb=data_kerusakan_arsitektur['fdinding']['fdinding_rsb'],
                        fdinding_kts=data_kerusakan_arsitektur['fdinding']['fdinding_kts'],
                        tk_fdinding=tk_arsitektur['fdinding'],
                        
                        v_fkupin=data_kerusakan_arsitektur['fkupin']['v_fkupin'],
                        fkupin_tr=data_kerusakan_arsitektur['fkupin']['fkupin_tr'],
                        fkupin_rsr=data_kerusakan_arsitektur['fkupin']['fkupin_rsr'],
                        fkupin_rr=data_kerusakan_arsitektur['fkupin']['fkupin_rr'],
                        fkupin_rs=data_kerusakan_arsitektur['fkupin']['fkupin_rs'],
                        fkupin_rb=data_kerusakan_arsitektur['fkupin']['fkupin_rb'],
                        fkupin_rsb=data_kerusakan_arsitektur['fkupin']['fkupin_rsb'],
                        fkupin_kts=data_kerusakan_arsitektur['fkupin']['fkupin_kts'],
                        tk_fkupin=tk_arsitektur['fkupin'],

                        bangunan=bangunan,
                    )
                    arsitektur_bangunan.save()
                    
                    utilitas_bangunan = UtilitasBangunan(
                        vk_listrik=data_kerusakan_utilitas['utilitas']['vk_listrik'],
                        tk_listrik=tk_instalasi_listrik,
                        vk_air=data_kerusakan_utilitas['utilitas']['vk_air'],
                        tk_air=tk_air_bersih,
                        
                        v_drainase=data_kerusakan_utilitas['drainase']['v_drainase'],
                        drainase_tr=data_kerusakan_utilitas['drainase']['drainase_tr'],
                        drainase_rsr=data_kerusakan_utilitas['drainase']['drainase_rsr'],
                        drainase_rr=data_kerusakan_utilitas['drainase']['drainase_rr'],
                        drainase_rs=data_kerusakan_utilitas['drainase']['drainase_rs'],
                        drainase_rb=data_kerusakan_utilitas['drainase']['drainase_rb'],
                        drainase_rsb=data_kerusakan_utilitas['drainase']['drainase_rsb'],
                        drainase_kts=data_kerusakan_utilitas['drainase']['drainase_kts'],
                        tk_drainase=tk_drainase['drainase'],

                        bangunan=bangunan,
                    )
                    utilitas_bangunan.save()
                    
                    messages.success(request, 'Data laporan kerusakan rumah berhasil disimpan.')
                    return redirect('ptkr:satu')
                
            except Exception as e:
                import traceback
                error_details = traceback.format_exc()
                messages.error(request, f'Terjadi kesalahan saat menyimpan data: {str(e)}')
                print("error kesalahan: ", error_details)
                return redirect('ptkr:satu')

        except Exception as e:
            messages.error(request, f'Terjadi kesalahan: {str(e)}')
            print("error method: ", e)
            return redirect('ptkr:satu')
        
    else:
        context = {
            'bencana': list_bencana,
            'list_point': list_point,
        }
        return render(request, 'forms/satu-lantai.html', context)