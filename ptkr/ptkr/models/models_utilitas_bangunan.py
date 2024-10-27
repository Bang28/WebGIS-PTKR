from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _
from . models_bangunan import Bangunan

class UtilitasBangunan(models.Model):
    vk_listrik = models.FloatField(_("Volume Kerusakan Instalasi Listrik (Estimasi)"))
    tk_listrik = models.FloatField(_("Tingkat Kerusakan Instalasi Listrik"))
    vk_air = models.FloatField(_("Voluke Kerusakan Instalasi Air Bersih (Estimasi)"))
    tk_air = models.FloatField(_("Tingkat Kerusakan Instalasi Air Bersih"))

    # Drainase
    v_drainase = models.PositiveSmallIntegerField(_("Panjang Drainase M1(Meter Lari)"))
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