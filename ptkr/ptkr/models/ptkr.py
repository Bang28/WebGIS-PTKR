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
    valid_extensions = ['.png', '.jpg']
    if not ext in valid_extensions:
        raise ValidationError('File tidak didukung, silahkan upload file berupa gambar(png/jpg)')

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
    geom = models.PointField(_("Titik Koordinat Lokasi Rumah"))
    
    # komponen struktur
    ket_pondasi = models.CharField(_("Indikasi kerusakan pondasi"), max_length=255)
    pondasi = models.FloatField(_("Tingkat Kerusakan Pondasi"))
    ket_kolom = models.CharField(_("Indikasi kerusakan kolom"), max_length=255)
    kolom = models.FloatField(_("Tingkat Kerusakan Kolom"))
    ket_balok = models.CharField(_("Indikasi kerusakan balok"), max_length=255)
    balok = models.FloatField(_("Tingkat Kerusakan Balok"))
    ket_plantai = models.CharField(_("Indikasi kerusakan plat lantai"), max_length=255, null=True, blank=True)
    plat_lantai = models.FloatField(_("Tingkat Kerusakan Plat Lantai"), null=True, blank=True)
    ket_tangga = models.CharField(_("Indikasi kerusakan tangga"), max_length=255, null=True, blank=True)
    tangga = models.FloatField(_("Tingkat Kerusakan Tangga"), null=True, blank=True)
    ket_atap = models.CharField(_("Indikasi kerusakan atap"), max_length=255)
    atap = models.FloatField(_("Tingkat Kerusakan Atap"))

    # komponen arsitektur
    ket_dinding = models.CharField(_("Indikasi kerusakan dinding"), max_length=255)
    dinding = models.FloatField(_("Tingkat Kerusakan Dinding"))
    plafon = models.FloatField(_("Tingkat Kerusakan Plafon"))
    lantai = models.FloatField(_("Tingkat Kerusakan Lantai"))
    kusen = models.FloatField(_("Tingkat Kerusakan Kusen"))
    pintu = models.FloatField(_("Tingkat Kerusakan Pintu"))
    jendela = models.FloatField(_("Tingkat Kerusakan Jendela"))
    f_plafon = models.FloatField(_("Tingkat Kerusakan Finishing Plafon"))
    f_dinding = models.FloatField(_("Tingkat Kerusakan Finishing Dinding"))
    f_kusen_pintu = models.FloatField(_("Tingkat Kerusakan Finishing Kusen & Pintu"))

    # Komponen utilitas
    instalasi_listrik = models.FloatField(_("Tingkat Kerusakan Instalasi Listrik"))
    instalasi_air_bersih = models.FloatField(_("Tingkat Kerusakan Instalasi Air Bersih"))
    drainase_limbah = models.FloatField(_("Tingkat Kerusakan Drainase Limbah"))

    tingkat_kerusakan = models.CharField(_("Tingkat kerusakan"), max_length=20)

    def preview_img(self):
        return mark_safe(f"<img src='{self.foto.url}' width='275' />")

    class Meta:
        verbose_name = _("Bangunan Terdampak")
        verbose_name_plural = _("Bangunan Terdampak")

    def __str__(self) -> str:
        return f"{self.pemilik_rumah} tingkat kerusakan {self.tingkat_kerusakan}"