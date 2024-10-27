from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _

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
    tanggal_terjadi = models.DateField(_("Tanggal terjadi"), auto_now=False, auto_now_add=False)
    lokasi_bencana = models.CharField(_("Desa Tempat Bencana Terjadi"), max_length=50, choices=LOKASI_BENCANA_CHOICES)
    deskripsi = models.TextField(_("Deskripsi bencana"), max_length=1000, null=True, blank=True, help_text="Opsional, boleh diisi boleh tidak.")

    class Meta:
        verbose_name = _("Bencana")
        verbose_name_plural = _("Bencana")

    def __str__(self):
        return f"{self.jenis_bencana} pada {self.tanggal_terjadi} di Desa {self.lokasi_bencana}" 


    





