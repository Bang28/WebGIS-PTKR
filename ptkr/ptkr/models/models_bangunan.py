from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.html import mark_safe
import os
from django.core.exceptions import ValidationError
from . models_bencana import Bencana

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
    rt = models.CharField(_("RT"), max_length=3)
    rw = models.CharField(_("RW"), max_length=3)
    bencana = models.ForeignKey(Bencana, verbose_name=_("Bencana"), on_delete=models.CASCADE, related_name='rumah_terdampak')
    foto = models.ImageField(_("Foto Rumah"), upload_to=file_upload, validators=[file_size, file_extension] , height_field=None, width_field=None, max_length=None, help_text='Ukuran foto maksimal 5MB.')
    lat = models.FloatField(_("Latitude"))
    long = models.FloatField(_("Longitude"))
    publish = models.DateField(_("Tanggal diunggah"), auto_now=False, auto_now_add=True)
    koordinat = models.PointField(_("Titik Koordinat Lokasi Rumah"))

    ket_pondasi = models.CharField(_("Visual Pondasi"), max_length=255)
    ket_kolom = models.CharField(_("Visual Kolom"), max_length=255)
    ket_balok = models.CharField(_("Visual Balok"), max_length=255)
    ket_plantai = models.CharField(_("Visual Plat Lantai"), max_length=255, blank=True, null=True)
    ket_tangga = models.CharField(_("Visual Tangga"), max_length=255, blank=True, null=True)
    ket_atap = models.CharField(_("Visual Atap"), max_length=255)
    ket_dinding = models.CharField(_("Visual Dinding"), max_length=255)

    tingkat_kerusakan = models.CharField(_("Tingkat kerusakan Bangunan"), max_length=20)
    ttl_nilai_kerusakan = models.FloatField(_("Total Nilai Kerusakan Bangunan (%)"))

    def preview_img(self):
        return mark_safe(f"<img src='{self.foto.url}' width='275' />")

    class Meta:
        verbose_name = _("Bangunan Rumah Terdampak")
        verbose_name_plural = _("Bangunan Rumah Terdampak")

    def __str__(self) -> str:
        return f"{self.pemilik_rumah} tingkat kerusakan {self.tingkat_kerusakan}"