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

class RumahTerdampak(models.Model):
    def file_upload(instance, filename):
        ext = filename.split('.')[-1]
        filename = "%s.%s" % (instance.pemilik_rumah, ext)
        return os.path.join('foto', filename)
    
    # fields info personal
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
    foto = models.ImageField(_("Foto sample"), upload_to=file_upload, validators=[file_size] , height_field=None, width_field=None, max_length=None, help_text='Ukuran foto maksimal 5MB.')
    lat = models.FloatField(_("Latitude"))
    long = models.FloatField(_("Longitude"))
    publish = models.DateField(_("Tanggal diunggah"), auto_now=False, auto_now_add=True)
    geom = models.PointField(_("Titik Koordinat Lokasi Rumah"))
    

    # fields info kerusakan komponen bangunan
    ket_pondasi = models.CharField(_("Indikasi kerusakan pondasi"), max_length=255)
    ket_kolom = models.CharField(_("Indikasi kerusakan kolom"), max_length=255)
    ket_balok = models.CharField(_("Indikasi kerusakan balok"), max_length=255)
    ket_plantai = models.CharField(_("Indikasi kerusakan plat lantai"), max_length=255, null=True, blank=True)
    ket_tangga = models.CharField(_("Indikasi kerusakan tangga"), max_length=255, null=True, blank=True)
    ket_atap = models.CharField(_("Indikasi kerusakan atap"), max_length=255)
    ket_dinding = models.CharField(_("Indikasi kerusakan dinding"), max_length=255)
    tingkat_kerusakan = models.CharField(_("Tingkat kerusakan"), max_length=20)


    def preview_img(self):
        return mark_safe(f"<img src='{self.foto.url}' width='275' />")


    class Meta:
        verbose_name = _("Rumah Terdampak")
        verbose_name_plural = _("Rumah Terdampak")

    def __str__(self) -> str:
        return f"{self.pemilik_rumah} tingkat kerusakan {self.tingkat_kerusakan}"