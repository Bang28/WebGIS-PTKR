from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.html import mark_safe
import os
from django.core.exceptions import ValidationError


def file_size(value):
    '''fungsi mengatur limit ukuran file yg diupload'''
    limit = 5242880 
    if value.size > limit:
        raise ValidationError('Maksimal ukuran file hanya 5MB')
    

def file_extension(value):
    '''fungsi mengatur ekstensi file yang diizinkan'''
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.png', '.jpg', 'jpeg']
    if not ext in valid_extensions:
        raise ValidationError('File tidak didukung, silahkan upload file berupa gambar(png/jpg/jpeg)')

class Bencana(models.Model):
    JENIS_BENCANA_CHOICES = [
        ('Gempa Bumi', 'Gempa Bumi'),
        ('Banjir', 'Banjir'),
        ('Topan', 'Topan'),
        ('Kebakaran', 'Kebakaran'),
        ('Tanah Bergerak', 'Tanah Bergerak'),
        ('Tanah Longsor', 'Tanah Longsor'),
    ]
    LOKASI_BENCANA_CHOICES = [
        ('Batursari', 'Batursari'),
        ('Benda', 'Benda'),
        ('Buniwah', 'Buniwah'),
        ('Dawuhan', 'Dawuhan'),
        ('Igirklanceng', 'Igirklanceng'),
        ('Kaligiri', 'Kaligiri'),
        ('Kaliloka', 'Kaliloka'),
        ('Manggis', 'Manggis'),
        ('Mendala', 'Mendala'),
        ('Mlayang', 'Mlayang'),
        ('Plompong', 'Plompong'),
        ('Sridadi', 'Sridadi'),
        ('Wanareja', 'Wanareja'),
    ]
    jenis_bencana = models.CharField(_("Jenis bencana"), max_length=50, choices=JENIS_BENCANA_CHOICES)
    tanggal_terjadi = models.DateTimeField(_("Tanggal terjadi"), auto_now=False, auto_now_add=False)
    lokasi_bencana = models.CharField(_("Desa Tempat Bencana Terjadi"), max_length=50, choices=LOKASI_BENCANA_CHOICES)
    deskripsi = models.TextField(_("Deskripsi bencana"), max_length=1000, null=True, blank=True, help_text="Opsional, boleh diisi boleh tidak.")

    class Meta:
        verbose_name = _("Bencana")
        verbose_name_plural = _("Bencana")

    def __str__(self):
        return f"{self.jenis_bencana} pada {self.tanggal_terjadi} di Desa {self.lokasi_bencana}" 

class Bangunan(models.Model):
    def file_upload(instance, filename):
        ext = filename.split('.')[-1]
        filename = "%s.%s" % (instance.pemilik_rumah, ext)
        return os.path.join('foto', filename)
    
    pemilik_rumah = models.CharField(_("Pemilik rumah"), max_length=60)
    tipe_bangunan = models.CharField(_("Tipe bangunan rumah"), max_length=50)
    provinsi = models.CharField(_("Provinsi"), max_length=150)
    kota = models.CharField(_("Kota"), max_length=150)
    kecamatan = models.CharField(_("Kecamatan"), max_length=150)
    kelurahan = models.CharField(_("Kelurahan"), max_length=150)
    dusun = models.CharField(_("Dusun"), max_length=150)
    rw = models.CharField(_("RW"), max_length=3)
    rt = models.CharField(_("RT"), max_length=3)
    bencana = models.ForeignKey(Bencana, verbose_name=_("Bencana"), on_delete=models.CASCADE, related_name='rumah_terdampak')
    foto = models.ImageField(_("Foto Rumah"), upload_to=file_upload, validators=[file_size, file_extension] , height_field=None, width_field=None, max_length=None, help_text='Ukuran foto maksimal 5MB.')
    lat = models.FloatField(_("Latitude"))
    long = models.FloatField(_("Longitude"))
    publish = models.DateField(_("Tanggal diunggah"), auto_now=False, auto_now_add=True)
    koordinat = models.PointField(_("Titik Koordinat Lokasi Rumah"))

    tingkat_kerusakan = models.CharField(_("Tingkat kerusakan Bangunan"), max_length=20)
    ttl_nilai_kerusakan = models.FloatField(_("Total Nilai Kerusakan Bangunan (%)"))

    def preview_img(self):
        return mark_safe(f"<img src='{self.foto.url}' width='275' />")

    class Meta:
        verbose_name = _("Bangunan Rumah Terdampak")
        verbose_name_plural = _("Bangunan Rumah Terdampak")

    def __str__(self) -> str:
        return f"{self.pemilik_rumah} tingkat kerusakan {self.tingkat_kerusakan}"
    

