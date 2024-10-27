from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _
from . models_bangunan import Bangunan

class ArsitekturBangunan(models.Model):
    # Dinding
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
    j_pintu = models.FloatField(_("Jumlah Pintu (Unit)"))
    pintu_tr = models.FloatField(_("Pintu Tidak Rusak"))
    pintu_rsr = models.FloatField(_("Pintu Rusak Sangat Ringan"))
    pintu_rr = models.FloatField(_("Pintu Rusak Ringan"))
    pintu_rs = models.FloatField(_("Pintu Rusak Sedang"))
    pintu_rb = models.FloatField(_("Pintu Rusak Berat"))
    pintu_rsb = models.FloatField(_("Pintu Rusak Sangat Berat"))
    pintu_kts = models.FloatField(_("Komponen Pintu Tidak Sesuai"))
    tk_pintu = models.FloatField(_("Tingkat Kerusakan Komponen Pintu"))
    
    # Jendela
    j_jendela = models.FloatField(_("Jumlah Jendela (Unit)"))
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
    fkupin_rsr = models.FloatField(_("Finishing Kusen & Pintu Rusak Sangat Ringan"))
    fkupin_rr = models.FloatField(_("Finishing Kusen & Pintu Rusak Ringan"))
    fkupin_rs = models.FloatField(_("Finishing Kusen & Pintu Rusak Sedang"))
    fkupin_rb = models.FloatField(_("Finishing Kusen & Pintu Rusak Berat"))
    fkupin_rsb = models.FloatField(_("Finishing Kusen & Pintu Rusak Sangat Berat"))
    fkupin_kts = models.FloatField(_("Komponen Finishing Kusen & Pintu Tidak Sesuai"))
    tk_fkupin = models.FloatField(_("Tingkat Kerusakan Komponen Finishing Kusen & Pintu"))

    # fk
    bangunan = models.ForeignKey(Bangunan, verbose_name=_("Bangunan"), on_delete=models.CASCADE, related_name="arsitektur_bangunan")

    class Meta:
        verbose_name = (_("Arsitektur Komponen Bangunan"))
        verbose_name_plural = (_("Arsitektur Komponen Bangunan"))