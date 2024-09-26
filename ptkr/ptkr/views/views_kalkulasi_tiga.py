from django.shortcuts import render, redirect
from django.contrib.gis.geos import Point
from django.db import transaction
from ptkr.models.ptkr import Bencana, Bangunan, StrukturBangunan, ArsitekturBangunan, UtilitasBangunan
from django.contrib import messages
from ptkr.decorators import user_is_aunthenticated

@user_is_aunthenticated
def tigaLantai(request):
    """fungsi kalkulasi kerusakan bangunan tipe satu lantai"""
    list_bencana = Bencana.objects.all().order_by('-tanggal_terjadi')
    list_point = Bangunan.objects.all()

    if request.method == 'POST':
        try:
            # ambil nilai input data info dasar dari form html
            info_dasar_fields = [
                'pemilik_rumah', 'provinsi', 'kota', 'kecamatan', 'kelurahan', 
                'dusun', 'rw', 'rt', 'bencana'
            ]
            info_dasar = {field: request.POST.get(field) for field in info_dasar_fields}
            info_dasar['tipe_bangunan'] = 'Tiga Lantai'
            info_dasar['foto'] = request.FILES.get('foto')
            info_dasar['bencana'] = int(info_dasar['bencana'])

            # ambil nilai input data tahap 1 (nilai pengamatan visual)
            pondasi = float(request.POST.get('vk_pondasi'))
            pengamatan_visual = [
                'ket_pondasi', 'ket_kolom', 'ket_balok', 'ket_plantai', 
                'ket_tangga', 'ket_atap', 'ket_dinding'
            ]
            visual_data = {field: request.POST.get(field) for field in pengamatan_visual}

            # ambil nilai input tahap 2 (nilai volume kerusakan)
            kerusakan_komponen_struktur = {
                'kolom': ['j_kolom', 'kolom_tr', 'kolom_rsr', 'kolom_rr', 'kolom_rs', 'kolom_rb', 'kolom_rsb', 'kolom_kts'],
                'balok': ['j_balok', 'balok_tr', 'balok_rsr', 'balok_rr', 'balok_rs', 'balok_rb', 'balok_rsb', 'balok_kts'],
                'plantai': ['j_plantai', 'plantai_tr', 'plantai_rsr', 'plantai_rr', 'plantai_rs', 'plantai_rb', 'plantai_rsb', 'plantai_kts'],
                'tangga': ['j_tangga', 'tangga_tr', 'tangga_rsr', 'tangga_rr', 'tangga_rs', 'tangga_rb', 'tangga_rsb', 'tangga_kts'],
                'atap': ['v_atap', 'atap_tr', 'atap_rsr', 'atap_rr', 'atap_rs', 'atap_rb', 'atap_rsb', 'atap_kts'],
            }

            data_kerusakan_struktur = {}
            for komponen, fields, in kerusakan_komponen_struktur.items():
                data_kerusakan_struktur[komponen] = {field: float(request.POST.get(field, '0')) for field in fields }

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
            
            data_kerusakan_arsitektur = {}
            for komponen, fields, in kerusakan_komponen_arsitektur.items():
                data_kerusakan_arsitektur[komponen] = {field: float(request.POST.get(field, '0')) for field in fields }

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
            bobot_struktur = [0.13, 0.12, 0.10, 0.03, 0.07]
            bobot_arsitektur = [0.0625, 0.08, 0.10, 0.015, 0.01, 0.0125, 0.03, 0.05, 0.03]
            bobot_utilitas = [0.03, 0.015, 0.015]

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
            tk_pondasi = pondasi * 0.10 
            print('TK Pondasi: ', tk_pondasi)
            tk_struktur = calc_kerusakan_struktur(data_kerusakan_struktur, kerusakan_komponen_struktur, bobot_struktur)
            print('TK Struktur', tk_struktur)
            tk_arsitektur = calc_kerusakan_arsitektur(data_kerusakan_arsitektur, kerusakan_komponen_arsitektur, bobot_arsitektur)
            print('TK Arsitektur', tk_arsitektur)
            tk_drainase = calc_kerusakan_utilitas(data_kerusakan_utilitas, {'drainase': kerusakan_komponen_utilitas['drainase']}, [bobot_utilitas[2]])
            print('TK Drainase', tk_drainase)

            # hitung kerusakan utilitas listrik dan air
            vk_listrik = data_kerusakan_utilitas['utilitas']['vk_listrik']
            vk_air = data_kerusakan_utilitas['utilitas']['vk_air']
            tk_instalasi_listrik = vk_listrik * bobot_utilitas[0]
            print('Total TK listrik: ', tk_instalasi_listrik)
            tk_air_bersih = vk_air * bobot_utilitas[1]
            print('Total TK Air: ', tk_air_bersih)
            
            # total tingkat kerusakan
            ttl_tk_struktur = sum(tk_struktur.values())
            print('Total TK Struktur: ', ttl_tk_struktur)
            ttl_tk_arsitektur = sum(tk_arsitektur.values())
            print('Total TK Arsitektur: ', ttl_tk_arsitektur)
            ttl_tk_drainase = sum(tk_drainase.values())
            print('Total TK Drainase: ', ttl_tk_drainase)

            # hitung total nilai kerusakan bangunan
            ttl_nilai_kerusakan = tk_pondasi + ttl_tk_struktur + ttl_tk_arsitektur + ttl_tk_drainase + tk_instalasi_listrik + tk_air_bersih
            print('Total TK: ', ttl_nilai_kerusakan)

            # klasifikasi tingkat kerusakan
            if ttl_nilai_kerusakan <= 0.3:
                tingkat_kerusakan = 'Rusak Ringan'
            elif 0.3 < ttl_nilai_kerusakan <= 0.45:
                tingkat_kerusakan = 'Rusak Sedang'
            else:
                tingkat_kerusakan = 'Rusak Berat'

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
                        
                        tingkat_kerusakan=tingkat_kerusakan,
                        ttl_nilai_kerusakan=ttl_nilai_kerusakan,
                    )
                    bangunan.full_clean()
                    bangunan.save()

                    # simpan data struktur bangunan
                    struktur_bangunan = StrukturBangunan(
                        ket_pondasi=visual_data['ket_pondasi'], 
                        vk_pondasi=tk_pondasi,
                        tk_pondasi=tk_pondasi,

                        ket_kolom=visual_data['ket_kolom'], 
                        j_kolom=data_kerusakan_struktur['kolom'][0],
                        kolom_tr=data_kerusakan_struktur['kolom'][1],
                        kolom_rsr=data_kerusakan_struktur['kolom'][2],
                        kolom_rr=data_kerusakan_struktur['kolom'][3],
                        kolom_rs=data_kerusakan_struktur['kolom'][4],
                        kolom_rb=data_kerusakan_struktur['kolom'][5],
                        kolom_rsb=data_kerusakan_struktur['kolom'][6],
                        kolom_ktr=data_kerusakan_struktur['kolom'][7],
                        tk_kolom=tk_struktur['kolom'],

                        ket_balok=visual_data['ket_balok'],
                        j_balok=data_kerusakan_struktur['balok'][0],
                        balok_tr=data_kerusakan_struktur['balok'][1],
                        balok_rsr=data_kerusakan_struktur['balok'][2],
                        balok_rr=data_kerusakan_struktur['balok'][3],
                        balok_rs=data_kerusakan_struktur['balok'][4],
                        balok_rb=data_kerusakan_struktur['balok'][5],
                        balok_rsb=data_kerusakan_struktur['balok'][6],
                        balok_ktr=data_kerusakan_struktur['balok'][7],
                        tk_balok=tk_struktur['balok'],

                        ket_plantai=visual_data['ket_plantai'],
                        j_plantai=data_kerusakan_struktur['plantai'][0],
                        plantai_tr=data_kerusakan_struktur['plantai'][1],
                        plantai_rsr=data_kerusakan_struktur['plantai'][2],
                        plantai_rr=data_kerusakan_struktur['plantai'][3],
                        plantai_rs=data_kerusakan_struktur['plantai'][4],
                        plantai_rb=data_kerusakan_struktur['plantai'][5],
                        plantai_rsb=data_kerusakan_struktur['plantai'][6],
                        plantai_ktr=data_kerusakan_struktur['plantai'][7],
                        tk_plantai=tk_struktur['plantai'],

                        ket_tangga=visual_data['ket_tangga'],
                        j_tangga=data_kerusakan_struktur['tangga'][0],
                        tangga_tr=data_kerusakan_struktur['tangga'][1],
                        tangga_rsr=data_kerusakan_struktur['tangga'][2],
                        tangga_rr=data_kerusakan_struktur['tangga'][3],
                        tangga_rs=data_kerusakan_struktur['tangga'][4],
                        tangga_rb=data_kerusakan_struktur['tangga'][5],
                        tangga_rsb=data_kerusakan_struktur['tangga'][6],
                        tangga_ktr=data_kerusakan_struktur['tangga'][7],
                        tk_tangga=tk_struktur['tangga'],

                        ket_atap=visual_data['ket_atap'], 
                        v_atap=data_kerusakan_struktur['atap'][0],
                        atap_tr=data_kerusakan_struktur['atap'][1],
                        atap_rsr=data_kerusakan_struktur['atap'][2],
                        atap_rr=data_kerusakan_struktur['atap'][3],
                        atap_rs=data_kerusakan_struktur['atap'][4],
                        atap_rb=data_kerusakan_struktur['atap'][5],
                        atap_rsb=data_kerusakan_struktur['atap'][6],
                        atap_ktr=data_kerusakan_struktur['atap'][7],
                        tk_atap=tk_struktur['atap'],

                        bangunan=bangunan,
                    )
                    struktur_bangunan.full_clean()
                    struktur_bangunan.save()
                    
                    # simpan data arsitektur bangunan
                    arsitektur_bangunan = ArsitekturBangunan(
                        ket_kolom=visual_data['ket_kolom'], 
                        v_dinding=data_kerusakan_arsitektur['dinding'][0],
                        dinding_tr=data_kerusakan_arsitektur['dinding'][1],
                        dinding_rsr=data_kerusakan_arsitektur['dinding'][2],
                        dinding_rr=data_kerusakan_arsitektur['dinding'][3],
                        dinding_rs=data_kerusakan_arsitektur['dinding'][4],
                        dinding_rb=data_kerusakan_arsitektur['dinding'][5],
                        dinding_rsb=data_kerusakan_arsitektur['dinding'][6],
                        dinding_ktr=data_kerusakan_arsitektur['dinding'][7],
                        tk_dinding=tk_arsitektur['dinding'],

                        v_plafon=data_kerusakan_arsitektur['plafon'][0],
                        plafon_tr=data_kerusakan_arsitektur['plafon'][1],
                        plafon_rsr=data_kerusakan_arsitektur['plafon'][2],
                        plafon_rr=data_kerusakan_arsitektur['plafon'][3],
                        plafon_rs=data_kerusakan_arsitektur['plafon'][4],
                        plafon_rb=data_kerusakan_arsitektur['plafon'][5],
                        plafon_rsb=data_kerusakan_arsitektur['plafon'][6],
                        plafon_ktr=data_kerusakan_arsitektur['plafon'][7],
                        tk_plafon=tk_arsitektur['plafon'],

                        v_lantai=data_kerusakan_arsitektur['lantai'][0],
                        lantai_tr=data_kerusakan_arsitektur['lantai'][1],
                        lantai_rsr=data_kerusakan_arsitektur['lantai'][2],
                        lantai_rr=data_kerusakan_arsitektur['lantai'][3],
                        lantai_rs=data_kerusakan_arsitektur['lantai'][4],
                        lantai_rb=data_kerusakan_arsitektur['lantai'][5],
                        lantai_rsb=data_kerusakan_arsitektur['lantai'][6],
                        lantai_ktr=data_kerusakan_arsitektur['lantai'][7],
                        tk_lantai=tk_arsitektur['lantai'],

                        j_kusen=data_kerusakan_arsitektur['kusen'][0],
                        kusen_tr=data_kerusakan_arsitektur['kusen'][1],
                        kusen_rsr=data_kerusakan_arsitektur['kusen'][2],
                        kusen_rr=data_kerusakan_arsitektur['kusen'][3],
                        kusen_rs=data_kerusakan_arsitektur['kusen'][4],
                        kusen_rb=data_kerusakan_arsitektur['kusen'][5],
                        kusen_rsb=data_kerusakan_arsitektur['kusen'][6],
                        kusen_ktr=data_kerusakan_arsitektur['kusen'][7],
                        tk_kusen=tk_arsitektur['kusen'],
                        
                        j_pintu=data_kerusakan_arsitektur['pintu'][0],
                        pintu_tr=data_kerusakan_arsitektur['pintu'][1],
                        pintu_rsr=data_kerusakan_arsitektur['pintu'][2],
                        pintu_rr=data_kerusakan_arsitektur['pintu'][3],
                        pintu_rs=data_kerusakan_arsitektur['pintu'][4],
                        pintu_rb=data_kerusakan_arsitektur['pintu'][5],
                        pintu_rsb=data_kerusakan_arsitektur['pintu'][6],
                        pintu_ktr=data_kerusakan_arsitektur['pintu'][7],
                        tk_pintu=tk_arsitektur['pintu'],
                        
                        j_jendela=data_kerusakan_arsitektur['jendela'][0],
                        jendela_tr=data_kerusakan_arsitektur['jendela'][1],
                        jendela_rsr=data_kerusakan_arsitektur['jendela'][2],
                        jendela_rr=data_kerusakan_arsitektur['jendela'][3],
                        jendela_rs=data_kerusakan_arsitektur['jendela'][4],
                        jendela_rb=data_kerusakan_arsitektur['jendela'][5],
                        jendela_rsb=data_kerusakan_arsitektur['jendela'][6],
                        jendela_ktr=data_kerusakan_arsitektur['jendela'][7],
                        tk_jendela=tk_arsitektur['jendela'],

                        v_fplafon=data_kerusakan_arsitektur['fplafon'][0],
                        fplafon_tr=data_kerusakan_arsitektur['fplafon'][1],
                        fplafon_rsr=data_kerusakan_arsitektur['fplafon'][2],
                        fplafon_rr=data_kerusakan_arsitektur['fplafon'][3],
                        fplafon_rs=data_kerusakan_arsitektur['fplafon'][4],
                        fplafon_rb=data_kerusakan_arsitektur['fplafon'][5],
                        fplafon_rsb=data_kerusakan_arsitektur['fplafon'][6],
                        fplafon_ktr=data_kerusakan_arsitektur['fplafon'][7],
                        tk_fplafon=tk_arsitektur['fplafon'],
                        
                        v_fdinding=data_kerusakan_arsitektur['fdinding'][0],
                        fdinding_tr=data_kerusakan_arsitektur['fdinding'][1],
                        fdinding_rsr=data_kerusakan_arsitektur['fdinding'][2],
                        fdinding_rr=data_kerusakan_arsitektur['fdinding'][3],
                        fdinding_rs=data_kerusakan_arsitektur['fdinding'][4],
                        fdinding_rb=data_kerusakan_arsitektur['fdinding'][5],
                        fdinding_rsb=data_kerusakan_arsitektur['fdinding'][6],
                        fdinding_ktr=data_kerusakan_arsitektur['fdinding'][7],
                        tk_fdinding=tk_arsitektur['fdinding'],
                        
                        v_fkupin=data_kerusakan_arsitektur['fkupin'][0],
                        fkupin_tr=data_kerusakan_arsitektur['fkupin'][1],
                        fkupin_rsr=data_kerusakan_arsitektur['fkupin'][2],
                        fkupin_rr=data_kerusakan_arsitektur['fkupin'][3],
                        fkupin_rs=data_kerusakan_arsitektur['fkupin'][4],
                        fkupin_rb=data_kerusakan_arsitektur['fkupin'][5],
                        fkupin_rsb=data_kerusakan_arsitektur['fkupin'][6],
                        fkupin_ktr=data_kerusakan_arsitektur['fkupin'][7],
                        tk_fkupin=tk_arsitektur['fkupin'],

                        bangunan=bangunan,
                    )
                    arsitektur_bangunan.full_clean()
                    arsitektur_bangunan.save()
                    
                    utilitas_bangunan = UtilitasBangunan(
                        vk_listrik=data_kerusakan_utilitas['utilitas'][0],
                        vk_air=data_kerusakan_utilitas['utilitas'][1],
                        
                        v_drainase=data_kerusakan_arsitektur['drainase'][0],
                        drainase_tr=data_kerusakan_arsitektur['drainase'][1],
                        drainase_rsr=data_kerusakan_arsitektur['drainase'][2],
                        drainase_rr=data_kerusakan_arsitektur['drainase'][3],
                        drainase_rs=data_kerusakan_arsitektur['drainase'][4],
                        drainase_rb=data_kerusakan_arsitektur['drainase'][5],
                        drainase_rsb=data_kerusakan_arsitektur['drainase'][6],
                        drainase_ktr=data_kerusakan_arsitektur['drainase'][7],
                        tk_drainase=tk_arsitektur['drainase'],
                    )
                    utilitas_bangunan.full_clean()
                    utilitas_bangunan.save()
                    
                    messages.success(request, 'Data rumah terdampak berhasil disimpan.')
                    return redirect('ptkr:tiga')
                
            except Exception as e:
                messages.error(request, f'Terjadi Kesalahan: {str(e)}')
                print(e)
                return redirect('ptkr:tiga')
            
        except Exception as e:
            messages.error(request, f'Terjadi kesalahan: {str(e)}')
            print(e)
            return redirect('ptkr:tiga')
    
    else:
        context = {
            'bencana': list_bencana,
            'list_point': list_point,
        }
        return render(request, 'forms/tiga-lantai.html', context)
        