class StrukturBangunan(models.Model):
    # Pondasi
    ket_pondasi = models.CharField(_("Visual Pondasi"), max_length=255)
    vk_pondasi = models.FloatField(_("Volume Kerusakan Pondasi"))
    tk_pondasi = models.FloatField(_("Tingkat Kerusakan Komponen Pondasi"))

    # Kolom
    ket_kolom = models.CharField(_("Visual Kolom"), max_length=255)
    j_kolom = models.PositiveSmallIntegerField(_("Jumlah Kolom (Unit)"))
    kolom_tr = models.PositiveSmallIntegerField(_("Kolom Tidak Rusak"))
    kolom_rsr = models.PositiveSmallIntegerField(_("Kolom Rusak Sangat Ringan"))
    kolom_rr = models.PositiveSmallIntegerField(_("Kolom Rusak Ringan"))
    kolom_rs = models.PositiveSmallIntegerField(_("Kolom Rusak Sedang"))
    kolom_rb = models.PositiveSmallIntegerField(_("Kolom Rusak Berat"))
    kolom_rsb = models.PositiveSmallIntegerField(_("Kolom Rusak Sangat Berat"))
    kolom_kts = models.PositiveSmallIntegerField(_("Komponen Kolom Tidak Sesuai"))
    tk_kolom = models.FloatField(_("Tingkat Kerusakan Komponen Kolom"))
    
    # Balok
    ket_balok = models.CharField(_("Visual Balok"), max_length=255)
    j_balok = models.PositiveSmallIntegerField(_("Jumlah Balok (Unit)"))
    balok_tr = models.PositiveSmallIntegerField(_("Balok Tidak Rusak"))
    balok_rsr = models.PositiveSmallIntegerField(_("Balok Rusak Sangat Ringan"))
    balok_rr = models.PositiveSmallIntegerField(_("Balok Rusak Ringan"))
    balok_rs = models.PositiveSmallIntegerField(_("Balok Rusak Sedang"))
    balok_rb = models.PositiveSmallIntegerField(_("Balok Rusak Berat"))
    balok_rsb = models.PositiveSmallIntegerField(_("Balok Rusak Sangat Berat"))
    balok_kts = models.PositiveSmallIntegerField(_("Komponen Balok Tidak Sesuai"))
    tk_balok = models.FloatField(_("Tingkat Kerusakan Komponen Balok"))

    # Plat Lantai
    ket_plantai = models.CharField(_("Visual Plat Lantai"), max_length=255)
    j_plantai = models.PositiveSmallIntegerField(_("Jumlah Plat Lantai (Unit)"))
    plantai_tr = models.PositiveSmallIntegerField(_("Plat Lantai Tidak Rusak"))
    plantai_rsr = models.PositiveSmallIntegerField(_("Plat Lantai Rusak Sangat Ringan"))
    plantai_rr = models.PositiveSmallIntegerField(_("Plat Lantai Rusak Ringan"))
    plantai_rs = models.PositiveSmallIntegerField(_("Plat Lantai Rusak Sedang"))
    plantai_rb = models.PositiveSmallIntegerField(_("Plat Lantai Rusak Berat"))
    plantai_rsb = models.PositiveSmallIntegerField(_("Plat Lantai Rusak Sangat Berat"))
    plantai_kts = models.PositiveSmallIntegerField(_("Komponen Plat Lantai Tidak Sesuai"))
    tk_plantai = models.FloatField(_("Tingkat Kerusakan Komponen Plat Lantai"))
    
    # Tangga
    ket_tangga = models.CharField(_("Visual Tangga"), max_length=255)
    j_tangga = models.PositiveSmallIntegerField(_("Jumlah Tangga (Unit)"))
    tangga_tr = models.PositiveSmallIntegerField(_("Tangga Tidak Rusak"))
    tangga_rsr = models.PositiveSmallIntegerField(_("Tangga Rusak Sangat Ringan"))
    tangga_rr = models.PositiveSmallIntegerField(_("Tangga Rusak Ringan"))
    tangga_rs = models.PositiveSmallIntegerField(_("Tangga Rusak Sedang"))
    tangga_rb = models.PositiveSmallIntegerField(_("Tangga Rusak Berat"))
    tangga_rsb = models.PositiveSmallIntegerField(_("Tangga Rusak Sangat Berat"))
    tangga_kts = models.PositiveSmallIntegerField(_("Komponen Tangga Tidak Sesuai"))
    tk_tangga = models.FloatField(_("Tingkat Kerusakan Komponen Tangga"))
    
    # Atap
    ket_atap = models.CharField(_("Visual Atap"), max_length=255)
    v_atap = models.FloatField(_("Volume Atap (%)"))
    atap_tr = models.FloatField(_("Atap Tidak Rusak"))
    atap_rsr = models.FloatField(_("Atap Rusak Sangat Ringan"))
    atap_rr = models.FloatField(_("Atap Rusak Ringan"))
    atap_rs = models.FloatField(_("Atap Rusak Sedang"))
    atap_rb = models.FloatField(_("Atap Rusak Berat"))
    atap_rsb = models.FloatField(_("Atap Rusak Sangat Berat"))
    atap_kts = models.FloatField(_("Komponen Atap Tidak Sesuai"))
    tk_atap = models.FloatField(_("Tingkat Kerusakan Komponen Atap"))

    # fk
    bangunan = models.ForeignKey(Bangunan, verbose_name=_("Bangunan"), on_delete=models.CASCADE, related_name="struktur_bangunan")

    class Meta:
        verbose_name = (_("Struktur Komponen Bangunan"))
        verbose_name_plural = (_("Struktur Komponen Bangunan"))

