from django.shortcuts import render, redirect
from ptkr.models.ptkr import Bencana, RumahTerdampak
from django.contrib import messages

def tigaLantai(request):
    """fungsi kalkulasi kerusakan bangunan tipe satu lantai"""
    list_bencana = Bencana.objects.all().order_by('-tanggal_terjadi')

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
            tk_arsitektur = calc_kerusakan_arsitektur(data_kerusakan_arsitektur, kerusakan_komponen_arsitektur, bobot_arsitektur)
            tk_drainase = calc_kerusakan_utilitas(data_kerusakan_utilitas, {'drainase': kerusakan_komponen_utilitas['drainase']}, [bobot_utilitas[2]])

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

            # hitung tingkat kerusakan bangunan
            ttl_tk = tk_pondasi + ttl_tk_struktur + ttl_tk_arsitektur + ttl_tk_drainase + tk_instalasi_listrik + tk_air_bersih
            print('Total TK: ', ttl_tk)

            # klasifikasi tingkat kerusakan
            if ttl_tk <= 0.3:
                tingkat_kerusakan = 'Rusak Ringan'
            elif 0.3 < ttl_tk <= 0.45:
                tingkat_kerusakan = 'Rusak Sedang'
            else:
                tingkat_kerusakan = 'Rusak Berat'

            # simpan ke dalam models
            tk_rumah_terdampak = RumahTerdampak(
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
                ket_pondasi=visual_data['ket_pondasi'], 
                ket_kolom=visual_data['ket_kolom'], 
                ket_balok=visual_data['ket_balok'],
                ket_plantai=visual_data['ket_plantai'],
                ket_tangga=visual_data['ket_tangga'],
                ket_atap=visual_data['ket_atap'], 
                ket_dinding=visual_data['ket_dinding'],
                tingkat_kerusakan=tingkat_kerusakan
            )
            tk_rumah_terdampak.save()
            messages.success(request, 'Data rumah terdampak berhasil disimpan.')
            return redirect('ptkr:tiga')

        except Exception as e:
            messages.error(request, f'Terjadi kesalahan saat menyimpan data: {str(e)}')
            print(e)
            return redirect('ptkr:tiga')
    
    else:
        context = {
            'bencana': list_bencana,
        }
        return render(request, 'forms/tiga-lantai.html', context)
        