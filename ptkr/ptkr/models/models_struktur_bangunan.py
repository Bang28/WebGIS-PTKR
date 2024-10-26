from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _
from . models_bangunan import Bangunan


class StrukturBangunan(models.Model):
    # Pondasi
    vk_pondasi = models.FloatField(_("Volume Kerusakan Pondasi"))
    tk_pondasi = models.FloatField(_("Tingkat Kerusakan Komponen Pondasi"))

    # Kolom
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
    j_plantai = models.PositiveSmallIntegerField(_("Jumlah Plat Lantai (Unit)"), blank=True, null=True)
    plantai_tr = models.PositiveSmallIntegerField(_("Plat Lantai Tidak Rusak"), blank=True, null=True)
    plantai_rsr = models.PositiveSmallIntegerField(_("Plat Lantai Rusak Sangat Ringan"), blank=True, null=True)
    plantai_rr = models.PositiveSmallIntegerField(_("Plat Lantai Rusak Ringan"), blank=True, null=True)
    plantai_rs = models.PositiveSmallIntegerField(_("Plat Lantai Rusak Sedang"), blank=True, null=True)
    plantai_rb = models.PositiveSmallIntegerField(_("Plat Lantai Rusak Berat"), blank=True, null=True)
    plantai_rsb = models.PositiveSmallIntegerField(_("Plat Lantai Rusak Sangat Berat"), blank=True, null=True)
    plantai_kts = models.PositiveSmallIntegerField(_("Komponen Plat Lantai Tidak Sesuai"), blank=True, null=True)
    tk_plantai = models.FloatField(_("Tingkat Kerusakan Komponen Plat Lantai"), blank=True, null=True)
    
    # Tangga
    j_tangga = models.PositiveSmallIntegerField(_("Jumlah Tangga (Unit)"), blank=True, null=True)
    tangga_tr = models.PositiveSmallIntegerField(_("Tangga Tidak Rusak"), blank=True, null=True)
    tangga_rsr = models.PositiveSmallIntegerField(_("Tangga Rusak Sangat Ringan"), blank=True, null=True)
    tangga_rr = models.PositiveSmallIntegerField(_("Tangga Rusak Ringan"), blank=True, null=True)
    tangga_rs = models.PositiveSmallIntegerField(_("Tangga Rusak Sedang"), blank=True, null=True)
    tangga_rb = models.PositiveSmallIntegerField(_("Tangga Rusak Berat"), blank=True, null=True)
    tangga_rsb = models.PositiveSmallIntegerField(_("Tangga Rusak Sangat Berat"), blank=True, null=True)
    tangga_kts = models.PositiveSmallIntegerField(_("Komponen Tangga Tidak Sesuai"), blank=True, null=True)
    tk_tangga = models.FloatField(_("Tingkat Kerusakan Komponen Tangga"), blank=True, null=True)
    
    # Atap
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