class ArsitekturBangunan(models.Model):
    # Dinding
    ket_dinding = models.CharField(_("Visual Dinding"), max_length=255)
    v_dinding = models.FloatField(_("Volume Dinding (%)"))
    dinding_tr = models.FloatField(_("Dinding Tidak Rusak"))
    dinding_rsr = models.FloatField(_("Dinding Rusak Sangat Ringan"))
    dinding_rr = models.FloatField(_("Dinding Rusak Ringan"))
    dinding_rs = models.FloatField(_("Dinding Rusak Sedang"))
    dinding_rb = models.FloatField(_("Dinding Rusak Berat"))
    dinding_rsb = models.FloatField(_("Dinding Rusak Sangat Berat"))
    dinding_kts = models.FloatField(_("Komponen Dinding Tidak Sesuai"))
    tk_dinding = models.FloatField(_("Tingkat Kerusakan Komponen Dinding"))

    # Plafon
    v_plafon = models.FloatField(_("Volume Plafon (%)"))
    plafon_tr = models.FloatField(_("Plafon Tidak Rusak"))
    plafon_rsr = models.FloatField(_("Plafon Rusak Sangat Ringan"))
    plafon_rr = models.FloatField(_("Plafon Rusak Ringan"))
    plafon_rs = models.FloatField(_("Plafon Rusak Sedang"))
    plafon_rb = models.FloatField(_("Plafon Rusak Berat"))
    plafon_rsb = models.FloatField(_("Plafon Rusak Sangat Berat"))
    plafon_kts = models.FloatField(_("Komponen Plafon Tidak Sesuai"))
    tk_plafon = models.FloatField(_("Tingkat Kerusakan Komponen Plafon"))
    
    # Lantai
    v_lantai = models.FloatField(_("Volume Lantai (%)"))
    lantai_tr = models.FloatField(_("Lantai Tidak Rusak"))
    lantai_rsr = models.FloatField(_("Lantai Rusak Sangat Ringan"))
    lantai_rr = models.FloatField(_("Lantai Rusak Ringan"))
    lantai_rs = models.FloatField(_("Lantai Rusak Sedang"))
    lantai_rb = models.FloatField(_("Lantai Rusak Berat"))
    lantai_rsb = models.FloatField(_("Lantai Rusak Sangat Berat"))
    lantai_kts = models.FloatField(_("Komponen Lantai Tidak Sesuai"))
    tk_lantai = models.FloatField(_("Tingkat Kerusakan Komponen Lantai"))
    
    # Kusen
    j_kusen = models.PositiveSmallIntegerField(_("Jumlah Kusen (Unit)"))
    kusen_tr = models.PositiveSmallIntegerField(_("Kusen Tidak Rusak"))
    kusen_rsr = models.PositiveSmallIntegerField(_("Kusen Rusak Sangat Ringan"))
    kusen_rr = models.PositiveSmallIntegerField(_("Kusen Rusak Ringan"))
    kusen_rs = models.PositiveSmallIntegerField(_("Kusen Rusak Sedang"))
    kusen_rb = models.PositiveSmallIntegerField(_("Kusen Rusak Berat"))
    kusen_rsb = models.PositiveSmallIntegerField(_("Kusen Rusak Sangat Berat"))
    kusen_kts = models.PositiveSmallIntegerField(_("Komponen Kusen Tidak Sesuai"))
    tk_kusen = models.FloatField(_("Tingkat Kerusakan Komponen Kusen"))
    
    # Pintu
    j_pintu = models.FloatField(_("Volume Pintu (%)"))
    pintu_tr = models.FloatField(_("Pintu Tidak Rusak"))
    pintu_rsr = models.FloatField(_("Pintu Rusak Sangat Ringan"))
    pintu_rr = models.FloatField(_("Pintu Rusak Ringan"))
    pintu_rs = models.FloatField(_("Pintu Rusak Sedang"))
    pintu_rb = models.FloatField(_("Pintu Rusak Berat"))
    pintu_rsb = models.FloatField(_("Pintu Rusak Sangat Berat"))
    pintu_kts = models.FloatField(_("Komponen Pintu Tidak Sesuai"))
    tk_pintu = models.FloatField(_("Tingkat Kerusakan Komponen Pintu"))
    
    # Jendela
    j_jendela = models.FloatField(_("Volume Jendela (%)"))
    jendela_tr = models.FloatField(_("Jendela Tidak Rusak"))
    jendela_rsr = models.FloatField(_("Jendela Rusak Sangat Ringan"))
    jendela_rr = models.FloatField(_("Jendela Rusak Ringan"))
    jendela_rs = models.FloatField(_("Jendela Rusak Sedang"))
    jendela_rb = models.FloatField(_("Jendela Rusak Berat"))
    jendela_rsb = models.FloatField(_("Jendela Rusak Sangat Berat"))
    jendela_kts = models.FloatField(_("Komponen Jendela Tidak Sesuai"))
    tk_jendela = models.FloatField(_("Tingkat Kerusakan Komponen Jendela"))

    # Finishing Plafon
    v_fplafon = models.FloatField(_("Volume Finishing Plafon (%)"))
    fplafon_tr = models.FloatField(_("Finishing Plafon Tidak Rusak"))
    fplafon_rsr = models.FloatField(_("Finishing Plafon Rusak Sangat Ringan"))
    fplafon_rr = models.FloatField(_("Finishing Plafon Rusak Ringan"))
    fplafon_rs = models.FloatField(_("Finishing Plafon Rusak Sedang"))
    fplafon_rb = models.FloatField(_("Finishing Plafon Rusak Berat"))
    fplafon_rsb = models.FloatField(_("Finishing Plafon Rusak Sangat Berat"))
    fplafon_kts = models.FloatField(_("Komponen Finishing Plafon Tidak Sesuai"))
    tk_fplafon = models.FloatField(_("Tingkat Kerusakan Komponen Finishing Plafon"))

    # Finishing Dinding
    v_fdinding = models.FloatField(_("Volume Finishing Dinding (%)"))
    fdinding_tr = models.FloatField(_("Finishing Dinding Tidak Rusak"))
    fdinding_rsr = models.FloatField(_("Finishing Dinding Rusak Sangat Ringan"))
    fdinding_rr = models.FloatField(_("Finishing Dinding Rusak Ringan"))
    fdinding_rs = models.FloatField(_("Finishing Dinding Rusak Sedang"))
    fdinding_rb = models.FloatField(_("Finishing Dinding Rusak Berat"))
    fdinding_rsb = models.FloatField(_("Finishing Dinding Rusak Sangat Berat"))
    fdinding_kts = models.FloatField(_("Komponen Finishing Dinding Tidak Sesuai"))
    tk_fdinding = models.FloatField(_("Tingkat Kerusakan Komponen Finishing Dinding"))
    
    # Finishing Kusen & Pintu
    v_fkupin = models.FloatField(_("Volume Finishing Kusen & Pintu (%)"))
    fkupin_tr = models.FloatField(_("Finishing Kusen & Pintu Tidak Rusak"))
    fkupinrsr = models.FloatField(_("Finishing Kusen & Pintu Rusak Sangat Ringan"))
    fkupinrr = models.FloatField(_("Finishing Kusen & Pintu Rusak Ringan"))
    fkupinrs = models.FloatField(_("Finishing Kusen & Pintu Rusak Sedang"))
    fkupinrb = models.FloatField(_("Finishing Kusen & Pintu Rusak Berat"))
    fkupinrsb = models.FloatField(_("Finishing Kusen & Pintu Rusak Sangat Berat"))
    fkupinkts = models.FloatField(_("Komponen Finishing Kusen & Pintu Tidak Sesuai"))
    tk_fkupin = models.FloatField(_("Tingkat Kerusakan Komponen Finishing Kusen & Pintu"))

    # fk
    bangunan = models.ForeignKey(Bangunan, verbose_name=_("Bangunan"), on_delete=models.CASCADE, related_name="arsitektur_bangunan")

    class Meta:
        verbose_name = (_("Arsitektur Komponen Bangunan"))
        verbose_name_plural = (_("Arsitektur Komponen Bangunan"))

class UtilitasBangunan(models.Model):
    vk_listrik = models.FloatField(_("Voluke Kerusakan Instalasi Listrik (Estimasi)"))
    vk_air = models.FloatField(_("Voluke Kerusakan Instalasi Air Bersih (Estimasi)"))

    # Drainase
    v_drainase = models.PositiveSmallIntegerField(_("Volume Drainase M1(Meter Lari)"))
    drainase_tr = models.PositiveSmallIntegerField(_("Drainase Tidak Rusak"))
    drainase_rsr = models.PositiveSmallIntegerField(_("Drainase Rusak Sangat Ringan"))
    drainase_rr = models.PositiveSmallIntegerField(_("Drainase Rusak Ringan"))
    drainase_rs = models.PositiveSmallIntegerField(_("Drainase Rusak Sedang"))
    drainase_rb = models.PositiveSmallIntegerField(_("Drainase Rusak Berat"))
    drainase_rsb = models.PositiveSmallIntegerField(_("Drainase Rusak Sangat Berat"))
    drainase_kts = models.PositiveSmallIntegerField(_("Komponen Drainase Tidak Sesuai"))
    tk_drainase = models.FloatField(_("Tingkat Kerusakan Komponen Drainase"))

    # fk
    bangunan = models.ForeignKey(Bangunan, verbose_name=_("Bangunan"), on_delete=models.CASCADE, related_name="utilitas_bangunan")

    class Meta:
        verbose_name = (_("Utilitas Komponen Bangunan"))
        verbose_name_plural = (_("Utilitas Komponen Bangunan"))